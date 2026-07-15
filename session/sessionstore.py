import string
import json
from datetime import timedelta, datetime

from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.sessions.backends.base import CreateError
from django.contrib.auth.models import User

from session.models import Session

VALID_KEY_CHARS = string.ascii_lowercase + string.digits


class SessionStore:
    def __init__(self, session_key=None):
        self._session_key = session_key
        self._session_cache = self.load() if session_key else {}

    def is_empty(self):
        try:
            return not self._session_key and not self._session_cache
        except AttributeError:
            return True

    def clear(self):
        self._session_cache = {}

    def __contains__(self, key):
        return key in self._session_cache

    def __getitem__(self, key):
        return self._session_cache[key]

    def __setitem__(self, key, value):
        self._session_cache[key] = value

    def __delitem__(self, key):
        del self._session_cache[key]

    def get(self, key, default=None):
        return self._session_cache.get(key, default)

    def get_session_from_db(self):
        try:
            return Session.objects.get(
                session_key=self._session_key, expire_date__gt=timezone.now()
            )
        except Session.DoesNotExist:
            self._session_key = None
            self.clear()
            return None

    def exists(self, session_key):
        return Session.objects.filter(session_key=session_key).exists()

    def get_new_session_key(self):
        while True:
            session_key = get_random_string(32, VALID_KEY_CHARS)
            if not self.exists(session_key):
                return session_key

    def set_expiry(self, value):
        if value is None:
            try:
                del self["session_expiry"]
            except KeyError:
                pass
            return
        if isinstance(value, timedelta):
            value = timezone.now() + value
        if isinstance(value, datetime):
            value = value.isoformat()
        self["session_expiry"] = value

    def get_session_cookie_age(self):
        return 60 * 60 * 24 * 7 * 2  # default 2 weeks

    def get_expiry_date(self, **kwargs):
        modification = kwargs.get("modification", timezone.now())
        expiry = kwargs.get("expiry", self.get("session_expiry"))
        if isinstance(expiry, datetime):
            return expiry
        elif isinstance(expiry, str):
            return datetime.fromisoformat(expiry)
        expiry = expiry or self.get_session_cookie_age()
        return modification + timedelta(seconds=expiry)

    def cycle_key(self):
        data = self._session_cache
        key = self._session_key
        self.create()
        self._session_cache = data
        if key:
            self.delete(key)

    def get_expiry_age(self, **kwargs):
        modification = kwargs.get("modification", timezone.now())
        expiry = kwargs.get("expiry", self.get("session_expiry"))
        if not expiry:
            return self.get_session_cookie_age()
        if not isinstance(expiry, (datetime, str)):
            return expiry
        if isinstance(expiry, str):
            expiry = datetime.fromisoformat(expiry)
        delta = expiry - modification
        return delta.days * 86400 + delta.seconds

    def load(self):
        session = self.get_session_from_db()
        return json.loads(session.session_data) if session else {}

    def create(self):
        while True:
            self._session_key = self.get_new_session_key()
            try:
                self.save()
            except CreateError:
                continue
            return

    def save(self):
        if self._session_key is None:
            self._session_key = self.get_new_session_key()
        data = self._session_cache
        obj, created = Session.objects.update_or_create(
            session_key=self._session_key,
            defaults={
                "session_data": json.dumps(data),
                "expire_date": self.get_expiry_date(),
            },
        )
        obj.save()

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        try:
            Session.objects.get(session_key=session_key).delete()
        except Session.DoesNotExist:
            pass

    def flush(self):
        self.clear()
        self.delete()
        self._session_key = None

    def pop(self, key, default=None):
        return self._session_cache.pop(key, default)

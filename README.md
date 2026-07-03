# Bring Your Own Session

This project is part of **HW28 - Custom Session Middleware**.

The goal is to understand how Django's session framework works by implementing a simplified version of it yourself.

The project has Django's built-in session framework disabled. Authentication is still enabled, but it cannot work until a compatible session framework is implemented.

Your job is to make it work again.

## Before You Start

Create a virtual environment.

```bash
python -m venv .venv
```


Run database migrations.

```bash
python manage.py migrate
```

Start the development server.

```bash
python manage.py runserver
```

## Available URLs

The project already contains a few views that you can use while developing.

| URL                                               | Description                                                |
| ------------------------------------------------- | ---------------------------------------------------------- |
| `/register/`                                      | Creates a test user.                                       |
| `/login/?username=<username>&password=<password>` | Authenticates a user using Django's authentication system. |
| `/show/`                                          | Displays the currently authenticated user.                 |

A successful implementation should allow the following flow:

1. Register a user.
2. Log in.
3. Visit `/show/` and see the authenticated user.
4. Restart the development server.
5. Visit `/show/` again.
6. The user should still be authenticated.

## Notes

* Django's authentication middleware is already included.
* Django's session framework has been removed.
* The project will not work correctly until a compatible session framework is implemented.
* You are expected to design your own solution.

Good luck.

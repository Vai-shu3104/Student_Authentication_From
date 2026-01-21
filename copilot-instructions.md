# Copilot Instructions - Student Management System

## Project Overview
Django 6.0 student registration & authentication system with MySQL backend. Custom user model (`Student`) via custom auth flow—**does NOT use Django's built-in User model**.

## Architecture

### Core App Structure
- **`registration/`**: Handles auth (register, login, logout) + custom `Student` model + dashboard view
- **`dashboard/`**: Placeholder app (models.py empty)
- **`login/`**: Legacy/unused login views (registration app is active)
- **`student/`**: Django project config (settings, URLs, WSGI)

### Data Flow
```
Register Form → validate passwords match & email unique → hash password with make_password()
              → Student model created → redirect to login

Login Form → lookup Student by email → check_password() with hashed DB value
          → session store [student_id, student_name, student_email] → dashboard
          
Dashboard → check 'student_id' in session (redirect to login if missing)
          → render with Student object from DB
```

### Session-Based Auth (NOT Django's auth framework)
- Sessions stored in `DATABASES['default']` (MySQL)
- Keys: `student_id`, `student_name`, `student_email`
- Logout calls `request.session.flush()`
- **Every protected view must check:** `if 'student_id' not in request.session: redirect('login')`

## Database
- **Engine**: MySQL (configured in `settings.py`)
- **Credentials**: root / root @ localhost:3306, database `college`
- **Model**: `Student` (fullname, email, mobile, password—all CharField/EmailField except password is hashed)
- **Migrations**: In `registration/migrations/` (0001-0005, password field has changed multiple times)

## Key Conventions

### Password Handling
- Use `make_password(password)` when storing (from `django.contrib.auth.hashers`)
- Use `check_password(plain, hashed)` when verifying
- **Never** store plain text (avoid: `password=password` in create/update)

### URL Routing
- Root URL (`/`) redirects to `/login/` via `home()` function in `student/urls.py`
- All app URLs defined in `registration/urls.py` (login, register, dashboard, logout)
- Dashboard is protected view—always check session

### Templates
- Located in `registration/templates/registration/` (register.html, login.html, dashboard.html)
- Using Django template language with context passed from views
- Message framework used for error/success alerts (`messages.error()`, `messages.success()`)

### Forms
- **NOT using Django Forms** (no forms.py)—POST data accessed directly via `request.POST['field_name']`
- Validation done in views (password confirmation, email uniqueness check)

## Critical Dev Workflows

### Running Locally
```bash
# Install dependencies (not listed, but likely: django, mysqlclient)
python manage.py runserver          # Dev server on 8000

# Database setup
python manage.py migrate            # Apply migrations (registration app migrations exist)
python manage.py createsuperuser    # For admin access
```

### Adding New Features
1. **New Model Fields**: Add to `registration/models.py` → create migration → migrate
2. **New Auth-Protected View**: Check `'student_id' in request.session` → use dashboard pattern
3. **New Registration Field**: Add to form input in template → capture in `register` view → validate → save to Student
4. **Modify Existing Models**: Squash old migrations if they conflict (e.g., password field has 5 migration versions)

### Testing Pattern
- Session data stored directly in view (no auth decorators like `@login_required`)
- To verify auth: print/log `request.session` in views or check session table in MySQL

## Important Anti-Patterns to Avoid
- **Don't** use Django's `User` model or `authenticate()`—this project uses custom auth
- **Don't** store plain passwords—always use `make_password()`
- **Don't** forget session checks in protected views
- **Don't** hardcode credentials—database config in settings.py uses `root/root` (dev only)

## Databases & Migrations
- Migrations tracked in `registration/migrations/` with version history
- Dashboard & login apps have empty migrations (no custom models)
- If adding new model fields: `python manage.py makemigrations registration`

## File References
- [settings.py](student/settings.py): MySQL config, INSTALLED_APPS, session middleware
- [registration/views.py](registration/views.py): Core auth logic, session handling
- [registration/models.py](registration/models.py): Custom Student model
- [registration/urls.py](registration/urls.py): Route definitions

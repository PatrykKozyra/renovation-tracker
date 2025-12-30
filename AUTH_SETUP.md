# User Authentication Setup

## Overview
The Renovation Tracker includes a complete authentication system with:
- Login/Logout functionality
- User-friendly Bootstrap 5 interface
- Polish/English language support
- Max 5 users (as specified)
- Dashboard with statistics
- Mobile-responsive design

## Quick Start

### 1. Create the First User (Superuser)
```bash
python manage.py createsuperuser
```

Enter details:
- Username: `admin`
- Email: (optional)
- Password: (your secure password)

### 2. Start the Server
```bash
# Windows
run_server.bat

# macOS/Linux
./run_server.sh

# Or manually
python manage.py runserver 8003
```

### 3. Access the Application
Visit: `http://localhost:8003/`

You'll be redirected to the login page.

---

## User Management

### Adding Users (Max 5)

**Option 1: Django Admin (Recommended)**
1. Login to admin: `http://localhost:8003/admin/`
2. Go to `Users`
3. Click `Add User`
4. Enter username and password
5. Click `Save`
6. (Optional) Edit user to add:
   - First name / Last name
   - Email
   - Staff status (to access admin panel)

**Option 2: Command Line**
```bash
python manage.py createsuperuser  # For admin users
python manage.py shell  # For regular users
```

Then in shell:
```python
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='jan',
    password='secure_password',
    first_name='Jan',
    last_name='Kowalski',
    email='jan@example.com'
)
user.save()
```

### User Permissions

**Regular Users:**
- Access to dashboard
- View purchases, progress, sessions
- Limited access (no editing)

**Staff Users:**
- All regular user access
- Access to admin panel
- Can add/edit/delete data
- View admin statistics

**To make user staff:**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
user = User.objects.get(username='jan')
user.is_staff = True
user.save()
```

---

## Application Features

### Login Page
- Clean, modern design
- Username/password authentication
- Language switcher (🇵🇱 PL / 🇬🇧 EN)
- Responsive design
- Error messages for failed login

**URL:** `http://localhost:8003/login/`

### Dashboard
After login, users see:

**Summary Cards:**
- Total spending (PLN)
- Progress entries count
- Work sessions count
- Total photos

**Recent Activity:**
- Last 5 purchases
- Last 5 progress entries

**Statistics:**
- Spending by category (top 5)
- Progress by room (top 5)

**Quick Actions:**
- Add Purchase
- Add Progress
- Add Session
- Admin Panel (staff only)

**URL:** `http://localhost:8003/`

### Navigation Menu
- Panel (Dashboard)
- Zakupy (Purchases)
- Postępy (Progress)
- Sesje (Sessions)
- Admin (staff only)
- User dropdown (logout)
- Language switcher

### Pages Available

1. **Dashboard** - `http://localhost:8003/`
   - Main overview with statistics

2. **Purchases List** - `http://localhost:8003/purchases/`
   - All purchases in table format
   - Total spending summary

3. **Progress List** - `http://localhost:8003/progress/`
   - All room progress entries
   - Photo thumbnails

4. **Sessions List** - `http://localhost:8003/sessions/`
   - All work sessions
   - Total hours worked

5. **Admin Panel** - `http://localhost:8003/admin/`
   - Full CRUD operations
   - Advanced filtering
   - Image previews

---

## Language Support

### Switching Language

Users can switch between Polish and English:

**On Login Page:**
- Dropdown at bottom of login card

**When Logged In:**
- Dropdown in top navigation bar
- Language persists in session

**Supported Languages:**
- 🇵🇱 Polski (Polish) - Default
- 🇬🇧 English

**Translation Coverage:**
- All UI elements
- Navigation menus
- Form labels
- Messages
- Admin interface

---

## Security Features

### Authentication Required
All pages except login require authentication:
- Automatic redirect to login if not authenticated
- Session-based authentication
- Secure password hashing

### Password Requirements
Django default validators:
- Minimum 8 characters
- Can't be too similar to username
- Can't be entirely numeric
- Can't be a commonly used password

### Session Security
- Session cookies
- CSRF protection on all forms
- Logout clears session

---

## Mobile Access

The application is fully responsive:

**Mobile Features:**
- Touch-friendly navigation
- Responsive cards and tables
- Collapsible navbar
- Mobile-optimized forms
- Photo gallery on mobile

**Recommended:**
- Access via mobile browser
- Bookmark homepage for quick access
- Use portrait mode for forms
- Landscape for tables/lists

---

## User Limits

**Maximum 5 Users** (as specified)

To check current user count:
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
print(f"Current users: {User.objects.count()}")
```

To list all users:
```python
for user in User.objects.all():
    print(f"{user.username} - Staff: {user.is_staff}")
```

To delete a user:
```python
user = User.objects.get(username='username_to_delete')
user.delete()
```

Or via admin panel:
1. Go to `http://localhost:8003/admin/`
2. Click `Users`
3. Select user
4. Click `Delete`

---

## Common Tasks

### Reset User Password

**Via Admin:**
1. Login to admin
2. Go to Users
3. Click on user
4. Click "this form" link in password field
5. Enter new password twice
6. Save

**Via Command Line:**
```bash
python manage.py changepassword username
```

### Lock Out a User
```python
from django.contrib.auth.models import User
user = User.objects.get(username='username')
user.is_active = False
user.save()
```

### Unlock a User
```python
user.is_active = True
user.save()
```

### Make User Staff
```python
user.is_staff = True
user.save()
```

### Remove Staff Access
```python
user.is_staff = False
user.save()
```

---

## Troubleshooting

### Can't Login
1. **Check username/password**
   - Usernames are case-sensitive
   - Password must match exactly

2. **User inactive?**
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   user = User.objects.get(username='username')
   print(user.is_active)  # Should be True
   ```

3. **Reset password:**
   ```bash
   python manage.py changepassword username
   ```

### Redirected to Wrong Port
- Admin URLs are at `/admin/` not port 8000
- Use `http://localhost:8003/admin/`

### Language Not Changing
1. Clear browser cookies
2. Try different browser
3. Check settings:
   ```python
   python manage.py shell
   ```
   ```python
   from django.conf import settings
   print(settings.LANGUAGES)
   print(settings.LANGUAGE_CODE)
   ```

### Session Expired
- Login again
- Sessions persist for 2 weeks by default
- Change in settings if needed

---

## Development

### Custom User Model (Future)
Currently using Django's built-in User model.

To add custom fields:
1. Create custom User model
2. Add fields (phone, address, etc.)
3. Update AUTH_USER_MODEL setting
4. Migrate database

### Additional Authentication
Could add:
- Email verification
- Password reset via email
- Two-factor authentication
- Social login (Google, Facebook)
- API authentication (tokens)

---

## Best Practices

### User Management
- Create unique usernames
- Use strong passwords
- Assign staff status carefully
- Regular password changes
- Monitor active users

### Security
- Never share passwords
- Use HTTPS in production
- Regular security updates
- Monitor login attempts
- Backup user data

### Access Control
- Limit staff access
- Remove unused accounts
- Review permissions regularly
- Use groups for permissions
- Audit user activities

---

## Testing

### Test Login
1. Create test user
2. Logout of current session
3. Login with test credentials
4. Verify dashboard loads
5. Test navigation
6. Test language switch
7. Logout

### Test Permissions
1. Login as regular user
2. Verify can't access admin
3. Verify can view lists
4. Login as staff user
5. Verify admin access
6. Verify CRUD operations

---

## URLs Reference

**Public:**
- Login: `/login/`

**Protected (Require Login):**
- Dashboard: `/`
- Purchases: `/purchases/`
- Progress: `/progress/`
- Sessions: `/sessions/`
- Logout: `/logout/`

**Admin (Require Staff):**
- Admin Home: `/admin/`
- All admin URLs: `/admin/...`

**Utilities:**
- Language Switch: `/i18n/setlang/`

---

For additional help, see:
- [README.md](README.md) - Main setup guide
- [GETTING_STARTED.md](GETTING_STARTED.md) - Usage guide
- [ADMIN_FEATURES.md](ADMIN_FEATURES.md) - Admin features

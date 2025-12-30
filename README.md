# Renovation Tracker

A comprehensive Django-based application for tracking home renovation projects with photo uploads, progress monitoring, and expense tracking.

## Features

- **Property Management**: Manage multiple properties with full address details
- **Purchase Tracking**: Record all expenses with receipt photos, categories, and vendors
- **Room Progress**: Document renovation progress for each room with multiple photo uploads
- **Work Sessions**: Log work hours and track time spent on renovation
- **Electrical Circuits**: Document electrical panel and circuit information
- **Equipment Tracking**: Manage tools and equipment with photos and room assignments
- **TODO System**: Organize renovation tasks and shopping lists by property
- **Vendor Management**: Configurable dropdown options for vendors and categories
- **Beautiful UI**: Modern Bootstrap 5 interface with responsive design
- **Analytics Dashboard**: Visual charts and statistics using Chart.js
- **Bilingual Support**: Full Polish/English language support
- **User Authentication**: Secure login system (supports up to 5 users)
- **Flexible Media Storage**: Configure media files location (D: drive by default)

## Quick Start

### Prerequisites
- Python 3.11+
- SQLite (included with Python for development)
- PostgreSQL 12+ (for production only)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/PatrykKozyra/renovation-tracker.git
cd renovation-tracker
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Populate vendor choices (optional):**
```bash
python manage.py populate_vendors
```

6. **Create your first user:**
```bash
python manage.py createsuperuser
```

7. **Start the server:**
```bash
# Windows
run_server.bat

# macOS/Linux
./run_server.sh

# Or manually
python manage.py runserver 8003
```

8. **Access the application:**
- Main App: http://localhost:8003/
- Admin Panel: http://localhost:8003/admin/

## Media Storage Configuration

By default, all uploaded files (photos, receipts) are stored on **D:\renovation-tracker-media\** to save space on C: drive.

To change this location, edit [config/settings/base.py](config/settings/base.py:126-129):
```python
MEDIA_ROOT = Path('D:/renovation-tracker-media')  # Change this path as needed
```

## Project Structure

```
renovation-tracker/
├── config/                    # Django project configuration
│   ├── settings/
│   │   ├── base.py           # Base settings
│   │   ├── dev.py            # Development (SQLite)
│   │   └── production.py     # Production (PostgreSQL)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── renovation/                # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── forms.py              # Beautiful crispy forms
│   ├── admin.py              # Admin customization
│   ├── urls.py               # URL routing
│   └── templates/            # HTML templates
├── static/                    # Static files (CSS, JS)
├── media/                     # Deprecated (now on D: drive)
├── locale/                    # Translation files
├── D:/renovation-tracker-media/  # User uploads (photos)
├── requirements.txt           # Python dependencies
└── requirements-prod.txt      # Production dependencies
```

## Tech Stack

- **Backend**: Django 5.0
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: Bootstrap 5, Chart.js
- **Forms**: django-crispy-forms with Bootstrap 5
- **Images**: Pillow
- **Translations**: Django i18n
- **Static Files**: WhiteNoise

## Database Models

### Property
Manage multiple properties:
- Name, full address, postal code, city, country
- Renovation start/end dates
- Active/inactive status
- Owner association

### PurchaseCategory
Categories for expenses: Equipment, Materials, Labor, Fuel, etc.

### Purchase
Track all renovation expenses with:
- Date, amount, vendor, category
- Description and notes
- Receipt photo upload
- Property association

### Room
9 predefined rooms per property:
- Salon, Sypialnia, Kuchnia, Łazienka, Ubikacja
- Pokój Dziecięcy, Biuro, Korytarz, Loggia

### RoomProgress
Document progress for each room:
- Date, description, notes
- Multiple photo uploads
- Linked to specific room

### WorkSession
Log work time:
- Date, start time, end time
- Automatic duration calculation
- Notes and rooms worked on
- Property association

### ElectricalCircuit
Document electrical system:
- Circuit name, breaker number
- Room assignment
- Connected appliances, amperage

### Equipment
Track tools and equipment:
- Name, serial number, purchase details
- Multiple photo uploads
- Room assignments
- Owner association

### RenovationTask
Organize renovation work:
- Title, description, priority
- Status: Not Started, In Progress, Completed, On Hold
- Automatic start/end date tracking
- Room and property association

### ShoppingItem
Shopping list management:
- Title, quantity, unit of measure
- Status: Not Bought, Ordered, Bought & Delivered
- Vendor selection, estimated price
- Room and property association

### DropdownChoice
Configurable dropdown options:
- Vendor management (Allegro, Castorama, Leroy Merlin, etc.)
- Custom categories and options

## User Guide

### Adding Records

All forms are accessible via the **Quick Actions** section on the dashboard:

1. **Add Purchase**: Click "Dodaj zakup" to record an expense
   - Fill in date, category, amount, vendor
   - Upload receipt photo (optional)
   - Add description and notes

2. **Add Progress**: Click "Dodaj postęp" to document room progress
   - Select room and date
   - Write description
   - Upload multiple photos at once

3. **Add Work Session**: Click "Dodaj sesję" to log work hours
   - Set date, start time, end time
   - Select rooms worked on
   - Add notes

4. **Add Circuit**: Click "Dodaj obwód" to document electrical circuits
   - Circuit name and breaker number
   - Room and amperage
   - Connected appliances

5. **Manage TODO Lists**: Click "Zadania" to organize tasks and shopping
   - **Renovation Tasks**: Track work items with status and priority
   - **Shopping List**: Plan purchases with vendors and quantities
   - Filter by status (All, Active, Completed)

6. **Equipment Management**: Navigate to Equipment section
   - Add tools and equipment with photos
   - Assign equipment to rooms
   - Track purchase information

7. **Options Management**: Configure dropdown choices
   - Manage vendor list
   - Customize categories and options

### Viewing Data

- **Dashboard**: Overview with charts, statistics, and recent activity
- **Purchases**: List all expenses with filtering options
- **Progress**: View all room progress entries with photos
- **Sessions**: List work sessions with total hours

### Language Switching

Switch between Polish and English using the language dropdown in the navigation bar.

## Documentation

- **[Getting Started Guide](GETTING_STARTED.md)**: Detailed usage instructions
- **[Authentication Setup](AUTH_SETUP.md)**: User management and permissions
- **[Admin Features](ADMIN_FEATURES.md)**: Admin panel capabilities

## Settings

### Development (default)
```bash
python manage.py runserver
```
- Uses SQLite database
- DEBUG mode enabled
- Console email backend

### Production
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py runserver
```
- Uses PostgreSQL database
- Security hardening
- Real email backend

## Environment Variables

Create a `.env` file in the project root:

```env
# Required for all environments
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Required for production only
DB_NAME=renovation_tracker
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Deployment

For production deployment:

1. Install production requirements:
```bash
pip install -r requirements-prod.txt
```

2. Set environment variables (see above)

3. Collect static files:
```bash
python manage.py collectstatic
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Use a production server (Gunicorn, uWSGI) instead of runserver

## Contributing

This is a personal project for home renovation tracking. Feel free to fork and customize for your own needs.

## License

MIT License - feel free to use and modify for your own projects.

## Author

Patryk Kozyra - [GitHub](https://github.com/PatrykKozyra)

## Support

For issues or questions, please open an issue on the [GitHub repository](https://github.com/PatrykKozyra/renovation-tracker/issues).

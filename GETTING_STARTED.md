# Getting Started with Renovation Tracker

## Quick Start (5 Minutes)

### 1. Setup
```bash
# Clone/navigate to project
cd renovation-tracker

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Enter username, email (optional), password
```

### 2. Run Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000/admin/`

### 3. Initial Setup (in Admin)

#### Create Rooms (One-time)
Go to: Admin > Pomieszczenia (Rooms) > Add

Add these rooms:
- Salon
- Sypialnia
- Kuchnia
- Łazienka
- Ubikacja
- Pokój Dziecięcy
- Biuro
- Korytarz
- Loggia

#### Create Purchase Categories (One-time)
Go to: Admin > Kategorie zakupów > Add

Add these categories:
- Sprzęt (Equipment)
- Materiały (Materials)
- Robocizna (Labor)
- Paliwo (Fuel)
- Narzędzia (Tools)
- Elektryka (Electrical)
- Hydraulika (Plumbing)
- Inne (Other)

---

## Using the Admin Interface

### Dashboard Overview
After logging in, you'll see:
- **Total spending** with purchase count
- **Progress entries** count
- **Work sessions** with total hours
- **Total photos** uploaded
- **Spending breakdown** by category
- **Progress breakdown** by room

### Adding a Purchase

1. Go to **Zakupy** (Purchases) > Add
2. Fill in:
   - Date
   - Category
   - Vendor (store name)
   - Amount
   - Description
   - Optional: Upload receipt photo
   - Optional: Notes
3. Click **Save**

**Example:**
```
Date: 2024-12-30
Category: Materiały
Vendor: Castorama
Amount: 250.50
Description: Farba biała 10L, pędzle
Receipt photo: [upload]
```

### Tracking Room Progress

1. Go to **Postępy prac** (Room Progress) > Add
2. Fill in:
   - Room (select from dropdown)
   - Date
   - Description of work done
   - Optional: Notes
3. **Add photos inline:**
   - Click the photo field
   - Upload image
   - Add caption (optional)
   - Add more rows as needed
4. Click **Save**

**Example:**
```
Room: Kuchnia
Date: 2024-12-30
Description: Ukończono montaż płytek na ścianie za kuchenką
Photos:
  - [photo1.jpg] "Ściana całość"
  - [photo2.jpg] "Detal narożnika"
  - [photo3.jpg] "Połączenie z blatem"
```

### Logging Work Sessions

1. Go to **Sesje pracy** (Work Sessions) > Add
2. Fill in:
   - Date
   - Start time
   - End time (optional, can leave blank if still working)
   - Notes (what was done)
   - Rooms worked on (select multiple with Ctrl/Cmd)
3. Click **Save**

**Duration is calculated automatically!**

**Example:**
```
Date: 2024-12-30
Start: 08:30
End: 16:00
Notes: Montaż płytek w kuchni i łazience
Rooms: Kuchnia, Łazienka
→ Duration: 7h 30m (automatic)
```

### Documenting Electrical Circuits

#### Option 1: Via Room (Inline)
1. Go to **Pomieszczenia** (Rooms)
2. Click on a room (e.g., "Kuchnia")
3. Scroll to **Obwody elektryczne** section
4. Add inline:
   - Breaker number (e.g., "B15")
   - Circuit name (e.g., "Kuchnia - duże AGD")
   - Amperage (e.g., 32)
   - Connected appliances
5. Click **Save**

#### Option 2: Direct Entry
1. Go to **Obwody elektryczne** (Electrical Circuits) > Add
2. Fill in all fields
3. Click **Save**

**Example:**
```
Circuit name: Kuchnia - duże AGD
Breaker number: B15
Room: Kuchnia
Amperage: 32
Connected appliances: Piekarnik, płyta indukcyjna, zmywarka
Notes: Obwód dedykowany, kabel 3x6mm²
```

---

## Features Guide

### Image Previews
- **Receipts:** Click to view full size in new tab
- **Progress photos:** Thumbnails in lists, click for full view
- **Inline photos:** Preview while editing

### Searching
Use the search box at top right:
- **Purchases:** Search by vendor, description, notes
- **Progress:** Search by description, notes, room
- **Sessions:** Search by notes, room names
- **Circuits:** Search by name, breaker, appliances

### Filtering
Use filters on right sidebar:
- **By date:** Year, Month, Day dropdowns
- **By category:** Click category names
- **By room:** Click room names
- Combine multiple filters

### Date Hierarchy
Navigate by date at top:
- Click year → See months
- Click month → See days
- Click day → See entries
- Click "All" to reset

### Viewing Statistics

#### Dashboard:
- Total spent across all categories
- Work hours logged
- Progress entries count
- Photos uploaded

#### Category Details:
- Click any category
- See purchase count
- See total spent
- View in collapsed "Statystyki" section

#### Room Details:
- Click any room
- See progress entries (clickable link)
- See circuit count
- See work sessions count

---

## Common Workflows

### Weekly Progress Update
1. Log work session with hours
2. Add progress entry for each room worked on
3. Upload 3-5 photos per room
4. Add any purchases made this week

### After Shopping Trip
1. Add purchase entry
2. Upload receipt photo
3. Categorize correctly
4. Add notes about deals/discounts

### Monthly Review
1. Go to dashboard
2. Check total spending
3. Review spending by category
4. Check progress by room
5. Use date filters to see last 30 days

### Electrical Documentation
1. Create all rooms first
2. For each room, add circuits inline
3. Document breaker panel layout
4. Note appliance locations

---

## Tips & Tricks

### 1. Use Inline Editing
- Add circuits while editing room
- Add photos while editing progress
- Saves time vs. separate entries

### 2. Bulk Operations
- Select multiple items (checkbox on left)
- Use "Action" dropdown
- Delete multiple at once

### 3. Smart Filtering
- Combine date + category filters
- Find specific purchases quickly
- Review room-specific progress

### 4. Photo Organization
- Use descriptive captions
- Take photos from multiple angles
- Upload immediately while fresh

### 5. Work Session Notes
- Be specific about work done
- List any issues encountered
- Note materials used

### 6. Regular Updates
- Log work sessions same day
- Upload photos immediately
- Enter purchases weekly

---

## Data Entry Best Practices

### Purchases:
✅ Use consistent vendor names (e.g., always "Castorama", not "Casto")
✅ Upload receipt photos for tax/warranty
✅ Add detailed descriptions
✅ Note any discounts in notes

### Progress:
✅ Take before/during/after photos
✅ Add captions to photos
✅ Be specific in descriptions
✅ Update regularly (weekly minimum)

### Work Sessions:
✅ Log actual hours worked
✅ Note all rooms worked on
✅ Describe what was accomplished
✅ Include any problems

### Circuits:
✅ Use breaker labels from panel
✅ List ALL appliances on circuit
✅ Note amperage from breaker
✅ Test and verify before documenting

---

## Keyboard Shortcuts (Admin)

- `Ctrl/Cmd + S` - Save
- `Ctrl/Cmd + K` - Focus search
- `Alt + S` - Save and add another
- `Alt + C` - Save and continue editing

---

## Mobile Access

The admin works on mobile but is optimized for desktop:
- Browse data on phone/tablet
- Quick entry in emergency
- Photo uploads from phone camera
- Best experience on desktop for data entry

---

## Backup & Export

### Manual Backup:
```bash
# Backup database
python manage.py dumpdata > backup.json

# Backup specific app
python manage.py dumpdata renovation > renovation_backup.json
```

### Export Data:
Use Django admin's built-in "Export" (if installed) or:
- Add django-import-export package
- Install admin export functionality
- Export to CSV/Excel

---

## Troubleshooting

### Can't log in?
```bash
# Create new superuser
python manage.py createsuperuser
```

### Images not showing?
- Check `MEDIA_URL` in settings
- Verify file uploaded correctly
- Check file permissions

### Database locked?
- Close other instances
- Restart server
- Check file permissions on db.sqlite3

### Migrations not working?
```bash
# Show migration status
python manage.py showmigrations

# Run migrations
python manage.py migrate

# If stuck, try:
python manage.py migrate --run-syncdb
```

---

## Next Steps

### Customize Admin:
- Modify colors in admin CSS
- Add custom actions
- Create admin reports
- Export functionality

### Add Features:
- Budget tracking
- Timeline view
- Photo gallery
- PDF reports
- Email notifications

### Integrate Tools:
- Google Calendar sync
- Cloud photo backup
- Budget alerts
- Progress charts

---

## Getting Help

### Documentation:
- See [README.md](README.md) for setup
- See [ADMIN_FEATURES.md](ADMIN_FEATURES.md) for detailed features
- See [MODELS_SUMMARY.md](MODELS_SUMMARY.md) for data structure
- See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for code examples

### Django Resources:
- Official docs: https://docs.djangoproject.com/
- Admin docs: https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
- Tutorial: https://docs.djangoproject.com/en/5.0/intro/tutorial02/

---

## Sample Data for Testing

Want to test the system? Add this sample data:

### Rooms:
- Kuchnia (15 m²)
- Łazienka (8.5 m²)
- Salon (25 m²)

### Categories:
- All 8 standard categories

### Sample Purchase:
```
Date: Today
Category: Materiały
Vendor: Castorama
Amount: 250.50
Description: Farba biała 10L, pędzle, wałek
```

### Sample Progress:
```
Room: Kuchnia
Date: Today
Description: Rozpoczęto malowanie ścian - pierwsza warstwa
Photos: Before/After shots
```

### Sample Session:
```
Date: Today
Start: 09:00
End: 17:00
Notes: Malowanie kuchni - pierwsza warstwa
Rooms: Kuchnia
```

---

Happy tracking! 🏠🔨

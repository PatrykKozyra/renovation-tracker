# Django Admin - Comprehensive Features

## Overview
The renovation tracker includes a fully-featured Django admin interface with Polish language support, image previews, statistics dashboard, and advanced filtering capabilities.

## Dashboard Statistics

When you log into the admin panel, you'll see a custom dashboard with:

### Key Metrics (Card Display):
1. **Całkowite wydatki** (Total Spending)
   - Total amount spent in PLN
   - Number of purchases

2. **Postęp prac** (Work Progress)
   - Number of progress entries

3. **Sesje pracy** (Work Sessions)
   - Number of sessions
   - Total hours worked

4. **Zdjęcia** (Photos)
   - Total progress photos uploaded

### Breakdown Tables:
- **Wydatki według kategorii** (Spending by Category)
  - Shows spending for each purchase category
  - Sorted by highest spending first

- **Postęp według pomieszczeń** (Progress by Room)
  - Shows number of progress entries per room
  - Sorted by most active rooms first

## Model Admin Features

### 1. Purchase Category Admin
**List View:**
- Category name (Polish translation)
- Description
- Number of purchases
- Total amount spent
- Created date

**Features:**
- Search by name and description
- Statistics in detail view (collapsible)
- Purchase count and total spent displayed

**Detail View:**
- Basic information section
- Statistics section (collapsible)
- Metadata section (collapsible)

---

### 2. Purchase Admin
**List View:**
- Date
- Vendor
- Category
- Amount (bold, formatted)
- Description (truncated to 50 chars)
- Receipt indicator (✓/✗)

**Features:**
- **Date hierarchy** - Browse by year/month/day
- **Filters:** Category, Date, Vendor
- **Search:** Vendor, Description, Notes
- **Image preview** in detail view (300px max)
- **Receipt photo** with clickable preview
- 50 items per page

**Detail View Sections:**
1. **Podstawowe informacje** (Basic Info)
   - Date, Category, Vendor, Amount

2. **Szczegóły** (Details)
   - Description, Notes

3. **Paragon** (Receipt)
   - Upload field
   - Image preview (clickable)

4. **Metadane** (Metadata - collapsed)
   - Created/Updated timestamps

---

### 3. Room Admin
**List View:**
- Room name (Polish)
- Square meters
- Progress entries count (with link)
- Circuit count
- Created date

**Features:**
- Search by name and description
- **Inline editing** for electrical circuits
- Statistics in detail view
- Link to related progress entries

**Inline:**
- Electrical circuits (tabular)
- Show change link for detailed editing

**Detail View:**
- Basic information
- Statistics (collapsible) - progress count, circuits, sessions
- Metadata (collapsible)

---

### 4. Room Progress Admin
**List View:**
- Room
- Date
- Description (truncated to 60 chars)
- Photo count
- Created date

**Features:**
- **Date hierarchy** - Browse by date
- **Filters:** Room, Date
- **Search:** Description, Notes, Room name
- **Inline photo editing** with previews
- Photo count displayed
- 50 items per page

**Inline Photos:**
- Photo upload
- Photo preview (150px in inline)
- Caption
- Upload timestamp
- Tabular display

**Detail View Sections:**
1. **Podstawowe informacje** - Room, Date
2. **Postęp prac** - Description, Notes
3. **Statystyki** (collapsed) - Photo count
4. **Metadane** (collapsed) - Timestamps

---

### 5. Room Progress Photo Admin
**List View:**
- **Thumbnail** (80x80px, cropped)
- Progress entry
- Caption (truncated to 40 chars)
- Upload date

**Features:**
- **Date hierarchy** - Browse by upload date
- **Filters:** Room (via progress), Upload date
- **Search:** Caption, Progress description
- **Full preview** in detail view (500px max)
- 50 items per page

**Detail View:**
- Progress link
- Caption field
- Photo upload
- **Large preview** (500px max, clickable)
- Upload timestamp

---

### 6. Work Session Admin
**List View:**
- Date
- Start time
- End time
- Duration (calculated, bold)
- Rooms worked on
- Notes (truncated)

**Features:**
- **Date hierarchy** - Browse by date
- **Filters:** Date, Rooms worked on
- **Search:** Notes, Room names
- **Duration calculation** (automatic)
- **Horizontal filter** for room selection
- 50 items per page

**Detail View Sections:**
1. **Czas** (Time)
   - Date, Start time, End time, Duration (calculated)

2. **Szczegóły** (Details)
   - Notes
   - Rooms worked on (multi-select with search)

3. **Metadane** (collapsed) - Timestamps

**Special Features:**
- Automatic duration calculation from start/end times
- Multi-room selection with filter interface
- Room names displayed in Polish

---

### 7. Electrical Circuit Admin
**List View:**
- Breaker number
- Circuit name
- Room
- Amperage (formatted with A)
- Connected appliances (truncated)

**Features:**
- **Filters:** Room, Amperage
- **Search:** Circuit name, Breaker number, Appliances, Notes
- Sortable by amperage
- 50 items per page

**Detail View Sections:**
1. **Podstawowe informacje**
   - Circuit name, Breaker number, Room, Amperage

2. **Szczegóły**
   - Connected appliances (text area)
   - Notes

3. **Metadane** (collapsed) - Timestamps

---

## Admin Interface Customization

### Polish Headers:
- Site header: "Panel Administracyjny Remontu"
- Site title: "Remont"
- Index title: "Zarządzanie remontem"

### Field Sections (Polish):
- **Podstawowe informacje** - Basic information
- **Szczegóły** - Details
- **Postęp prac** - Work progress
- **Czas** - Time
- **Statystyki** - Statistics
- **Metadane** - Metadata
- **Paragon** - Receipt
- **Zdjęcie** - Photo

### Visual Enhancements:
1. **Bold formatting** for important values (amounts, counts)
2. **Color coding** for receipt indicators (green ✓, red ✗)
3. **Thumbnails** in list views (80x80px)
4. **Large previews** in detail views (300-500px)
5. **Clickable images** - Open full size in new tab
6. **Truncated text** for better list view readability
7. **Collapsible sections** for metadata and statistics

---

## Search Capabilities

### Purchase:
- Vendor name
- Description
- Notes

### Room Progress:
- Description
- Notes
- Room name

### Progress Photos:
- Caption
- Progress description

### Work Sessions:
- Notes
- Room names

### Electrical Circuits:
- Circuit name
- Breaker number
- Connected appliances
- Notes

---

## Filtering Options

### By Date:
- Purchase (date hierarchy + filter)
- Room Progress (date hierarchy + filter)
- Progress Photos (upload date hierarchy + filter)
- Work Sessions (date hierarchy + filter)

### By Category/Room:
- Purchase → Category, Vendor
- Room Progress → Room
- Progress Photos → Room (via progress)
- Work Sessions → Rooms worked on
- Electrical Circuit → Room, Amperage

---

## Image Preview Features

### Receipt Photos (Purchase):
- **List view:** ✓/✗ indicator
- **Detail view:** 300px preview, clickable

### Progress Photos:
- **List view:** 80x80px thumbnail
- **Inline view:** 150px preview, clickable
- **Detail view:** 500px preview, clickable

### Photo Upload:
- All photos organized by date: `media/receipts/YYYY/MM/` and `media/progress/YYYY/MM/`
- Automatic thumbnail generation in list views
- Full-size images open in new tab

---

## Inline Editing

### Room → Electrical Circuits:
- **Type:** Tabular inline
- **Fields:** Breaker number, Circuit name, Amperage, Appliances
- **Features:** Direct editing, link to full form
- No extra empty forms by default

### Room Progress → Photos:
- **Type:** Tabular inline
- **Fields:** Photo upload, Preview, Caption, Upload date
- **Features:** Image preview, 1 extra blank form
- Quick photo addition without leaving progress entry

---

## Performance Optimizations

### Database Indexes:
- All date fields
- Category + Date composite
- Room relationships
- Breaker numbers

### Pagination:
- 50 items per page on large lists
- Default 100 for smaller lists

### Query Optimization:
- Aggregations for statistics
- Prefetch for related objects
- Count annotations

---

## Mobile Responsiveness

The Django admin is responsive by default and works on:
- Desktop browsers
- Tablets
- Mobile devices (limited functionality)

---

## User Experience Features

1. **Smart defaults** - Sections collapsed when not frequently used
2. **Visual feedback** - Bold values, color indicators
3. **Quick navigation** - Date hierarchies, filters
4. **Efficient search** - Multiple fields per model
5. **Batch operations** - Django's built-in actions
6. **Change history** - Automatic logging of changes
7. **Related object links** - Quick navigation between models

---

## Access Control

### Permissions:
- Add, Change, Delete, View permissions per model
- Django's built-in permission system
- Customizable per user/group

### Superuser Features:
- Full access to all models
- User management
- Group management
- Permission assignment

---

## Tips for Using the Admin

1. **Use date hierarchies** - Quickly jump to specific time periods
2. **Combine filters** - Stack multiple filters for precise results
3. **Search first** - Use search before scrolling through lists
4. **Inline editing** - Add circuits/photos without extra clicks
5. **Check statistics** - Dashboard and detail views show summaries
6. **Image previews** - Click to view full size
7. **Related links** - Navigate between rooms, progress, and circuits

---

## Admin URLs

- Main admin: `http://localhost:8000/admin/`
- Purchases: `http://localhost:8000/admin/renovation/purchase/`
- Purchase Categories: `http://localhost:8000/admin/renovation/purchasecategory/`
- Rooms: `http://localhost:8000/admin/renovation/room/`
- Room Progress: `http://localhost:8000/admin/renovation/roomprogress/`
- Progress Photos: `http://localhost:8000/admin/renovation/roomprogressphoto/`
- Work Sessions: `http://localhost:8000/admin/renovation/worksession/`
- Electrical Circuits: `http://localhost:8000/admin/renovation/electricalcircuit/`

---

## Customization

All admin features are defined in:
- [renovation/admin.py](renovation/admin.py) - Main admin configuration
- [renovation/context_processors.py](renovation/context_processors.py) - Dashboard statistics
- [renovation/templates/admin/index.html](renovation/templates/admin/index.html) - Dashboard template
- [config/urls.py](config/urls.py) - Admin headers and media URLs

To customize further, edit these files and restart the development server.

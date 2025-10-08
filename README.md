Hotel Reservation Management System (PyQt6)


Key Features

**Dashboard**:
* Displays summaries of key hotel metrics (reservations, available rooms, services, etc.)
* Includes a professional layout with styled summary cards and tables.


**Reservation Management**:
* Add, edit, and delete reservations
* Assign room types (Single, Double, Suite)
* Auto-calculates total price based on stay duration
* Validates input fields (names, phone numbers, date logic)
* Prevents overlapping bookings
* Data saved to a local SQLite database


**Service Assignment**:
* Assign additional services (e.g., cleaning, laundry) to reservations
* Automatically updates pricing
* Handles service deletion safely (linked reservations are updated accordingly)


**Form Validation**:
* Ensures correct data formats (e.g., no numbers in names, valid 11-digit phone numbers)
* Disallows invalid or overlapping booking dates


**Modern UI Design**:
* Fully styled using PyQt6 QSS (custom stylesheet)
* Professional color palette inspired by violet and lavender tones
* Clean layout with responsive table resizing

=========================================================================

---

**Installation & Setup**

**Create Virtual Environment**

```bash
python -m venv .venv
```
**Activate virtual environment**
For windows
```
.\venv\Scripts\activate
```
For macOS / Linux:
```
source venv/bin/activate
```
**Install Dependencies**
```
pip install -r requirements.txt
```
```
pip freeze > requirements.txt
```
**Run the Application**
```
python Main_app/main.py
```
or alternatively (if inside project root):
```
python -m Main_app.main
```


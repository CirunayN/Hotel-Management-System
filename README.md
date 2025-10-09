**Key Features:**


**-Dashboard**:
* Displays summaries of key hotel metrics (reservations, available rooms, services, etc.)
* Includes a professional layout with styled summary cards and tables.


**-Reservation Management**:
* Add, edit, and delete reservations
* Assign room types (Single, Double, Suite)
* Auto-calculates total price based on stay duration
* Validates input fields (names, phone numbers, date logic)
* Prevents overlapping bookings
* Data saved to a local SQLite database


**-Service Assignment**:
* Assign additional services (e.g., cleaning, laundry) to reservations
* Automatically updates pricing
* Handles service deletion safely (linked reservations are updated accordingly)


**-Form Validation**:
* Ensures correct data formats (e.g., no numbers in names, valid 11-digit phone numbers)
* Disallows invalid or overlapping booking dates


**-Modern UI Design**:
* Fully styled using PyQt6 QSS (custom stylesheet)
* Professional color palette inspired by violet and lavender tones
* Clean layout with responsive table resizing
  











**System Flow:**





 1. **Launch Application**  
   - The entry point is `main.py`.  
   - Initializes the main window and connects to the database.

2. **Main Window (`main_window.py`)**  
   - Acts as the container for all features (Dashboard, Reservation, Services).  
   - Uses a tab or stacked layout for smooth navigation.

3. **Core Database (`core/db.py`)**  
   - Connects to an SQLite database.  
   - Creates tables if they don’t exist (Reservations, Services, Assignments).  

4. **Data Models (`core/data.py`)**  
   - Defines Python dataclasses for type-safe, structured data:
     ```python
     @dataclass
     class Reservation:
         id: int | None
         name: str
         number: str
         room_type: str
         check_in: str
         check_out: str
         price: int
     ```

5. **Reservation Module**
   - **`view.py`** — Handles UI (form fields, buttons, tables)
   - **`repo.py`** — CRUD operations for reservation records
   - **`func.py`** — Business rules:
     - Prevent overlapping bookings  
     - Validate phone numbers and name format  
     - Auto-calculate room price based on duration and type  

6. **Dashboard Module**
   - Displays summarized data:
     - Total Reservations  
     - Revenue Estimation  
     - Most Booked Room Type  
   - Dynamically updates from database on refresh.

7. **Service Module**
   - Allows assigning extra services (e.g., cleaning, meals) to reservations.  
   - Can list, remove, or update service assignments.  

8. **Stylesheet System**
   - Centralized in `core/stylesheet.py`
   - Uses **Qt Stylesheets** to ensure a consistent look:
     - Buttons  
     - Tables  
     - Input fields  
     - Cards and group boxes  



**Installation & Setup:**


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
If you don’t have a requirements.txt file, generate one using:
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


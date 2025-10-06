# Movie Ticket Booking Backend 

A backend system for a **movie ticket booking application**, built with **Python**, **Django**, and **Django REST Framework (DRF)**.  
It provides a complete API for user management, movie listings, showtimes, and seat booking functionalities.

---

##  Features

###  Authentication
- Secure user signup and login using **JSON Web Tokens (JWT)**.

### Movie & Show Management
- API endpoints to list all movies and view showtimes for specific movies.  
- Protected **admin-only** endpoints for adding new movies and shows.

###  Booking System
- Book seats for a specific show.  
- View all personal bookings.  
- Cancel a booking.

### Business Logic
- Prevents **double-booking** of a single seat.  
- Prevents **overbooking** beyond the show’s total capacity.  
- Ensures users can only **cancel their own bookings**.
- **Prevents race conditions** during concurrent booking attempts using atomic database transactions.

### API Documentation
- Interactive API documentation available through **Swagger (OpenAPI)**.  
- Proper request/response schemas for all endpoints.

### Testing
- Unit tests for core booking and cancellation logic to ensure reliability.

---

## My Approach

-   **API Design**: I used Django REST Framework (DRF) to build a clean, well-structured, and scalable RESTful API. The logic is separated into Models (data structure), Serializers (data translation/validation), and Views (endpoints).

-   **Authentication**: I implemented JWT (JSON Web Token) authentication for a stateless and secure way to handle user sessions. All booking-related endpoints are protected (except All Movie List Endpoint) , requiring a valid token.

-   **Business Logic & Concurrency**: To handle the critical booking logic, I used atomic database transactions (`transaction.atomic`) with row-level locking (`select_for_update`). This is a robust solution that prevents race conditions, ensuring that two users cannot book the same seat simultaneously and that inventory is managed correctly.

-   **Testing**: I prioritized writing unit tests for the most critical parts of the application: the booking and cancellation logic. This ensures the core business rules are reliable and prevents regressions.

-   **Documentation**: I integrated Swagger UI to provide clear, interactive, and self-documenting API endpoints, making the API easy for developers to understand and consume.
---


## Tech Stack

- **Python**
- **Django** & **Django REST Framework**
- **Simple JWT** (for authentication)
- **drf-yasg** (for Swagger documentation)
- **SQLite** (for local database)

---

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1️. Clone the Repository

```bash
git clone https://github.com/Kunals990/movie-ticket-booking-django.git
cd movie-ticket-booking-django
```

### 2️. Create and Activate a Virtual Environment

```bash
# Create the virtual environment
python -m venv backend/venv

# Activate it (choose the correct command for your OS)

# On Windows:
backend\venv\Scripts\activate

# On macOS/Linux:
source backend/venv/bin/activate

```

### 3. Install Dependencies
Install all required packages from the requirements.txt file.
```bash
pip install -r backend/requirements.txt

```
### 4. Run Database Migrations
Apply the database schema to create all necessary tables.
```bash
python backend/manage.py migrate
python backend/manage.py makemigrations
```

### 5. Create a Superuser
This will create an admin account with staff privileges (needed for admin-only endpoints).
```bash
python backend/manage.py createsuperuser
```

### 6. Run Tests
The project includes unit tests for the core booking and cancellation logic.
```bash
# Make sure you are in the root project directory
python backend/manage.py test movie
```
If everything works correctly, you’ll see an “OK” message indicating all tests have passed .

### 6. Run the Application
Once setup is complete, start the Django development server:
```bash
python backend/manage.py runserver
```
The Django Backend will be available at : http://127.0.0.1:8000/


---

## API Documentation

Once the server is running, you can access the interactive documentation at:

**Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)



**Facilities Directory Website**

The Facilities Directory Website is a simple, fast, and secure web application that allows users to search for local services such as restaurants, shops, hospitals, and places to visit. It also includes an admin dashboard for managing facilities, protected by JWT-based authentication.

Overview

The Facilities Directory allows users to browse various categories of local services or search for specific facilities. The project includes a secure admin login system, which allows admins to add, edit, and remove facilities.

This project was developed using FastAPI for the backend, SQLAlchemy for database management, and Jinja2 templates for frontend rendering. JWT-based authentication secures the admin login.

Features
* Search Functionality: Users can search for facilities by name and browse by category (restaurants, shops, hospitals, places to visit).
* Admin Authentication: Secure JWT-based admin login system.
* Admin Dashboard: Allows admins to add, edit, and delete facility data.
* Responsive Design: Clean and modern UI with mobile responsiveness, built using Bootstrap.
* SQLAlchemy ORM: Manage facilities and users in the database.

Tech Stack
* Backend: FastAPI (Python)
* Frontend: Jinja2 templates, HTML, CSS, Bootstrap
* Database: SQLAlchemy (with SQLite or PostgreSQL)
* Authentication: JWT-based using oauth2_scheme
* Static Assets: Bootstrap CSS, Custom Stylesheets
* Middleware: CORS for handling requests

Installation
To get the project running locally, follow these steps:

Prerequisites
* Python 3.8+
* Pip (Python package manager)


Set up a virtual environment (optional but recommended):
* bash
Copy code: python3 -m venv env
            source env/bin/activate  # On Windows use `env\Scripts\activate`

Install dependencies:
bash
Copy code
pip install -r requirements.txt

Set up the database:

Initialize the database using SQLAlchemy with FastAPI’s dependency injection:
bash
Copy code
python -m uvicorn main:app --reload
This will create the necessary tables and relationships in your database.
Set environment variables (for sensitive data like SECRET_KEY):

Create a .env file in the root directory and add:
makefile
Copy code
SECRET_KEY=your-secret-key

Running the Project
To start the FastAPI development server:
bash
Copy code
or fastapi dev main.py
uvicorn main:app --reload
By default, the app will run at http://127.0.0.1:8000/. You can access the following routes:
* Homepage: http://127.0.0.1:8000/
* Admin Login: http://127.0.0.1:8000/admin_login
* Search: http://127.0.0.1:8000/search?query=yoursearchterm
* Admin Dashboard: http://127.0.0.1:8000/admin (Requires admin login)

Usage
* Admin Login
* Admins can log in to manage the facilities. The login form is located at:

arduino
Copy code
http://127.0.0.1:8000/admin_login
Enter your admin credentials.
Upon successful login, you will be redirected to the admin dashboard where you can add, edit, or remove facilities.
Search for Facilities
Users can search for facilities by name or browse by category (restaurants, shops, hospitals, places to visit). Simply use the search bar on the homepage or navigate to the desired category.

Admin Authorization
To protect sensitive admin routes, JWT-based authentication is implemented. Admins need a valid JWT token, which is obtained by logging in via the /token endpoint.

Challenges and Future Work
Challenges
* Search Suggestions: We attempted to implement dynamic search suggestions but faced issues with JavaScript integration and opted to focus on basic search functionality.
* Admin Authentication: Securing the admin dashboard using JWT tokens was initially challenging, but we managed to implement it using OAuth2PasswordBearer and FastAPI's built-in JWT library.
* Admin Panel: Login was successfull implemented but the admin panel has not been fully set up yet.
* Scope Reduction: Initially, we had planned for a more interactive website, but due to team changes, we scaled the project down to focus on core features.

Future Work
* Search Suggestions: Implementing JavaScript to provide real-time suggestions as users type their search queries.
* User Reviews: Allow users to leave reviews and ratings for facilities.
* API Integration: Use external APIs (e.g., Google Places) to keep facility data up to date.
* Additional Categories: Expand categories and subcategories for better facility organization.

Contributing
@zoumanzouman
@harshdixit05
@SiyaGirisaballa
@mitanshaggarwal

Fork the repository.
* Create a new feature branch (git checkout -b feature/your-feature).
* Make changes and commit (git commit -m 'Add your feature').
* Push to your branch (git push origin feature/your-feature).
* Open a Pull Request.

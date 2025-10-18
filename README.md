Django Expense Tracker
A simple Django web application for tracking personal expenses with user authentication.

** Features **

User registration and authentication

Create, read, update, and delete expenses

Filter expenses by category and date range

Monthly expense summary

Responsive design with minimal CSS

Form validation and user feedback messages

Secure user sessions with proper logout functionality

** Setup Instructions **
Prerequisites
Python 3.8+

pip (Python package manager)

** Installation **
Download and extract the project files

Navigate to the project directory

bash
cd expense_tracker
Create a virtual environment (recommended)

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Run migrations

bash
python manage.py makemigrations
python manage.py migrate
Create a superuser (optional, for admin access)

bash
python manage.py createsuperuser
Follow the prompts to create an admin account.

Run the development server

bash
python manage.py runserver
Access the application

Main application: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/ (if superuser created)

** Steps to Test the Application **
1. Register a New Account
Go to http://127.0.0.1:8000/register

Fill in the registration form with:

Username

Email

Password

Confirm Password

Click "Register"

You should see a success message and be redirected to the login page

2. Login
Go to http://127.0.0.1:8000/login

Enter your username and password

Click "Login"

You should be redirected to the expenses list page

3. Add Expenses
Click "Add New Expense" button

Fill out the form:

Title: Enter a description (e.g., "Groceries")

Amount: Enter a positive number (e.g., 50.00)

Category: Select from dropdown (e.g., "Food")

Date: Select a date (defaults to today)

Click "Create Expense"

You should see a success message and the new expense in the list

Verify: Check that the monthly total updates with the new amount

4. View and Filter Expenses
All expenses are displayed in a table format

Use the filter section to:

Filter by category using the dropdown

Filter by date range using start and end dates

Click "Apply Filters" to see filtered results

Click "Clear Filters" to reset

5. Edit an Expense
Click the "Edit" button next to any expense

Modify any field in the form

Click "Update Expense"

You should see a success message and the updated expense

6. Delete an Expense
Click the "Delete" button next to any expense

Confirm deletion in the confirmation page

Click "Yes, Delete"

You should see a success message and the expense removed from the list

Verify: Check that the monthly total updates after deletion

7. Logout
Click the "Logout" link in the navigation

You should be logged out and redirected to the login page

A confirmation message "You have been successfully logged out" should appear

8. Test Monthly Total
Add multiple expenses with different dates in the current month

Verify that the "Total this month" amount correctly sums all expenses

Add expenses from previous months to ensure they're not included in the current month total

** Short Explanation of the Approach **
Architecture
Backend: Django with SQLite database

Authentication: Django's built-in authentication system with custom views for registration

Frontend: Django templates with minimal CSS for clean, responsive design

Security: User authentication required for all operations, users can only access their own data

Key Components
Models:

Expense model with fields for title, amount, category, date, and user relationship

User model (Django's built-in with registration extension)

Views:

Class-based views for all CRUD operations

Custom authentication mixins to ensure security

Filtering logic for category and date-based queries

Monthly total calculation using Django's aggregation

Templates:

Base template with consistent navigation and styling

Individual templates for each view with form handling

Message framework integration for user feedback

Forms:

ModelForm for expense creation/editing with validation

Custom registration form with password confirmation

** Security Features **
CSRF protection on all forms

LoginRequiredMixin for protected views

User-specific data filtering (users only see their own expenses)

Secure password handling with validation

Proper session management with logout redirect

** Bonus Features Implemented **
User registration system

Expense filtering by category and date range

Monthly total calculation and display

Responsive design with clean CSS

Form validation and user feedback messages
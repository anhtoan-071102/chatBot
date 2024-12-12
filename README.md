# ChatBot Backend Project

This is the backend for a ChatBot application built using Django. The backend supports features such as user registration, login, AI-based chat interaction, chat history, and the ability to view and delete individual chat sessions.

## Technologies Used

- **Django**: A high-level Python web framework for rapid development.
- **Django REST Framework**: A powerful toolkit for building Web APIs in Django.
- **Django Admin**: Used for managing users and chat data via the admin interface.
- **Django Authentication**: For managing user authentication, registration, and login.
- **MySQL**: can be replaced with others.

## Features

1. **User Registration**: Users can create an account by providing a username, email, and password.
2. **User Login**: Registered users can log in to access chat functionality.
3. **AI Chat**: Users can chat with an AI chatbot that responds to their questions.
4. **View Chat History**: Users can view a list of their previous chat sessions.
5. **View Chat Details**: Users can view the details of a specific chat session, including each message exchanged.
6. **Delete Chat**: Users can delete individual chat sessions from their history.

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 3.x or higher
- Django REST Framework
- MySQL (or other databases if configured)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/chatbot-backend.git
   cd chatbot-backend
Create a virtual environment (optional but recommended):

```bash
Sao chép mã
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

```bash
Sao chép mã
pip install -r requirements.txt
Migrate the database:

```bash
Sao chép mã
python manage.py migrate
Create a superuser for admin access:

```bash
Sao chép mã
python manage.py createsuperuser
Run the development server:

```bash
Sao chép mã
python manage.py runserver
The application will be running on http://127.0.0.1:8000/.

/api/register/
Method: POST
/api/login/
Method: POST
URL: /api/chat/history/
Method: GET
URL: /api/chat/{chat_id}/
Method: GET
URL: /api/chat/{chat_id}/delete/
Method: DELETE

Admin Panel
You can access the Django admin panel at /admin/ and use the superuser credentials to log in and manage users and chats.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Thanks to the Django and Django REST Framework communities for their excellent documentation and support.

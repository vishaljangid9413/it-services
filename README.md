# IT Services

The IT Services is a web application built with Django and Django REST Framework to manage Services and Subscription orders.

## Functionality

### Users App

- **User Registration and Authentication:** Allows users to register with their name, email, and mobile number. Supports user authentication with mobile number and password.
- **Password Management:** Provides functionality for users to reset their passwords if forgotten.
- **Logout:** Enables users to log out securely.


## Installation and Setup

1. Clone the repository from GitHub:
    ```bash
    git clone https://github.com/vishaljangid9413/it-services.git
    ```

2. Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    
3. Run the Django migrations to set up the database:
    ```bash
    python manage.py makemigrations
    ```

4. Run the Django migrations to set up the database:
    ```bash
    python manage.py migrate
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

6. Create a Superuser Account to access admin panel:
    ```bash
    python manage.py createsuperuser
    ```

7. Access the application in your web browser at [http://localhost:8000](http://localhost:8000).

## Dependencies

- **Django:** Web framework for building web applications in Python.
- **Django REST Framework:** Toolkit for building Web APIs in Django.
- **Django Rest Allauth Token:** Implements Allauth Token functionality in Python.

## Advanced Code Practices

- **Custom User Model:** Uses a custom user model to extend Django's built-in user model with additional fields.
- **Serializer Usage:** Utilizes Django REST Framework serializers for data serialization and deserialization.
- **Signals:** Uses Django signals to trigger actions upon certain database events, such as saving or deleting objects.
- **ViewSets:** Implements Django REST Framework viewsets for CRUD operations on database models.
- **Token Authentication:** Implements token-based authentication for user login and session management.

## Robustness Checks

- **Input Validation:** Validates user input using Django model validators and form validation.
- **Error Handling:** Implements error handling and returns meaningful error messages to users.
- **Data Integrity:** Ensures data integrity by performing data validation and enforcing constraints at the model level.
- **Security Measures:** Implements security measures such as password hashing and token-based authentication to protect user data.

# Authentication System with Django REST Framework and JWT
This project implements a user authentication system using Django REST Framework (DRF) and JSON Web Tokens (JWT). Below are the key features and steps to follow:

## Features:
1. **User Registration**: Allows users to register with email, name, date of birth, and password.
2. **User Login**: Authenticates users using email and password.
3. **User Profile Management**: Enables users to view and update their profile information.
4. **Password Change**: Allows users to change their password after login.
5. **Password Reset**: Provides functionality to reset the password via email with a secure token.
6. **JWT Authentication**: Secures API endpoints using JWT for token-based authentication.

## Steps to Build the System:
1. **Install Dependencies**:
    - Install Django and Django REST Framework.
    - Install `djangorestframework-simplejwt` for JWT authentication.

2. **Setup Models**:
    - Create a custom `User` model in `acounts/models.py` with fields like `email`, `name`, `dob`, etc.

3. **Create Serializers**:
    - Use the serializers provided in `serializers.py` to handle data validation and transformation.

4. **Setup Views**:
    - Implement views for registration, login, profile management, password change, and password reset.

5. **Configure URLs**:
    - Add routes for authentication endpoints in `urls.py`.

6. **JWT Integration**:
    - Configure JWT settings in `settings.py` and use `SimpleJWT` for token generation and verification.

7. **Email Utility**:
    - Use the `EmailUtils` class to send password reset emails with a secure link.

8. **Testing**:
    - Test all endpoints using tools like Postman or Django's test framework.

## Example Endpoints:
- **POST /api/register/**: User registration.
- **POST /api/login/**: User login and JWT token generation.
- **GET /api/profile/**: Retrieve user profile (requires authentication).
- **PUT /api/profile/**: Update user profile (requires authentication).
- **POST /api/change-password/**: Change password (requires authentication).
- **POST /api/reset-password/**: Request password reset email.
- **POST /api/reset-password-confirm/{uid}/{token}/**: Reset password using token.

## Notes:
- Ensure proper validation and error handling in serializers.
- Use secure practices for storing and handling passwords.
- Customize the email templates for password reset links.

Follow the code structure and instructions to build a robust authentication system.


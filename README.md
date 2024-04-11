# UserAuth

This is a RESTful API for user authentication built using Django and Django REST Framework.

## Features

- User registration with email verification
- User login with OTP
- Forgot password functionality with OTP
- Reset password functionality

## Endpoints

### User Registration

- **URL:** `/register`
- **Method:** POST
- **Description:** Registers a new user.
- **Request Body:** JSON object with user details including `first_name`, `last_name`, `email`, `username`, and `password`.
- **Response:** JSON object with success message and user details if registration is successful, or error message if validation fails.

### Email Verification

- **URL:** `/email-verification`
- **Method:** POST
- **Description:** Verifies user's email using OTP.
- **Request Body:** JSON object with `username` or `email` and `otp` fields.
- **Response:** JSON object with success message if verification is successful, or error message if validation fails.

### User Login

- **URL:** `/login`
- **Method:** POST
- **Description:** Authenticates the user based on email and OTP.
- **Request Body:** JSON object with `username` or `email` and `otp` fields.
- **Response:** JSON object with user details and access tokens if authentication is successful, or error message if authentication fails.

### Forgot Password

- **URL:** `/forgot-password`
- **Method:** POST
- **Description:** Sends OTP to user's email for password reset.
- **Request Body:** JSON object with `username` or `email` field.
- **Response:** JSON object with success message if OTP is sent successfully, or error message if validation fails.

### Reset Password

- **URL:** `/reset-password`
- **Method:** POST
- **Description:** Resets user's password using OTP.
- **Request Body:** JSON object with `username` or `email`, `otp`, and `password` fields.
- **Response:** JSON object with success message if password is reset successfully, or error message if validation fails.

## Getting Started

To get started with InovaTech, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/Riosumit/UserAuth.git

2. Navigate to the project directory:
   ```bash
   cd UserAuth

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the development server:
   ```bash
   python manage.py runserver
   
5. Access the api's locally at http://localhost:8000/

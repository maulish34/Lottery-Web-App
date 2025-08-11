# Lottery Web App

This is a secure lottery web application built using Python Flask and a SQL database. The app allows users to register, authenticate, and participate in a lottery game, with a strong emphasis on cybersecurity best practices. The project demonstrates how to build a secure web application by integrating encryption, multi-factor authentication, secure data validation, error handling, and secure data transmission.

## About the Lottery App

Users can register with their details, set up two-factor authentication (2FA), and log in to play the lottery. Each user can submit their own lottery draw or use a cryptographically secure random generator for a "lucky dip." Admin users have additional privileges, such as managing users and viewing activity logs. The app enforces strict validation on all user inputs and provides clear feedback for errors. All sensitive operations and data are logged for auditing purposes.

## Security Highlights

- **Input Validation:** All registration and login fields are validated using regular expressions and custom logic to prevent invalid or malicious input. This includes strict checks on email, names, phone numbers, passwords, date of birth, and postcode.
- **Password Security:** Passwords are hashed and salted before storage, ensuring that even if the database is compromised, raw passwords are not exposed.
- **Two-Factor Authentication (2FA):** After registration, users must set up 2FA using a QR code and an authenticator app, adding an extra layer of security beyond just passwords.
- **Role-Based Access Control:** The app restricts access to pages and actions based on user roles (anonymous, user, admin), ensuring users can only access what they're authorized for.
- **Logging and Auditing:** All critical actions (registration, login, logout, failed attempts, unauthorized access) are logged with timestamps and IP addresses, supporting monitoring and forensic analysis.
- **Encryption:** Lottery draw numbers are encrypted (using symmetric or asymmetric encryption) before being stored in the database, protecting sensitive game data at rest.
- **Error Handling:** Custom error pages are provided for common HTTP errors, each with explanations and links to external resources for further information.
- **Secure Data Transmission:** The app enforces HTTPS using a self-signed certificate and sets strict security headers to protect against common web vulnerabilities.
- **Environment Configuration:** All sensitive configuration data is stored in environment variables, keeping secrets out of the codebase.
- **Programming Best Practices:** The codebase is well-structured, commented, and avoids redundancy, making it maintainable and secure.

These security measures reflect real-world practices for protecting user data, preventing unauthorized access, and ensuring the integrity and confidentiality of sensitive information in web applications.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lottery-web-app.git
cd lottery-web-app
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with the following variables (these will **not** be present in the repository):

```
SECRET_KEY = <your-secret-key>
SQLALCHEMY_DATABASE_URI = sqlite:///lottery.db
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
RECAPTCHA_PUBLIC_KEY = <your-recaptcha-public-key>
RECAPTCHA_PRIVATE_KEY = <your-recaptcha-private-key>
```

Replace `<your-secret-key>`, `<your-recaptcha-public-key>`, and `<your-recaptcha-private-key>` with your own secure values.

### 3. Install Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Flask Application

To run the app with HTTPS (using a self-signed certificate):

```bash
flask run --cert=cert.pem --key=key.pem
```

Make sure you have generated `cert.pem` and `key.pem` for local HTTPS. You can generate them using OpenSSL:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

The app will be available at `https://localhost:5000`.

## License

This project was created for educational purposes. Credits for the boilerplate code go to Newcastle University.

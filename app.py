from flask import Flask, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to validate user credentials
def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

# Route to serve the login page
@app.route('/')
def login_page():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Page</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); width: 300px; text-align: center; }
            .login-container h2 { margin-bottom: 20px; color: #333; }
            .login-container input[type="text"], .login-container input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
            .login-container input[type="submit"] { width: 100%; padding: 10px; background-color: #28a745; border: none; border-radius: 4px; color: #fff; font-size: 16px; cursor: pointer; }
            .login-container input[type="submit"]:hover { background-color: #218838; }
            .login-container .error { color: red; margin-top: 10px; }
            .login-container a { display: block; margin-top: 10px; color: #007bff; text-decoration: none; }
            .login-container a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>Login</h2>
            <form id="loginForm" action="/login" method="POST">
                <input type="text" id="username" name="username" placeholder="Username" required>
                <input type="password" id="password" name="password" placeholder="Password" required>
                <input type="submit" value="Login">
            </form>
            <div id="error-message" class="error"></div>
            <a href="/register">Don't have an account? Register here.</a>
        </div>
    </body>
    </html>
    '''

# Route to serve the register page
@app.route('/register')
def register_page():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register Page</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .register-container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); width: 300px; text-align: center; }
            .register-container h2 { margin-bottom: 20px; color: #333; }
            .register-container input[type="text"], .register-container input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
            .register-container input[type="submit"] { width: 100%; padding: 10px; background-color: #28a745; border: none; border-radius: 4px; color: #fff; font-size: 16px; cursor: pointer; }
            .register-container input[type="submit"]:hover { background-color: #218838; }
            .register-container .error { color: red; margin-top: 10px; }
            .register-container a { display: block; margin-top: 10px; color: #007bff; text-decoration: none; }
            .register-container a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="register-container">
            <h2>Register</h2>
            <form id="registerForm" action="/register" method="POST">
                <input type="text" id="username" name="username" placeholder="Username" required>
                <input type="password" id="password" name="password" placeholder="Password" required>
                <input type="submit" value="Register">
            </form>
            <div id="error-message" class="error"></div>
            <a href="/">Already have an account? Login here.</a>
        </div>
    </body>
    </html>
    '''

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Route to handle register form submission
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if register_user(username, password):
        return jsonify({'message': 'Registration successful! Please login.'})
    else:
        return jsonify({'message': 'Username already exists!'}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
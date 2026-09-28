from flask import Flask, request
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    if count == 0:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("anjali", "12345")
        )

        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SQL Injection Lab</title>

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }

            body {
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .container {
                background: white;
                width: 420px;
                padding: 40px;
                border-radius: 18px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.25);
                text-align: center;
            }

            h1 {
                font-size: 30px;
                color: #333;
                margin-bottom: 15px;
            }

            p {
                font-size: 17px;
                color: #666;
                margin-bottom: 25px;
                line-height: 1.5;
            }

            .btn {
                display: inline-block;
                background: #667eea;
                color: white;
                text-decoration: none;
                padding: 13px 28px;
                border-radius: 8px;
                font-size: 17px;
                transition: 0.3s;
            }

            .btn:hover {
                background: #5568d9;
                transform: translateY(-2px);
            }

            .warning {
                margin-top: 25px;
                padding: 12px;
                background: #fff3cd;
                border-radius: 8px;
                color: #856404;
                font-size: 14px;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>🔐 SQL Injection Lab</h1>

            <p>
                Secure Coding Practices<br>
                Web Application Security Demonstration
            </p>

            <a href="/login" class="btn">
                Go to Login
            </a>

            <div class="warning">
                ⚠️ Educational demonstration running locally
            </div>

        </div>

    </body>
    </html>
    """


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return """
        <!DOCTYPE html>
        <html>

        <head>
            <title>Login - SQL Injection Lab</title>

            <style>

                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                }

                body {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    min-height: 100vh;

                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .login-card {
                    background: white;
                    width: 430px;
                    padding: 42px;
                    border-radius: 18px;

                    box-shadow:
                        0 15px 40px rgba(0,0,0,0.25);
                }

                .icon {
                    text-align: center;
                    font-size: 48px;
                    margin-bottom: 10px;
                }

                h2 {
                    text-align: center;
                    font-size: 30px;
                    color: #333;
                    margin-bottom: 8px;
                }

                .subtitle {
                    text-align: center;
                    color: #777;
                    font-size: 16px;
                    margin-bottom: 30px;
                }

                label {
                    display: block;
                    font-size: 17px;
                    font-weight: bold;
                    color: #444;
                    margin-bottom: 8px;
                }

                input {
                    width: 100%;
                    padding: 13px;

                    border: 1px solid #ccc;
                    border-radius: 8px;

                    font-size: 16px;

                    margin-bottom: 22px;

                    outline: none;
                }

                input:focus {
                    border-color: #667eea;
                    box-shadow: 0 0 5px rgba(102,126,234,0.4);
                }

                button {
                    width: 100%;
                    padding: 14px;

                    background: #667eea;
                    color: white;

                    border: none;
                    border-radius: 8px;

                    font-size: 18px;
                    font-weight: bold;

                    cursor: pointer;

                    transition: 0.3s;
                }

                button:hover {
                    background: #5568d9;
                    transform: translateY(-2px);
                }

                .info {
                    margin-top: 25px;
                    padding: 13px;

                    background: #f3f4ff;
                    border-left: 4px solid #667eea;

                    color: #555;
                    font-size: 14px;
                    line-height: 1.5;

                    border-radius: 5px;
                }

                .back {
                    display: block;
                    text-align: center;

                    margin-top: 20px;

                    color: #667eea;
                    text-decoration: none;

                    font-size: 15px;
                }

                .back:hover {
                    text-decoration: underline;
                }

            </style>
        </head>

        <body>

            <div class="login-card">

                <div class="icon">🔐</div>

                <h2>Welcome Back</h2>

                <div class="subtitle">
                    SQL Injection Security Lab
                </div>

                <form method="POST">

                    <label>Username</label>

                    <input
                        type="text"
                        name="username"
                        placeholder="Enter username"
                        required
                    >

                    <label>Password</label>

                    <input
                        type="password"
                        name="password"
                        placeholder="Enter password"
                        required
                    >

                    <button type="submit">
                        Login
                    </button>

                </form>

                <div class="info">
                    🧪 This application is being used for
                    controlled security testing and demonstration.
                </div>

                <a href="/" class="back">
                    ← Back to Home
                </a>

            </div>

        </body>

        </html>
        """

    username = request.form["username"]
    password = request.form["password"]

    # INTENTIONALLY VULNERABLE
    query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        AND password = '{password}'
    """

    print("SQL Query:", query)

    conn = get_db()

    try:
        user = conn.execute(query).fetchone()

    except Exception as e:
        conn.close()
        return f"Database Error: {e}", 500

    conn.close()

    if user:
        return f"""
        <div style="
            font-family: Arial;
            text-align: center;
            margin-top: 100px;
        ">

            <h1 style="color: #28a745;">
                ✅ Login Successful
            </h1>

            <h2>
                Welcome, {user['username']}!
            </h2>

            <br>

            <a href="/login">
                Back to Login
            </a>

        </div>
        """

    return """
    <div style="
        font-family: Arial;
        text-align: center;
        margin-top: 100px;
    ">

        <h1 style="color: #dc3545;">
            ❌ Invalid Credentials
        </h1>

        <br>

        <a href="/login">
            Try Again
        </a>

    </div>
    """, 401


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
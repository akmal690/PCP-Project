import smtplib
import random
import sqlite3
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Database Setup ---
def create_table():
    conn = sqlite3.connect('otp_database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS otp_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            otp TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            expires_at TIMESTAMP NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def store_otp(email, otp, expires_in_minutes=5):
    created_at = datetime.now()
    expires_at = created_at + timedelta(minutes=expires_in_minutes)
    conn = sqlite3.connect('otp_database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO otp_codes (email, otp, created_at, expires_at)
        VALUES (?, ?, ?, ?)
    ''', (email, otp, created_at, expires_at))
    conn.commit()
    conn.close()

# --- OTP Generation ---
def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

# --- Email Sending ---
def send_otp_email(sender_email, sender_password, recipient_email, otp):
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

# --- Main Workflow ---
if _name_== "_main_":
    create_table()  # Ensure the table exists

    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # Use App Password if 2FA enabled
    recipient_email = "recipient@example.com"

    otp = generate_otp()
    store_otp(recipient_email, otp)  # Store OTP in database
    send_otp_email(sender_email, sender_password, recipient_email, otp)
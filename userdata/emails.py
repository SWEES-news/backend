import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import userdata.db_connect as dbc
from datetime import datetime
from zoneinfo import ZoneInfo
import dateutil.parser
import json
load_dotenv()  # This will load environment variables from a .env file

COLLECTION = "verification_codes"
TIMESTAMP_FIELD = 'timestamp'
TIMEZONE = ZoneInfo('America/New_York')
TIMEOUT = 10 * 60  # 10 minutes


def get_time_as_string():
    current_time = datetime.now(TIMEZONE)
    return current_time.strftime("%Y-%m-%d %H:%M:%S %z")


def compare_times(time_str1, time_str2):
    datetime1 = dateutil.parser.parse(time_str1)
    datetime2 = dateutil.parser.parse(time_str2)
    timedelta = datetime1 - datetime2
    print(timedelta.total_seconds())
    return abs(timedelta.total_seconds()) < TIMEOUT


def generate_verification_code():
    return f"{random.randint(100000, 999999)}"


def send_verification_email(to_address):
    EMAIL = os.getenv('EMAIL_EMAIL')
    PASSWORD = os.getenv('EMAIL_PASSWORD')

    verification_code = generate_verification_code()

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    connected = False
    try:
        server.login(EMAIL, PASSWORD)
        connected = True

        if connected:
            from_address = EMAIL
            subject = "Email Verification"
            body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f6f6f6;
                    }}
                    .container {{
                        width: 90%;
                        margin: auto;
                        background-color: #F2F2F2;
                        padding: 20px;
                        border-radius: 4px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
                        border: 2px solid black;
                    }}
                    .code {{
                        font-size: 26px;
                        font-weight: bold;
                        color: #2a7ae2;
                        background-color: #eeeeee;
                        margin: 0 auto;
                        padding: 20px;
                        border-radius: 4px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <p>Dear User,</p>

                    <p>Thank you for signing up.</p>

                    <p>Your verification code is: <div class="code">{verification_code}</div></p>

                    <p>Please enter this code to complete your registration.</p>

                    <p>Best regards,<br><strong>The SWEES</strong></p>
                </div>
            </body>
            </html>
            """
            msg = MIMEMultipart()
            msg['From'] = from_address
            msg['To'] = to_address
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            server.send_message(msg)
            print("Verification email sent.")

            dbc.connect_db()
            time = get_time_as_string()
            filter_dict = {"email": to_address}
            update_dict = {
                "email": to_address,
                "code": verification_code,
                "is_verified": False,
                TIMESTAMP_FIELD: time
            }
            submission_result = dbc.update_or_insert_one(COLLECTION, filter_dict, update_dict)

            # Check the result of the operation and retrieve the ID if needed
            if submission_result.upserted_id is not None:
                submission_id = submission_result.upserted_id
                print(f"Inserted new document with submission ID: {submission_id}")
            else:
                print("Updated existing document.")
            
            print(f"Verification code: {verification_code}")
            res = dbc.fetch_all(COLLECTION)
            pretty_json = json.dumps(res, indent=4)
            print(pretty_json)
    except Exception as e:
        print("Failed to connect or send email:", e)
    finally:
        if connected:
            server.quit()


def verify_email(email, code):
    dbc.connect_db()
    verification = dbc.fetch_one(COLLECTION, {"email": email})
    print(verification)
    if verification and 'code' in verification:
        if verification['code'] == code:
            db_timestamp = verification[TIMESTAMP_FIELD]
            current_time = get_time_as_string()
            if compare_times(current_time, db_timestamp):
                dbc.update_doc(COLLECTION, {"email": email}, {"is_verified": True})
                return True
            else:
                dbc.del_one(COLLECTION, {"email": email})
                print("Verification code expired")
        print("Verification code does not match")
        print(f"Expected: {verification['code']}, Received: {code}")
        return False
    print("No verification code found")
    return False


def check_email_verification(email):
    dbc.connect_db()
    verification = dbc.fetch_one(COLLECTION, {"email": email})
    if verification and 'is_verified' in verification:
        return verification['is_verified']
    return False

"""
Handles sending OTP via AWS SES
"""

import boto3
from config import AWS_REGION, SES_SENDER_EMAIL

def send_otp_email(to_email: str, otp: str):
    client = boto3.client("ses", region_name=AWS_REGION)

    subject = "Your NareshKart OTP Code"
    body = f"""
Hello,

Your OTP for NareshKart registration is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this, ignore this email.

Regards,
NareshKart Team
"""

    client.send_email(
        Source=SES_SENDER_EMAIL,
        Destination={"ToAddresses": [to_email]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
        },
    )

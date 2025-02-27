from email.mime.application import MIMEApplication
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


def send_email(sender_email, password, recipient, link):
    """Function to send an HTML email with a processed data download link"""

    html_body = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f9f9f9;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            .content {{
                font-size: 16px;
            }}
            .link {{
                display: inline-block;
                padding: 10px 15px;
                margin-top: 10px;
                color: white solid;
                background-color: #0056b3;
                text-decoration: none;
                border-radius: 5px;
            }}
            .link:hover {{
                background-color: #004494;
            }}
            .signature {{
                margin-top: 30px;
                font-size: 14px;
                color: #555;
            }}
            .contact {{
                margin-top: 10px;
                font-size: 14px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <p class="content">Dear Researcher,</p>
            <p class="content">
                I hope you're doing well.<br>
                Your data has been successfully processed, and the output is now available for download. You can access the results using the link below:
            </p>
            <p>
                <a href="{link}" class="link"><b>Download Processed Data</b></a>
            </p>
            <p class="content">
                If you have any questions or require further adjustments, please feel free to reach out. We appreciate your contributions to data-driven research and look forward to supporting your work.
            </p>
            <p class="signature">
                Best regards,<br>
                <strong>Miel Hostens</strong><br>
                Robert and Anne Everett Endowed Associate Professor of Digital Dairy Management and Data Analytics<br>
                Cornell Atkinson Center for Sustainability Faculty Fellow<br>
                Cornell Institute for Digital Agriculture Faculty Fellow
            </p>
            <p class="contact">
                <strong>Department of Animal Science</strong><br>
                273 Morrison Hall, Ithaca, NY 14853<br><br>
                📞 Cell US: (607) 663-0808 | Office US: (607) 255-7441 | Cell EU: +32-478-593703<br>
                📧 <a href="mailto:miel.hostens@cornell.edu">miel.hostens@cornell.edu</a><br>
                🌐 <a href="https://bovi-analytics.com" target="_blank">bovi-analytics.com</a> | <a href="https://cals.cornell.edu" target="_blank">cals.cornell.edu</a>
            </p>
        </div>
    </body>
    </html>
    """

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_email, password)
            receiver_email = recipient.strip()  # Remove whitespace

            subject = "Processed Data Download Link - Bovi-Analytics Lab"
            print(f"Sending to: {receiver_email}")

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            message.attach(MIMEText(html_body, "html"))

            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"--- Sent email to {receiver_email} ---")
        except Exception as e:
            print(f"Error sending email: {e}")
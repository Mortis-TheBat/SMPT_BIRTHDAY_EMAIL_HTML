import csv
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def send_birthday_email(recipient_name, recipient_email, image_filename):
    # Email configuration
    sender_email = 'birthday@email.com'
    sender_password = 'your_password'
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    # Compose the email
    message = MIMEMultipart('related')
    message['Subject'] = 'Happy Birthday!'
    message['From'] = sender_email
    message['To'] = recipient_email

    # Load the HTML template
    with open('message.html', 'r') as file:
        html_template = file.read()

    # Replace placeholders with recipient-specific information
    html_content = html_template.replace('{{name}}', recipient_name)
    html_content = html_content.replace('{{image}}', image_filename)

    # Attach HTML content to the email
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    # Attach the image
    with open(image_filename, 'rb') as file:
        image_data = file.read()
        image = MIMEImage(image_data)
        image.add_header('Content-Disposition', 'attachment', filename=image_filename)
        image.add_header('Content-ID', '<{}>'.format(image_filename))
        message.attach(image)

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

# File path of the CSV data file
csv_file_path = 'data.csv'

# Current date
current_date = datetime.date.today()

# Read the CSV file
data = read_csv(csv_file_path)

# Iterate over the data and send birthday emails
for row in data:
    dob = datetime.datetime.strptime(row['DOB'], '%d/%m/%Y').date()
    if dob.month == current_date.month and dob.day == current_date.day:
        print ("Match found for", row['Name'])
        recipient_name = row['Name']
        recipient_email = row['Email']
        image_filename = row['ImageFilename']  # Provide the actual filename or path to add in
        send_birthday_email(recipient_name, recipient_email, image_filename)

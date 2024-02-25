#!/usr/bin/env python3
import sys
import re
import os
import email
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Load environment variables
load_dotenv()

# Use the loaded environment variable for Firebase authentication
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()


# Function to parse email and extract data
def parse_email(email_content):
    # Simple parsing for demonstration; extract subject
    subject_match = re.search(r"^Subject: (.+)$", email_content, re.MULTILINE)
    if subject_match:
        subject = subject_match.group(1)
        datestr = subject.split(" ")[-1]
    else:
        datestr= "Unknown Date"

    return datestr

# Parse the email to extract body
def parse_email_for_body(email_content):
    msg = email.message_from_string(email_content)
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload()
    else:
        return msg.get_payload()


# Function to insert data into Firestore
def insert_into_firestore(datestr, body):
    # Reference to your collection
    collection_ref = db.collection(u'thought-of-the-days')
    # Data to insert
    doc_data = {
        u'date': datestr,
        u'totd': body,
        u'processed': firestore.SERVER_TIMESTAMP
    }
    # Add a new doc in collection
    collection_ref.add(doc_data)

# Main script logic
if __name__ == "__main__":
    # Read email content from stdin
    email_content = sys.stdin.read()
    
    # Parse the email to extract information
    datestr = parse_email(email_content)
    body = parse_email_for_body(email_content)

    # Insert extracted information into Firestore
    insert_into_firestore(datestr, body)

    print("Email processed and data inserted into Firestore.")

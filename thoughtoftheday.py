#!/usr/bin/env python3
import sys
import re
from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()

# Function to parse email and extract data
def parse_email(email_content):
    # Simple parsing for demonstration; extract subject
    subject_match = re.search(r"^Subject: (.+)$", email_content, re.MULTILINE)
    if subject_match:
        subject = subject_match.group(1)
    else:
        subject = "Unknown Subject"
    return subject

# Function to insert data into Firestore
def insert_into_firestore(subject):
    # Reference to your collection
    collection_ref = db.collection(u'emails')
    # Data to insert
    doc_data = {
        u'subject': subject,
        u'processed': firestore.SERVER_TIMESTAMP
    }
    # Add a new doc in collection
    collection_ref.add(doc_data)

# Main script logic
if __name__ == "__main__":
    # Read email content from stdin
    email_content = sys.stdin.read()
    
    # Parse the email to extract information
    subject = parse_email(email_content)
    
    # Insert extracted information into Firestore
    insert_into_firestore(subject)

    print("Email processed and data inserted into Firestore.")

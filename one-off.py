#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import base64

# Load environment variables
load_dotenv()

# Use the loaded environment variable for Firebase authentication
cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()


# get all documents from the collection
def get_all_documents():
    # Reference to your collection
    collection_ref = db.collection(u'thought-of-the-days').order_by(u'date')
    # Get all documents
    docs = collection_ref.stream()
    return docs


#insert content into firestore collection totd feild
def insert_into_firestore(date, text):
    # Get your document
    doc_snapshot = next(db.collection(u'thought-of-the-days').where(u'date', u'==', date).stream(), None)
    if doc_snapshot is not None:
        # Get the document reference
        doc_ref = doc_snapshot.reference
        # Update the document
        doc_ref.update({
            u'totd': text
        })
        print(f"Document successfully updated with date {date}")
    else:
        print(f"No document found with date {date}")


# Main script logic
if __name__ == "__main__":
    # Read email content from stdin
    quotes = get_all_documents()
    
    for quote in quotes:
        quote_dict = quote.to_dict()
        if 'totd' in quote_dict:
            try:
                text = base64.b64decode(quote_dict['totd']).decode('utf-8')
                insert_into_firestore(quote_dict['date'], text)
            except:
                text = quote_dict['totd']
            print(quote_dict['date'])
            print(text)

    print("totd reppaced with base64 decode content")

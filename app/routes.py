

import couchdb

COUCHDB_URL = "http://admin:vijay123@127.0.0.1:5984/"
RESUME_DB_NAME = "user-resumes"  # Separate database for PDFs

# Connect to CouchDB
couch = couchdb.Server(COUCHDB_URL)
resume_db = couch[RESUME_DB_NAME] if RESUME_DB_NAME in couch else couch.create(RESUME_DB_NAME)

def upload_pdf(user_email: str, file_path: str):
    """Uploads a PDF file to the 'user-resumes' database with email as the document ID."""
    try:
        # Read the PDF in binary mode
        with open(file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()

        doc_id = user_email  # Use email as the document ID
        file_name = f"{user_email}_resume.pdf"  # Custom file name format

        # Check if the user document exists, if not create one
        if doc_id not in resume_db:
            resume_db[doc_id] = {"email": user_email}

        # Retrieve the document
        user_doc = resume_db[doc_id]
        
        # Attach PDF to the user document
        resume_db.put_attachment(user_doc, pdf_data, filename=file_name, content_type="application/pdf")
        
        return {"success": f"PDF uploaded as {file_name}"}
    
    except Exception as e:
        return {"error": str(e)}

def download_pdf(user_email: str, save_path: str):
    """Downloads a PDF from the 'user-resumes' database and saves it locally."""
    try:
        doc_id = user_email  # Document ID (same as email)
        file_name = f"{user_email}_resume.pdf"  # Expected attachment name

        # Check if the document exists
        if doc_id not in resume_db:
            return {"error": "User resume not found in database"}

        user_doc = resume_db[doc_id]

        # Check if the expected PDF attachment exists
        if file_name not in user_doc.get('_attachments', {}):
            return {"error": "Resume attachment not found"}

        # Retrieve the PDF attachment
        pdf_data = resume_db.get_attachment(user_doc, file_name)
        if not pdf_data:
            return {"error": "Failed to retrieve PDF"}

        # Save the PDF locally
        save_location = f"{save_path}/{user_email}_resume_downloaded.pdf"
        with open(save_location, "wb") as pdf_file:
            pdf_file.write(pdf_data.read())

        return {"success": f"PDF downloaded and saved at {save_location}"}

    except Exception as e:
        return {"error": str(e)}

# Example Usage
print(upload_pdf("sadakopa2210221@ssn.edu.in", r"C:\Users\ASUS\Downloads\SadakopaRamakrishnanResume-Feb2025.pdf"))
print(download_pdf("sadakopa2210221@ssn.edu.in", r"C:\Users\ASUS\Downloads"))

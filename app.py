# from flask import Flask, request, render_template, redirect, url_for
# import pdfplumber
# import re
# import os

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# def extract_all_details_with_bidder_adjustments(pdf_path):
#     details = {
#         "state": "INDIANA",
#         "county": None,
#         "purchase_amount": None,
#         "certificate_no": None,
#         "sale_date": None,
#         "bidder_name": None,
#         "bidder_number": None,
#         "bidder_address": None,
#         "property_id": None,
#         "brief_description": None,
#         "property_address": None,
#         "owner_name": None,
#         "owner_address": None,
#         "owner_city_state_zip": None,
#         "redemption_date": None,
#         "minimum_bid": None,
#         "surplus_bid": None
#     }

#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()

#                         # State and County Information
#     county_match = re.search(r"STATE OF INDIANA,\s+([A-Za-z\s]+) COUNTY", text, re.IGNORECASE)
#     if county_match:
#         details["county"] = county_match.group(1).strip()

#     # Purchase Amount (highest dollar amount)
#     all_amounts = re.findall(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})", text)
#     if all_amounts:
#         highest_amount = max(all_amounts, key=lambda amt: float(amt.replace('$', '').replace(',', '')))
#         details["purchase_amount"] = highest_amount

#     # Certificate Number
#     cert_match = re.search(r"No\.\s*(\d+\s*\d+)", text, re.IGNORECASE)
#     if cert_match:
#         details["certificate_no"] = cert_match.group(1)

#     # Sale Date
#     sale_date_match = re.search(r"commenced\s+on\s+([A-Za-z]+,\s+[A-Za-z]+\s+\d{1,2},\s+\d{4})", text, re.IGNORECASE)
#     if sale_date_match:
#         details["sale_date"] = sale_date_match.group(1)

#     # Adjusted Bidder Information
#     bidder_number_match = re.search(r"Bidder\s+Number:\s*([A-Za-z0-9])", text, re.IGNORECASE)
#     if bidder_number_match:
#         details["bidder_number"] = bidder_number_match.group(1)
#     # Capture bidder name and expanded address lines
#     bidder_name_match = re.search(r"Bidder\s+Number:\s*[A-Za-z0-9]+\s+([A-Za-z\s]+)", text, re.IGNORECASE)
#     if bidder_name_match:
#         details["bidder_name"] = bidder_name_match.group(1).strip()
#         # Capture additional lines for the address following the name
#         following_text = text.split(details["bidder_name"], 1)[1].strip()
#         address_lines = following_text.splitlines()
#         if len(address_lines) > 1:
#             details["bidder_address"] = f"{address_lines[0].strip()}, {address_lines[1].strip()}"

#     # Property ID using specified structure
#     property_id_match = re.search(r"\d{2}-\d{2}-\d{2}-\d{3}-\d{3}\.\d{3}-\d{3}", text)
#     if property_id_match:
#         details["property_id"] = property_id_match.group(0)

#     # Brief Legal Description between markers
#     brief_desc_match = re.search(r"Brief\s+Legal\s+Description\s*[:]\s*(.*?)\s*street\s+address\s+or\s+other\s+common\s+description\s*[:]", text, re.IGNORECASE | re.DOTALL)
#     if brief_desc_match:
#         details["brief_description"] = brief_desc_match.group(1).strip()

#     # Property Address / Street Address
#     prop_addr_match = re.search(r"street\s+address\s+or\s+other\s+common\s+description\s*[:]\s*(.+)", text, re.IGNORECASE)
#     if prop_addr_match:
#         details["property_address"] = prop_addr_match.group(1).strip()

#     # Owner Name and Address, including city, state, and ZIP
#     owner_name_match = re.search(r"taxation\s+in\s+the\s+name\s+of\s+(.+)", text, re.IGNORECASE)
#     if owner_name_match:
#         details["owner_name"] = owner_name_match.group(1).strip()
#         following_owner_text = text.split(details["owner_name"], 1)[1].strip()
#         owner_address_lines = following_owner_text.splitlines()
#         if owner_address_lines:
#             details["owner_address"] = owner_address_lines[0].strip()
#             # Attempt to find city, state, and ZIP on the next line
#             if len(owner_address_lines) > 1:
#                 city_state_zip = owner_address_lines[1].strip()
#                 if re.search(r"[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}", city_state_zip):  # Simple pattern for city, state, ZIP
#                     details["owner_city_state_zip"] = city_state_zip

#     # Redemption Date
#     redemption_match = re.search(r"redemption\s+period\s*\(([^)]+)\)", text, re.IGNORECASE)
#     if redemption_match:
#         details["redemption_date"] = redemption_match.group(1).strip()

#     # Minimum Bid Amount after the first '%'
#     first_percent_match = re.search(r"%.*?(\$\d{1,3}(?:,\d{3})*(?:\.\d{2}))", text, re.IGNORECASE)
#     if first_percent_match:
#         details["minimum_bid"] = first_percent_match.group(1).strip()

#     # Surplus Bid Amount
#     surplus_bid_match = re.search(r"\(Surplus\):\s*\$\d{1,3}(?:,\d{3})*(?:\.\d{2})", text)
#     if surplus_bid_match:
#         details["surplus_bid"] = surplus_bid_match.group(0).split(":")[1].strip()

#     return details

# @app.route('/')
# def upload_file():
#     return render_template('upload.html')

# @app.route('/process', methods=['POST'])
# def process_file():
#     if 'pdf_file' not in request.files:
#         return redirect(request.url)

#     file = request.files['pdf_file']
#     if file.filename == '':
#         return redirect(request.url)

#     if file:
#         print(f"Received file: {file.filename}")
#         print(f"File type: {file.mimetype}")  # Check if the file type is PDF
#         print(f"File size: {len(file.read())} bytes")  # Check the file size (after reading, reset file pointer)
#         file.seek(0)  # Reset the file pointer after reading the file size

#         # Check if the file is a PDF
#         if not file.filename.endswith('.pdf'):
#             return "Invalid file format. Only PDF files are allowed."

#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        
#         try:
#             file.save(filepath)
#             print(f"File saved to {filepath}")
#         except Exception as e:
#             print(f"Error saving file: {e}")
#             return "Error saving file."

#         # Check if the file exists
#         if not os.path.exists(filepath):
#             return "Error: The file was not saved correctly."

#         # Extract details from the PDF
#         extracted_details = extract_all_details_with_bidder_adjustments(filepath)

#         # Render the results
#         return render_template('./templates/results.html', details=extracted_details)


# if __name__ == '__main__':
#     app.run(debug=True)



from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import pdfplumber
import re
import uvicorn
from typing import List

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_all_details_with_bidder_adjustments(pdf_path: str):
    details = {
        "state": "INDIANA",
        "county": None,
        "purchase_amount": None,
        "certificate_no": None,
        "sale_date": None,
        "bidder_name": None,
        "bidder_number": None,
        "bidder_address": None,
        "property_id": None,
        "brief_description": None,
        "property_address": None,
        "owner_name": None,
        "owner_address": None,
        "owner_city_state_zip": None,
        "redemption_date": None,
        "minimum_bid": None,
        "surplus_bid": None
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Extract county
            county_match = re.search(r"STATE OF INDIANA,\s+([A-Za-z\s]+) COUNTY", text, re.IGNORECASE)
            if county_match:
                details["county"] = county_match.group(1).strip()

            # Extract purchase amount
            all_amounts = re.findall(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})", text)
            if all_amounts:
                highest_amount = max(all_amounts, key=lambda amt: float(amt.replace('$', '').replace(',', '')))
                details["purchase_amount"] = highest_amount

            # Extract certificate number
            cert_match = re.search(r"No\.\s*(\d+\s*\d+)", text, re.IGNORECASE)
            if cert_match:
                details["certificate_no"] = cert_match.group(1)

            # Extract sale date
            sale_date_match = re.search(r"commenced\s+on\s+([A-Za-z]+,\s+[A-Za-z]+\s+\d{1,2},\s+\d{4})", text, re.IGNORECASE)
            if sale_date_match:
                details["sale_date"] = sale_date_match.group(1)

            # Extract bidder information
            bidder_number_match = re.search(r"Bidder\s+Number:\s*([A-Za-z0-9])", text, re.IGNORECASE)
            if bidder_number_match:
                details["bidder_number"] = bidder_number_match.group(1)

            bidder_name_match = re.search(r"Bidder\s+Number:\s*[A-Za-z0-9]+\s+([A-Za-z\s]+)", text, re.IGNORECASE)
            if bidder_name_match:
                details["bidder_name"] = bidder_name_match.group(1).strip()
                following_text = text.split(details["bidder_name"], 1)[1].strip()
                address_lines = following_text.splitlines()
                if len(address_lines) > 1:
                    details["bidder_address"] = f"{address_lines[0].strip()}, {address_lines[1].strip()}"

            # Extract property ID
            property_id_match = re.search(r"\d{2}-\d{2}-\d{2}-\d{3}-\d{3}\.\d{3}-\d{3}", text)
            if property_id_match:
                details["property_id"] = property_id_match.group(0)

            # Extract brief legal description
            brief_desc_match = re.search(r"Brief\s+Legal\s+Description\s*[:]\s*(.*?)\s*street\s+address\s+or\s+other\s+common\s+description\s*[:]", text, re.IGNORECASE | re.DOTALL)
            if brief_desc_match:
                details["brief_description"] = brief_desc_match.group(1).strip()

            # Extract property address
            prop_addr_match = re.search(r"street\s+address\s+or\s+other\s+common\s+description\s*[:]\s*(.+)", text, re.IGNORECASE)
            if prop_addr_match:
                details["property_address"] = prop_addr_match.group(1).strip()

            # Extract owner information
            owner_name_match = re.search(r"taxation\s+in\s+the\s+name\s+of\s+(.+)", text, re.IGNORECASE)
            if owner_name_match:
                details["owner_name"] = owner_name_match.group(1).strip()
                following_owner_text = text.split(details["owner_name"], 1)[1].strip()
                owner_address_lines = following_owner_text.splitlines()
                if owner_address_lines:
                    details["owner_address"] = owner_address_lines[0].strip()
                    if len(owner_address_lines) > 1:
                        city_state_zip = owner_address_lines[1].strip()
                        if re.search(r"[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}", city_state_zip):
                            details["owner_city_state_zip"] = city_state_zip

            # Extract redemption date
            redemption_match = re.search(r"redemption\s+period\s*\(([^)]+)\)", text, re.IGNORECASE)
            if redemption_match:
                details["redemption_date"] = redemption_match.group(1).strip()

            # Extract minimum bid
            first_percent_match = re.search(r"%.*?(\$\d{1,3}(?:,\d{3})*(?:\.\d{2}))", text, re.IGNORECASE)
            if first_percent_match:
                details["minimum_bid"] = first_percent_match.group(1).strip()

            # Extract surplus bid
            surplus_bid_match = re.search(r"\(Surplus\):\s*\$\d{1,3}(?:,\d{3})*(?:\.\d{2})", text)
            if surplus_bid_match:
                details["surplus_bid"] = surplus_bid_match.group(0).split(":")[1].strip()

    return details

@app.post("/upload-pdf/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    print("Received files:", files)  # Debugging log

    if not files:
        return JSONResponse(
            status_code=400,
            content={"message": "No files provided. Please upload PDF files."},
        )
    
    results = []
    for file in files:
        print(f"Processing file: {file.filename}")  # Debugging log
        
        if file.content_type != "application/pdf":
            return JSONResponse(
                status_code=400,
                content={"message": f"Invalid file type: {file.filename}. Please upload a PDF file."},
            )

        try:
            # Save the uploaded PDF temporarily
            file_path = f"temp_{file.filename}"
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Debugging log before extracting details
            print(f"Extracting details from {file.filename}...")

            # Extract details using the custom function
            details = extract_all_details_with_bidder_adjustments(file_path)

            # Check if details are empty or None
            if not details:
                print(f"No details extracted from {file.filename}")  # Debugging log

            # Clean up: delete the temporary file
            os.remove(file_path)

            # Append the result
            results.append({file.filename: details})

        except Exception as e:
            print(f"Error processing {file.filename}: {str(e)}")  # Debugging log
            results.append({file.filename: {"error": str(e)}})

    if not results:
        print("No results to return.")  # Debugging log
    
    print(results)
    return {"extracted_details": results}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

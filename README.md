# Automate Error Reporting and Data Profiling During Data Ingestion

Individual contributors upload their Excel/CSV data into a designated cloud storage folder with access controls in place. This action automatically triggers code hosted on GitHub through Azure Function and GitHub Actions workflows. The system then performs data profiling, comparing the uploaded data with the expected format. If the data fails to meet the required standards or contains errors, the system automatically sends an email to the data provider, explaining the issue so they can promptly address it. Meanwhile, the central admin team is also notified, ensuring they stay informed.

Once the data provider corrects the errors and uploads the revised data, the system sends a thank-you email along with a data profiling report. This gives the provider an overview of the corrected data.

Overall Workflow is demonstrated below

<div style="text-align: center;">
  <img src="https://github.com/EnhongLiu/methane_data_ingestion_pipeline/blob/aca8ccdd98fcd7c43b35e8297db472957fffd253/pic/azure%20function%20pipeline.png" width="800" height="auto">
</div>


## All tasks within the system are automated, requiring no human intervention except for maintenance and package updates.



## Prototype Implementation

### 📌 Overview

A prototype version of this system has been developed to demonstrate the architecture and core functionalities. The prototype is located in the prototype directory on a separate branch.

🔹 **Features of the Prototype**

- **React Frontend**: Users can upload a file and provide an email address.
- **Flask Backend**:
  - Accepts file and email input.
  - Processes the file and performs basic operations.
  - Uploads the processed file to Azure Blob Storage.
  - Sends an email with the processed files and link.
- **Swagger Documentation**: API endpoints are documented for easy testing.


🚀 **How to Run the Prototype**

1️⃣ **Clone the Repository**

Ensure you are on the correct branch:

```sh
git clone https://github.com/EnhongLiu/methane_data_ingestion_pipeline.git
cd prototype

2️⃣ Run the Backend API (Flask)

Prerequisites:

Python 3.x installed.

Virtual environment setup.

cd prototype/api
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Start the API:
```sh
export AZURE_STORAGE_CONNECTION_STRING='YourConnectionString'
export EMAIL='LabEmail'
export APP_PASSWORD=''
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000

By default, the API runs on http://localhost:5000.
```

3️⃣ Run the Frontend (React)

Prerequisites:

Node.js and npm installed.
```sh
cd prototype/frontend/methane-frontend
npm install
npm start

By default, the frontend runs on http://localhost:3000.
```

4️⃣ Test API with Swagger

Once the backend is running, access Swagger documentation:
```sh
http://localhost:5000/swagger/
```

This provides interactive documentation to test API endpoints.


5️⃣ Upload a File & Receive an Email

Open the frontend at http://localhost:3000.

Select a file and enter a valid email address.

Click "Upload" to send the request to the backend.

If successful, an email with the processed file link will be sent to the provided email.

🔄 Next Steps

Expand backend logic to include full data profiling and validation.

Improve error handling and notification features.

Increase support for additional file types and cloud integrations.

This prototype serves as a foundational implementation, showcasing the architecture and functionality while allowing for future enhancements. 🚀



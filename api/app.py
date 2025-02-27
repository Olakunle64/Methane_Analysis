from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient
import os
import pandas as pd
from io import BytesIO
from functions import send_email
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# Setting up Swagger documentation
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Methane Data API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# Azure Storage connection string
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "uploads"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# Ensure container exists
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
if not container_client.exists():
    container_client.create_container()


@app.errorhandler(404)
def page_not_found(error):
    """return 404 error when a page is not found"""
    return make_response(jsonify({"error": "***Not Found***"}), 404)


@app.route('/')
def index():
    return jsonify({'API Status': 'active'})


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    email = request.form['email']
    if email == '':
        return jsonify({'error': 'No email provided'}), 400
    # print(f"email: {request.form['email']}")
    # return jsonify({'message': 'File uploaded successfully'})
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file)

        # Compute methane intensity
        df["Methane_Intensity_g_per_L"] = df["Methane_Emission_g_per_day"] / df["Milk_Production_L_per_day"]

        # Convert DataFrame to CSV in memory
        fileName = file.filename.split('.')
        if len(fileName) > 1:
            output_file_name = f"{fileName[0]}_processed.csv"
        else:
            output_file_name = f"{file.filename}_processed.csv"
        # output_file_name = f"{file.filename}_processed.csv"
        output_buffer = BytesIO()
        df.to_csv(output_buffer, index=False)
        output_buffer.seek(0)

        # Upload processed file to Azure Blob Storage
        processed_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=output_file_name)
        processed_blob_client.upload_blob(output_buffer, overwrite=True)

        # # Delete original file from Blob Storage
        # original_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
        # original_blob_client.delete_blob()

        # Generate URL of the processed file
        processed_file_url = f"https://methanedata.blob.core.windows.net/{CONTAINER_NAME}/{output_file_name}"
        sender_email = os.getenv("EMAIL")
        app_password = os.getenv("APP_PASSWORD")
        send_email(sender_email, app_password, email, processed_file_url)

        return jsonify({'message': 'File processed and uploaded successfully', 'file_url': processed_file_url})
    
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/get_processed_file', methods=['GET'])
def get_processed_file():
    file_name = request.args.get('file_name')  # Get file name from query parameter

    if not file_name:
        return jsonify({'error': 'Missing file_name parameter'}), 400

    try:
        # Fetch the processed file from Azure Blob Storage
        processed_blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)

        if not processed_blob_client.exists():
            return jsonify({'error': f'File {file_name} not found in Blob Storage'}), 404

        # Download the file content
        blob_data = processed_blob_client.download_blob().readall()
        
        # Read CSV into Pandas DataFrame
        df = pd.read_csv(BytesIO(blob_data))

        # Convert DataFrame to JSON and return it
        return jsonify({'message': 'File retrieved successfully', 'data': df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/list_files', methods=['GET'])
def list_files():
    try:
        # List blobs in the container
        blob_list = container_client.list_blobs()
        files = [blob.name for blob in blob_list]
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = os.getenv("API_PORT", 5000)
    # app.run(host=HOST, port=PORT, threaded=True)
    app.run(debug=True)

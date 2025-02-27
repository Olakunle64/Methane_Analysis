from azure.storage.blob import BlobServiceClient
# from azure.identity import DefaultAzureCredential

# Connection string for Azurite (local emulator)
# connection_string = 
# Create DefaultAzureCredential
# default_credential = DefaultAzureCredential()
# Create BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Name of the container
container_name = "uploads"

# Name of the file to upload
local_file_path = "test.py"  # The path to the file you want to upload
blob_name = "example.txt"  # The name it will have in the blob storage

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

print(container_client)
# # Upload the file
# with open(local_file_path, "rb") as data:
#     container_client.upload_blob(name=blob_name, data=data, overwrite=True)

# print(f"File '{local_file_path}' uploaded successfully to container '{container_name}'!")
blobs = container_client.list_blobs()
for blob in blobs:
    print(blob.name)

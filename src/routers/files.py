from fastapi import APIRouter, UploadFile, Form, File
import src.utils.logging_config
import logging


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)


from src.config import settings
import requests
from pydantic import BaseModel
import subprocess
import os
router = APIRouter()


STORAGE_PATH = "storage1"
CLIENT_DOCKER_ID = "connector-1-ui"
INSTANCE = "LDS"
DATA_FOLDER_PATH = "/app/data_folder"
LDS_CONNECTOR_PATH= "/app/docker_compose"
UPLOAD_LDS_SCRIPT = "uploadToEDC1.sh"


  
async def auth_keycloak(username: str = "admin", password: str = "admin"):
    # Gain token from Keycloak
    URL = f"https://{settings.ADDRESS}/auth/realms/{INSTANCE}/protocol/openid-connect/token"

    # Init params
    data = {
        "client_id": CLIENT_DOCKER_ID,
        "grant_type": "password",
        "username": username,
        "password": password
    }

    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    try: 
        response = requests.post(URL, data=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {"error": "Authentication request failed.", "details": str(e)}

    return response.json()


@router.get("/files/list")
async def read_files():

    # List files in data folder - add size of files
    try:
        files = os.listdir(DATA_FOLDER_PATH)
        files = [
            {
                "name": file, 
                "size": f"{(round(os.path.getsize(os.path.join(DATA_FOLDER_PATH, file)) / 1024, 2))} KB"
            } 
            for file in files if os.path.isfile(os.path.join(DATA_FOLDER_PATH, file))]
        if not files:
            logger.info("No files found in the data folder.")
            return {"message": "No files found."}
        
        logger.info(f"Files listed successfully: {files}")
        return {"files": files}
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return {"error": "Failed to list files.", "details": str(e)}
    


@router.post("/files/upload")
async def upload_file(
        username: str = Form(..., description="Username for authentication"),
        password: str   = Form(..., description="Password for authentication"),
        file: UploadFile  = File(None, description="File to upload (optional)")

):

    auth = await auth_keycloak(username, password)
    if "error" in auth:
        logger.error(auth['details'])
        return auth

    if file:
        # If file is provided, handle the upload
        contents = await file.read()
        logger.info(f"User {username} uploaded file: {file.filename} of size {len(contents)} bytes")
    else:
        logger.info(f"No file uploaded by user {username}.")
        return {"message": "No file uploaded."}

    
    # Save the file to the storage path
    file_path = f"{DATA_FOLDER_PATH}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
        logger.info(f"File saved to {file_path}")


    # Execute the upload script
    try:
        script_path = os.path.join(LDS_CONNECTOR_PATH, UPLOAD_LDS_SCRIPT)

        subprocess.run( 
            ["/bin/bash", script_path, username, password, file_path],
            cwd=LDS_CONNECTOR_PATH,
            check=True
        )
        logger.info(f"Upload script executed successfully for user {username}")
        return {"message": f"File {file.filename} uploaded successfully by user {username}."}
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing upload script: {str(e)}")
        return {"error": "Failed to execute upload script.", "details": str(e)}

    


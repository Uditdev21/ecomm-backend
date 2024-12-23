from fastapi import APIRouter, HTTPException, Depends, File, status, Form, UploadFile
from .auth import check_user,user_status,check_user_status  # Assuming check_user is a dependency for user validation
from cloudinary.uploader import upload
from cloudinary.exceptions import Error
from cloudinary import config
from dotenv import load_dotenv
import os
load_dotenv()


# FastAPI router
admin = APIRouter()

# Cloudinary configuration
api_secret = os.getenv("CLOUDINARY_API_SECRET")
api_key = os.getenv("CLOUDINARY_API_KEY")
cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")

# _folder = "products"
config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)


# Function to upload file to Cloudinary
def uploade_file(image,_folder):
    try:
        response = upload(
            file=image,
            folder=_folder
        )
        return response
    except Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unable to upload the file: {str(e)}")


# FastAPI endpoint for file upload
# @admin.post("/upload")
# async def upload_product(
#     file: UploadFile = File(...), 
#     user_type: str = Depends(check_user_status)
# ):
#     try:
#         # Read file content
#         file_content = await file.read()

#         # Upload to Cloudinary
#         response = uploade_file(file_content)

#         # Return the Cloudinary response
#         return {
#             "message": "File uploaded successfully",
#             "url": response.get("secure_url"),
#             "public_id": response.get("public_id"),
#         }
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
#             detail=f"Unexpected error: {str(e)}"
#         )

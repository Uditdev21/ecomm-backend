import datetime
import firebase_admin
from firebase_admin import credentials,auth
from firebase_admin.auth import InvalidIdTokenError
from .db import db,users_collection,userModel,user_status
from fastapi import Request, status,HTTPException
from pydantic import BaseModel




cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)




async def check_user(request: Request):
    auth_header = request.headers.get('Authorization')

    if auth_header is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    try:
        token = auth_header.split(" ")[1]
        decoded_token=auth.verify_id_token(token)
        uid = decoded_token["user_id"]  
        email = decoded_token.get("email")

        user=users_collection.find_one({"uid":uid})
        if user:
            # Return the existing user's details
            return {
                "uid": user["uid"],
                "email": user["email"],
                "user_type": user["user_type"]
            }
        else:
            # Create a new user document
            # new_user = {
            #     "uid": uid,
            #     "email": email,
            #     "user_type": user_status.CLIENT,  # Default user type
            #     # "created_at": datetime.utcnow()  # Use current timestamp
            # }
            new_user=userModel(uid=uid,email=email,user_type=user_status.CLIENT)
            # Insert the new user into the database
            users_collection.insert_one(new_user)
            return new_user

    except InvalidIdTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid address")
        
#test
def check_user_status(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authorization header missing"
        )
    try:
        token = auth_header.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["user_id"]
        user_doc = users_collection.find_one({"uid": uid})
        
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="User not found"
            )

        if user_doc["user_type"] == user_status.ADMIN:
            return user_status.ADMIN
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access denied"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Token verification failed: {str(e)}"
        )

from fastapi import APIRouter,HTTPException,Depends,Header,status
from .auth import check_user
from .db import db,userModel,prdoducts_collection

client=APIRouter()

@client.get('/prod')
def getdata(user=Depends(check_user)):
    print(user)
    return [{"name":"udit","description":"test data"},{"name":"udit","description":"test data"}]


def serialize_object_id(document):
    # Convert all _id fields to string
    if '_id' in document:
        document['_id'] = str(document['_id'])
    return document

@client.get('/getProducts')
def get_products(user=Depends(check_user)):
    try:
        # Fetch all documents from the collection
        docs = prdoducts_collection.find()

        # Convert the cursor to a list
        product_list = [serialize_object_id(doc) for doc in docs]

        # Optionally, you can log the documents or return them in the response
        return product_list

    except Exception as e:
        # Handle any exception that occurs during the process
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Some internal server error occurred: {str(e)}"
        )
from fastapi import APIRouter,HTTPException,Depends,Header,status,Query
from .auth import check_user
from .db import db,userModel,prdoducts_collection,catagory_collection,users_collection,orders_cpollection,order_status
from bson import ObjectId
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

client=APIRouter()

@client.get('/prod')
def getdata(user=Depends(check_user)):
    print(user)
    return [{"name":"udit","description":"test data"},{"name":"udit","description":"test data"}]



def serialize_product_object_id(doc):
    # """Convert ObjectId to string in MongoDB document."""
    doc["_id"] = str(doc["_id"])
    if "catagory" in doc and isinstance(doc["catagory"], ObjectId):
        doc["catagory"] = str(doc["catagory"])
    return doc

def serialize_category_object_id(doc):
    """Convert ObjectId to string in MongoDB document."""
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if "prdoducts" in doc and isinstance(doc["prdoducts"], list):
        doc["prdoducts"] = [
            str(product_id) if isinstance(product_id, ObjectId) else product_id
            for product_id in doc["prdoducts"]
        ]
    return doc

@client.get('/getProducts')
def get_products(user=Depends(check_user)):
    try:
        # Fetch all documents from the collection
        docs = prdoducts_collection.find()

        # Convert the cursor to a list
        product_list = [serialize_product_object_id(doc) for doc in docs]

        # Optionally, you can log the documents or return them in the response
        return product_list

    except Exception as e:
        # Handle any exception that occurs during the process
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Some internal server error occurred: {str(e)}"
        )
    
@client.get('/getCategory')
def getCategory(user=Depends(check_user)):
    try:
        # Fetch documents from the collection
        docs = catagory_collection.find()
        docs_list = list(docs)  # Convert cursor to a list

        # Serialize the documents
        catagory_list = [serialize_category_object_id(doc) for doc in docs_list]
        
        return catagory_list

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get category: {str(e)}"
        )


@client.get('/getproductByCategory')
def getproductByCategory(catagoryID:str=Query(...),user=Depends(check_user)):
    try:
        try:
            catagory_id = ObjectId(catagoryID)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid documentID format"
            )
        print("test")
        docs=prdoducts_collection.find({'catagory':catagory_id})
        product_list = [serialize_product_object_id(doc) for doc in docs]
        print (product_list)
        print(len(product_list))  # FastAPI example

        return product_list
        # return 
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to get product by category: {str(e)}")
    

@client.get('/buyProduct')
def buyProduct(productID: str = Query(...), payment: str = Query(...), user=Depends(check_user)):
    try:
        try:
            product_id = ObjectId(productID)
        except Exception as e:
            logging.error(f"Invalid documentID format: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid documentID format"
            )
        try:
            user_id=ObjectId(user["_id"])
        except Exception as e:
            logging.error(f"Invalid documentID format: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid documentID format"
                )

        userdoc = users_collection.find_one({'_id': user_id})
        if not userdoc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        doc = prdoducts_collection.find_one({'_id': product_id})
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        order_doc = {
            'product': product_id,
            'user': user_id,
            'payment_type': payment,
            'order_status': order_status.PENDING.value
        }
        order_result = orders_cpollection.insert_one(order_doc)
        users_collection.update_one({'_id': user_id}, {'$push': {'order': order_result.inserted_id},'$inc':{'current_order':1}})
        return {"message": "Order placed successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Failed to place order: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to place order")
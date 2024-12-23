from fastapi import APIRouter,HTTPException,File,UploadFile,status,Form,Query
from firebase_admin import auth
from .admin import uploade_file

from .db import prdoducts_collection,slidshow_collection,catagory_collection,orders_cpollection,payment_type,productModel,imageStruct,order_status
from bson import ObjectId

# from pymongo.database import

testRouts= APIRouter()



# def serialize_object_id(document):
#     # Convert all _id fields to string
#     if '_id' in document:
#         document['_id'] = str(document['_id'])
#     return document
def serialize_product_object_id(doc):
    # """Convert ObjectId to string in MongoDB document."""
    doc["_id"] = str(doc["_id"])
    if "catagory" in doc and isinstance(doc["catagory"], ObjectId):
        doc["catagory"] = str(doc["catagory"])
    return doc

@testRouts.get('/generate-token')
def generate_test_token(uid: str):
    # Create a custom token for the user
    custom_token = auth.create_custom_token(uid)
    # return custom_token.decode('utf-8') 
    print(f"Custom Token: {custom_token.decode('utf-8')}")




@testRouts.post('/upload')
async def uploade_product(
    image_small: UploadFile = File(...),
    image_medium: UploadFile = File(...),
    image_large: UploadFile = File(...),
    Name: str = Form(...),
    Discription: str = Form(...),
    Price: str = Form(...),
    catagory:str=Form(...)
):
    try:
        # Read file content
        image_small_content = await image_small.read()
        image_medium_content = await image_medium.read()
        image_large_content = await image_large.read()

        # Upload to Cloudinary
        response_1 = uploade_file(image_small_content,'products')
        response_2 = uploade_file(image_medium_content,'products')
        response_3 = uploade_file(image_large_content,'products')

        try:
            catagory_id = ObjectId(catagory)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid documentID format"
            )
        print("test")
        # Prepare product details
        product_details = productModel(
            image_small=imageStruct(image_url=response_1.get("secure_url"), image_publicid=response_1.get("public_id")),
            image_medium=imageStruct(image_url=response_2.get("secure_url"), image_publicid=response_2.get("public_id")),
            image_large=imageStruct(image_url=response_3.get("secure_url"), image_publicid=response_3.get("public_id")),
            Discription=Discription,
            price=Price,
            Name=Name,
            catagory=catagory_id
        )
        # print(catagory_id)
        # Insert product into the database
        prcoductDoc=prdoducts_collection.insert_one(product_details.dict())
        try:
            productid=ObjectId(prcoductDoc.inserted_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid documentID format"
            )
        #update the catagory collection with the product id
        catagory_collection.update_one({'_id':catagory_id},{'$push':{'prdoducts':productid}})

        return {"message": "File uploaded successfully", "Name": Name}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )



@testRouts.get('/getProducts')
def get_products():
    try:
        # Fetch all documents from the collection
        docs = prdoducts_collection.find()
        print(docs)

        # Convert the cursor to a list
        product_list = [serialize_product_object_id(doc) for doc in docs]

        # Optionally, you can log the documents or return them in the response
        return product_list
        print(product_list)

    except Exception as e:
        # Handle any exception that occurs during the process
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Some internal server error occurred: {str(e)}"
        )
    

# @testRouts.get('/getSlidshowImages')

@testRouts.get('testkey')
def data(form=Form(...)):
    print(form)
    return "test"

@testRouts.post('/UplodeSlidShowImages')
async def upload_slideshow_image(
    image: UploadFile = File(),
    documentID: str = Form()  # Ensure the ID is passed as a string
):
    file = await image.read()
    try:
        # Upload the file to your file storage
        response = uploade_file(file, 'slidShowImages')
        if not response or 'secure_url' not in response:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="File upload failed"
            )

        # Validate documentID as an ObjectId
        try:
            linked_product_id = ObjectId(documentID)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid documentID format"
            )

        # Prepare the document to insert into the database
        doc = {
            'image_url': response.get("secure_url"),
            'linkedproduct': linked_product_id  # Store as ObjectId reference
        }

        # Insert the document into the slidshow_collection
        slidshow_collection.insert_one(doc)

        return {"message": "File uploaded successfully", "image_url": response.get("secure_url")}

    except HTTPException as e:
        raise e
    except Exception as e:
        # Handle generic errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to upload"
        )


@testRouts.post('/createCategory')
async def createCategory(name=Form(...),discription=Form(...),image:UploadFile=File()):
    try:
        file=await image.read()
        response=uploade_file(file,'CategoryImage')
        docs={'Name':name,
              'discription':discription,
              'image_url':response.get("secure_url"),
              'prdoducts':[]}
        collection_id=catagory_collection.insert_one(docs)
        return {"message":"category uploded","category_id":f" {collection_id.inserted_id}"}

    except:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='faild to upload document')


@testRouts.get('/getCategory')
def getCategory():
    try:
        docs=catagory_collection.find()
        catagory_list = [serialize_product_object_id(doc) for doc in docs]
        return catagory_list
    except:
        HTTPException()

@testRouts.get('/getproductByCategory')
def getproductByCategory(catagoryID:str=Query(...)):
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
        return product_list
        # return 
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to get product by category: {str(e)}")


@testRouts.get('/slidshowImages')
def slidShowImages():
    try:
        print("test")
    except:
        HTTPException()


@testRouts.get('/buyProduct')
def buyProduct(productID:str=Query(...),payment:str=Query(...)):
    try:
        try:
            product_id = ObjectId(productID)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid documentID format"
            )
        
        doc=prdoducts_collection.find_one({'_id':product_id})
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")
        orders_cpollection.insert_one(doc,payment_type=payment,order_Status=order_status.PENDING)
        return {"message":"order placed successfully"}
    except:
        raise HTTPException()
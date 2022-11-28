import fastapi
import fastapi.security as security 
import sqlalchemy.orm as orm 
import services
from fastapi import Form
import schemas 
from typing import List



app = fastapi.FastAPI()

@app.post('/api/users')
async def create_user(user : schemas.UserCreate , db : orm.Session = fastapi.Depends(services.get_db)):
    db_user = await services.get_user_by_email(user.email , db)
    if db_user:
        raise fastapi.HTTPException(status_code = 400, detail = "User with the email already exists")
    user =  await services.create_user(user, db)
    return await services.create_token(user)

@app.post('/api/token')
async def generate_token(form_data : security.OAuth2PasswordRequestForm = fastapi.Depends(), db : orm.Session = fastapi.Depends(services.get_db)):
    user = await services.authenticate_user(form_data.username , form_data.password , db)
    if not user:
        raise fastapi.HTTPException(status_code = 401, detail = "Invalid Credentials")
    return await services.create_token(user)


@app.get('/api/user/me' , response_model=schemas.User)
async def get_user(user : schemas.User = fastapi.Depends(services.get_current_user)):
    return user

@app.post("/api/products",  response_model = schemas.Product)
async def create_product(product : schemas.ProductCreate , user : schemas.User = fastapi.Depends(services.get_current_user) , db : orm.Session = fastapi.Depends(services.get_db)):
    return await services.create_product(user = user, db = db , product = product)


@app.get("/api/products", response_model = List[schemas.Product])
async def get_products(user : schemas.User = fastapi.Depends(services.get_current_user) , db : orm.Session = fastapi.Depends(services.get_db)):
    return await services.get_products(user = user, db = db)


@app.get("/api/products/{product_id}" , status_code = 200)
async def get_product(product_id : int, user : schemas.User = fastapi.Depends(services.get_current_user) , db : orm.Session = fastapi.Depends(services.get_db)):
    return await services.get_product(product_id , user , db)
    
@app.delete("/api/product/{product_id}" , status_code = 204)
async def delete_product(product_id : int, user : schemas.User = fastapi.Depends(services.get_current_user) , db : orm.Session = fastapi.Depends(services.get_db)):
    await services.delete_product(product_id, user, db)
    return {"message" , "Successfully deleted"}

@app.put("/api/product/{product_id}" , status_code = 200)
async def update_product(product_id : int,product : schemas.ProductCreate, user : schemas.User = fastapi.Depends(services.get_current_user) , db : orm.Session = fastapi.Depends(services.get_db)):
    await services.update_product(product_id , product, user, db)
    return {"message" , "SuccessFully Updated"}

@app.get("/api")
async def root():
    return {"message" : "Product listing @ Noon"}

    
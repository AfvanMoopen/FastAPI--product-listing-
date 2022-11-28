import database 
import sqlalchemy.orm as orm 
import models
import jwt 
import datetime
import fastapi.security as security 
import fastapi 
import schemas 
import sqlalchemy.orm as orm 
import passlib.hash as hash 

oauth2schema = security.OAuth2PasswordBearer(tokenUrl='/api/token')
JWT_SECRET = "infosec"

def create_database():
    return database.Base.metadata.create_all(bind = database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db 
    finally:
        db.close()

async def get_user_by_email(email : str, db : orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def create_user(user : schemas.UserCreate , db : orm.Session):
    user_obj = models.User(email = user.email , hashed_password = hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email : str, password : str, db : orm.Session):
    user = await get_user_by_email(email = email, db = db)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user

async def create_token(user : models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict() , JWT_SECRET)
    return dict(access_token = token , token_type = "bearer")

async def get_current_user(db : orm.Session = fastapi.Depends(get_db), token : str = fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token , JWT_SECRET , algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code = 401 , detail = "Invalid email or password")
    return schemas.User.from_orm(user)

async def create_product(user : schemas.User , db : orm.Session , product : schemas.ProductCreate):
    product = models.Product(**product.dict() , owner_id = user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return schemas.Product.from_orm(product)


async def get_products(user : schemas.User, db : orm.Session):
    products = db.query(models.Product).filter_by(owner_id = user.id)
    return list(map(schemas.Product.from_orm , products))

async def product_selector(product_id : int, user : schemas.User , db : orm.Session):
    product = (db.query(models.Product).filter_by(owner_id = user.id).filter(models.Product.id == product_id).first())
    if product is None:
        raise fastapi.HTTPException(status_code = 404 , detail = "Not found")
    return product

async def get_product(product_id : int , user : schemas.User , db : orm.Session):
    product = await product_selector(product_id = product_id , user = user , db = db)
    return schemas.Product.from_orm(product)

async def delete_product(product_id : int, user : schemas.User, db : orm.Session):
    product = await product_selector(product_id , user, db)
    product.delete()
    db.commit()
    
async def update_product(product_id : int, product : schemas.ProductCreate , user : schemas.User , db : orm.Session):
    product_db = await product_selector(product_id , user, db)
    product_db.first_name = product.first_name
    product_db.last_name = product.last_name
    product_db.email = product.email 
    product_db.company = product.company 
    product_db.note = product.note 
    product_db.date_past_updated = datetime.datetime.utcnow()
    db.commit()
    db.refresh(product_db)
    return schemas.Product.from_orm(product_db)

    
    
    
    
    
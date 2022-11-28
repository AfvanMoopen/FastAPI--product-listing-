import datetime 
import pydantic 

class UserBase(pydantic.BaseModel):
    email : str 

class UserCreate(UserBase):
    hashed_password : str
    class Config:
        orm_mode = True
    
class User(UserBase):
    id : int 
    class Config:
        orm_mode = True 

class ProductBase(pydantic.BaseModel):
    first_name : str 
    last_name : str 
    email : str 
    company : str
    note : str 

class ProductCreate(ProductBase):
    ...
    
class Product(ProductBase):
    id : int
    owner_id : int 
    date_created : datetime.datetime 
    data_past_updated : datetime.datetime 
    
    class Config:
        orm_mode = True 
        
    
import datetime 
import database
import sqlalchemy.orm as orm 
import passlib.hash as hash 
import sqlalchemy

class User(database.Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer , primary_key = True , index = True)
    email = sqlalchemy.Column(sqlalchemy.String, unique = True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    products = orm.relationship("Product" , back_populates="users")
    
    def verify_password(self, password : str):
        return hash.bcrypt.verify(password,self.hashed_password)

class Product(database.Base):
    __tablename__ = "products"
    id = sqlalchemy.Column(sqlalchemy.Integer , primary_key = True , index = True)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer , sqlalchemy.ForeignKey("users.id"))
    first_name = sqlalchemy.Column(sqlalchemy.String , index = True)
    last_name = sqlalchemy.Column(sqlalchemy.String, index = True)
    email = sqlalchemy.Column(sqlalchemy.String, index = True)
    company = sqlalchemy.Column(sqlalchemy.String, index = True , default = " ")
    note = sqlalchemy.Column(sqlalchemy.String, default = " ")
    date_created = sqlalchemy.Column(sqlalchemy.DateTime, default = datetime.datetime.utcnow)
    data_past_updated = sqlalchemy.Column(sqlalchemy.DateTime, default = datetime.datetime.utcnow)
    users = orm.relationship("User" , back_populates="products")
    
    

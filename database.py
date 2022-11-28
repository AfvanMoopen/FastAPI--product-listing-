import sqlalchemy
import sqlalchemy.ext.declarative as declarative 
import sqlalchemy.orm as orm 

URL_DB = "sqlite:///./database.db"
engine = sqlalchemy.create_engine(URL_DB , connect_args = {"check_same_thread": False})
SessionLocal = orm.sessionmaker(autocommit=False , autoflush=False , bind = engine)
Base = declarative.declarative_base()

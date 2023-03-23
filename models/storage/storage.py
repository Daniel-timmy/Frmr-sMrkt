from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.products import Products
from models.users import Users
from models.loggedusers import LoggedUsers

classes = {"Products": Products, "Users": Users, "LoggedUsers": LoggedUsers}


class DBStorage:
    """The database class"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiate the database"""
        # self.__engine = create_engine('mysql+pymysql://farm:password@127.0.0.1/farmers_db', echo=None)
        self.__engine = create_engine('sqlite:///farmer.db', echo=None)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        s_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session_f = scoped_session(s_factory)
        self.__session = session_f

    def new(self, obj):
        """add a new object to the database"""
        self.__session.add(obj)

    def save(self):
        """commit changes to the current database session"""
        self.__session.commit()

    def delete(self, obj):
        """delete from the current database session"""
        self.__session.delete(obj)

    def get(self):
        """returns a single object"""

    def all(self, cls=None):
        """gets all objects form the database"""
        obj_dict = {}
        if cls in classes.values():
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + obj.id
                obj_dict[key] = obj
        elif cls is None:
            for clss in classes.values():
                objs = self.__session.query(clss).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    obj_dict[key] = obj.to_dict()
        return obj_dict

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

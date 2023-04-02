from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


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

    def get(self, attr, cls=None):
        """returns true if object exists, otherwise false"""
        objs = self.all(cls)

        for obj in objs.values():
            if attr in obj.to_dict().values():
                return True
        return False

    def get_obj(self, attr, cls=None):
        """returns a single object"""
        objs = self.all(cls)

        for obj in objs.values():
            # print(obj.username)
            if attr in obj.to_dict().values():

                return obj
        return None

    def get_one(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        from models.products import Products
        from models.users import Users
        from models.customers import Customers
        from models.registered_farm import Business
        from models.reviews import Reviews
        import models
        classes = \
            {"Products": Products, "Users": Users, "Business": Business, "Customers": Customers}

        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def all(self, cls=None):
        """gets all objects form the database"""
        from models.products import Products
        from models.users import Users
        from models.customers import Customers
        from models.registered_farm import Business
        from models.reviews import Reviews
        classes = \
            {"Products": Products, "Users": Users, "Business": Business, "Customers": Customers, "Reviews": Reviews}

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

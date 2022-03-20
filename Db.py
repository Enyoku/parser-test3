import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import ForeignKey, Numeric, Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from local_settings import posrtgesql as settings


DeclarativeBase = declarative_base()

engine = create_engine(
    f'postgresql+psycopg2://{settings["username"]}:{settings["password"]}@{settings["host"]}/{settings["database"]}')

engine.connect()

# connection = psycopg2.connect(user="postgres", password="556893765r")
# connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# cursor = connection.cursor()
# sql_create_database = cursor.execute(
#     f'create database parser')
# cursor.close()
# connection.close()


class Category(DeclarativeBase):
    __tablename__ = 'Category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column('category_name', String)
    gender = Column('male', bool, default=False)

    def __repr__(self):
        return "".format(self.code)


class Product(DeclarativeBase):
    __tablename__ = 'Product'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(40), nullable=False)
    category_name = Column(Integer, ForeignKey(Category.category_id))
    description = Column(Text)
    article = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)


class Last_check(DeclarativeBase):
    __tablename__ = 'Last_check'

    check_id = Column(Integer, primary_key=True)
    check_date = Column(DateTime, nullable=False)


DeclarativeBase.metadata.create_all(engine)

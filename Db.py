from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, ForeignKey, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from local_settings import posrtgesql as settings


engine = create_engine(
    f'postgresql+psycopg2://{settings["username"]}:{settings["password"]}@{settings["host"]}/{settings["database"]}', echo=True,)

DeclarativeBase = declarative_base()


class Category(DeclarativeBase):
    __tablename__ = 'Category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False, unique=True)
    gender = Column(Boolean, default=False)
    Product = relationship("Product")


class Product(DeclarativeBase):
    __tablename__ = 'Product'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False)
    category_name = Column(String(100))
    check_date = Column(DateTime)
    description = Column(Text)
    article = Column(Integer)
    price = Column(Numeric(10, 2), nullable=False)
    Category = relationship("Category")
    last_check = relationship("Last_check")

    __table_args__ = (
        ForeignKeyConstraint(['category_name'], ['Category.category_name']),
        ForeignKeyConstraint(['check_date'], ['Last_check.check_date']),
    )


class Last_check(DeclarativeBase):
    __tablename__ = 'Last_check'

    check_id = Column(Integer, primary_key=True)
    check_date = Column(DateTime)
    Product = relationship("Product")

    __table_args__ = (
        UniqueConstraint('check_date', name='_check_date_uc'),
    )


DeclarativeBase.metadata.create_all(engine)

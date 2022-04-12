from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint, ForeignKey, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from local_settings import posrtgesql as settings
# ?=======================================IF USES PostgreSQL=============================================================

engine = create_engine(
    f'postgresql+psycopg2://{settings["username"]}:{settings["password"]}@{settings["host"]}/{settings["database"]}', echo=True,)

# ?========================================IF USES SQLite================================================================

# engine = create_engine('sqlite:///places.sqlite', echo=True)

# ?======================================================================================================================

DeclarativeBase = declarative_base()


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


DeclarativeBase.metadata.create_all(engine)

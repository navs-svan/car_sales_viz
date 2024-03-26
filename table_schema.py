from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import CHAR, VARCHAR, INTEGER, DATE
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import URL, create_engine
import os

Base = declarative_base()

class Dates(Base):
    __tablename__ = "dates"

    date_id = Column(CHAR(7), primary_key=True)
    date = Column(DATE)
    year = Column(INTEGER)
    month = Column(INTEGER)
    quarter = Column(CHAR(2))

    revenue = relationship("Revenue")


class Branch(Base):
    __tablename__ = "branches"

    branch_id = Column(CHAR(7), primary_key=True)
    branch_nm = Column(VARCHAR(256))
    country_nm = Column(VARCHAR(256))

    revenue = relationship("Revenue")


class Countries(Base):
    __tablename__ = "countries"

    country_id = Column("country_id", CHAR(7), primary_key=True)
    country_nm = Column("country_nm", VARCHAR(128))

    dealer = relationship("Dealer")


class Dealer(Base):
    __tablename__ = "dealers"

    dealer_id = Column(CHAR(7), primary_key=True)
    dealer_nm = Column(VARCHAR(256))
    location_id = Column(CHAR(6))
    location_nm = Column(VARCHAR(128))
    country_id = Column(CHAR(7), ForeignKey(Countries.country_id))

    revenue = relationship("Revenue")


class Products(Base):
    __tablename__ = "products"

    model_id = Column(VARCHAR(16), primary_key=True)
    product_nm = Column(VARCHAR(32))
    model_nm = Column(VARCHAR(32))

    revenue = relationship("Revenue")


class Revenue(Base):
    __tablename__ = "revenue"

    dealer_id = Column(CHAR(7), ForeignKey(Dealer.dealer_id), primary_key=True)
    model_id = Column(VARCHAR(16), ForeignKey(Products.model_id), primary_key=True)
    branch_id = Column(CHAR(7), ForeignKey(Branch.branch_id), primary_key=True)
    date_id = Column(CHAR(7), ForeignKey(Dates.date_id), primary_key=True)
    units_sold = Column(INTEGER)
    revenue = Column(INTEGER)


if __name__ == "__main__":
    # CREATE THE TABLES
    
    DBHOST = os.environ.get("DBHOST")
    DBPORT = os.environ.get("DBPORT")
    DBUSER = os.environ.get("DBUSER")
    DBNAME = os.environ.get("DBNAME")
    DBPASS = os.environ.get("DBPASS")

    engine_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DBUSER,
        password=DBPASS,
        host=DBHOST,
        port=DBPORT,
        database=DBNAME,
    )
    engine = create_engine(url=engine_url)

    Base.metadata.create_all(bind=engine)
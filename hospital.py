from sqlalchemy import String, Column, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Hospital(Base):
    __tablename__ = 'hospital'
    patientno = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    address = Column(String(50))
    age = Column(Integer)

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

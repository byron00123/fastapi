from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

engine = create_engine("sqlite:///db.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    gender = Column(String, nullable=False)

class CustomerSchema(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    gender: str

    class Config:
        orm_mode = True

class UpdateCustomerSchema(BaseModel):
    customer_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None

    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)

@app.get("/")
def get_root():
    db = SessionLocal()
    customers = db.query(Customer).all()
    db.close()
    return {"message": "Hello, GET request!"}

@app.get("/customer/{id}")
def get_one_customer(id: int) -> CustomerSchema:
    db = SessionLocal()
    single_customer = db.query(Customer).filter_by(customer_id=id).first()
    db.close()
    return single_customer

@app.post("/customer/")
def add_data(customer: CustomerSchema) -> CustomerSchema:
    db = SessionLocal()
    new_customer = Customer(**dict(customer))
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    db.close()

    return new_customer

@app.patch("/customer/update/{id}")
def update_customer(id: int, payload: UpdateCustomerSchema) -> CustomerSchema:
    db = SessionLocal()
    customer = db.query(Customer).filter_by(customer_id=id).first()
    
    for key, value in dict(payload).items():
        if value is not None:
            setattr(customer, key, value)
    
    db.commit()
    db.refresh(customer)
    db.close()
    
    return customer

@app.delete("/customer/delete/{id}")
def delete_customer(id: int) -> None:
    db = SessionLocal()
    customer = db.query(Customer).filter_by(customer_id=id).first()
    db.delete(customer)
    db.commit()
    db.close()
    
    return {"message": f"Customer {id} deleted"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional
# from customer import Customer, sessionmaker

# app = FastAPI()

# class CustomerSchema(BaseModel):
#     customer_id:int
#     first_name: str
#     last_name: str
#     email: str
#     gender: str

#     class Config:
#         orm_mode=True

# class UpdateCustomerSchema(BaseModel):
#     customer_id: Optional[int] = None
#     first_name: Optional [str] = None
#     last_name: Optional [str] = None
#     email: Optional [str] = None
#     gender: Optional [str] = None

#     class Config:
#         orm_mode=True

# @app.get("/")
# def get_root():
#     customer = session.query(Customer).all()
#     return {"message": "Hello, GET request!"}

# @app.get("/customer/{id}")
# def get_one_customer(id:int)->CustomerSchema:
#     single_customer = session.query(Customer).filter_by().first()
#     return single_student

# @app.post("/customer/")
# def add_data(customer: CustomerSchema)->CustomerSchema:
#     customer = Customer (**dict(customer))
#     session.add(customer)
#     session.commit()

#     return customer

# @app.put("/customer/")
# def put_root(put_data: PutData):
#     return {"message": f"Hello, PUT request! You sent: {put_data.put_data}"}


# @app.patch("/customer/update/{id}")
# def update_customer(id:int, payload:UpdateCustomerSchema )-> CustomerSchema:
    
#     customer = session.query(customer).filter_by(customer_id = id).first()
#     # breakpoint()
#     for key, value in dict(payload).items(exclude_unset = True).items():
#         setattr(customer, key, value)
#         session.commit()
#     return customer


# @app.delete("/customer/delete/{id}")
# def delete_customer(id : int)-> None:
#     customer = session.query(Customer).filter_by(customer-id).first().delete()
#     session.delete(customer)
#     session.commit()
#     return {"message": f"Customer, {id} deleted request"}
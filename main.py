from fastapi import FastAPI
from pydantic import BaseModel
from hospital import Hospital,session
from typing import List,Optional
app = FastAPI()
class HospitalSchema(BaseModel):
    patientno:int
    firstname:str
    lastname:str
    address:str
    age:int
    class Config:
        orm_mode=True
class UpdatedHospitalSchema(BaseModel):
    patientno:Optional[int]= None
    firstname:Optional[str]=None
    lastname:Optional[str]=None
    address:Optional[str]=None
    age:Optional[int]=None
    class Config:
        orm_mode=True   
@app.get('/')
def get_all() -> List[HospitalSchema]:
  patients = session.query(Hospital).all()
  return patients

@app.get('/patients{id}')
def get_single_patient(id:int) ->HospitalSchema:
  singlepatient = session.query(Hospital).filter_by(patientno=id).first()
  return singlepatient
# this is the route to add a new car with its details
@app.post('/add_patient')
def add_patient(hospital:HospitalSchema) ->HospitalSchema:
   inpatient=Hospital(**dict(hospital))
   session.add(inpatient)
   session.commit()
   return inpatient
  # this is the route for updating the whole existing car details
@app.put('/add_patient/{patient_id}')
def update_patient(patient_id:int,payload:UpdatedHospitalSchema) -> HospitalSchema:
  new_patient = session.query(Hospital).filter_by(patientno=patient_id).first()
  if new_patient is None:
    return {"error":"The patient has not been found"}
  for key,value in payload.dict().items():
    setattr(new_patient,key,value)
  session.commit()
  return new_patient
# this is the route for deleting a car and its details
@app.delete('/patient/delete{id}')
def delete_patient(id:int) -> None:
  adm_patient = session.query(Hospital).filter_by(patientno=id).first()
  session.delete(adm_patient)
  session.commit()
  return {"detail":f"Patient with the patientno {id} has succesfully been deleted"}

@app.patch('/patient/update/{id}')
def updating_patient(id:int,payload:UpdatedHospitalSchema) -> HospitalSchema:
  updated_patient = session.query(Hospital).filter_by(patientno=id).first()
  for key,value in payload.dict(exclude_unset=True).items():
    setattr(updated_patient,key,value)
  session.commit()
  return updated_patient   




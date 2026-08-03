from fastapi import APIRouter, Depends, HTTPException
from backend.models import Classroom, Child
from backend.schemas import ClassroomCreate, ClassroomResponse, ClassroomUpdate
from backend.database import getdb, Session, Select,selectinload
router = APIRouter(tags=["Classroom_V1"])

@router.post("/create_classroom")
def create_classroom(classroom:ClassroomCreate, db: Session = Depends(getdb)):
    name = db.scalars(Select(Classroom).where(Classroom.name == classroom.name)).first()
    if name:
        raise HTTPException(status_code=404, detail="Classroom Already Exists")
    new_classroom = Classroom(**classroom.model_dump())
    db.add(new_classroom)
    db.commit()
    db.refresh(new_classroom)
    return new_classroom


@router.patch("/update_classroom")
def update_classroom(classroom_data: ClassroomUpdate, classroom_id:int, db: Session = Depends(getdb)):
    classroom = db.scalars(Select(Classroom).where(Classroom.id == classroom_id)).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom Does Not Exist")
    update_dict = classroom_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(classroom, key, value)
    db.commit()
    db.refresh(classroom)
    return classroom

@router.get("/classroom/{id}", response_model=ClassroomResponse)
def get_classroom(id: int, db: Session = Depends(getdb)):
    classroom = db.scalars(Select(Classroom).where(Classroom.id == id)).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom Does Not Exist")
    return classroom

@router.get("/classrooms")
def get_all_classrooms(db: Session = Depends(getdb)):

    classroom_query = db.execute(Select(Classroom, Child.name).join(Child)).all()

    grouped = {}

    for room, child in classroom_query:
         if room not in grouped:
            grouped[room] = []
         grouped[room].append(child)
    results = [{"classroom": room, "children": names} for room, names in grouped.items()]
    
    return results
   
 

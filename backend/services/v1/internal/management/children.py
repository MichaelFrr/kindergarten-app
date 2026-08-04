from fastapi import APIRouter
from backend.models import Child, User, Classroom
from backend.schemas import ChildCreate, ChildResponse, ChildUpdate
from backend.database import getdb, Session, Select, or_
from fastapi import APIRouter, Depends, HTTPException
router = APIRouter(tags=["Child_V1"])
from uuid import UUID


@router.post("/create_child")
def create_child(child: ChildCreate, db: Session = Depends(getdb)):
    name_and_email = db.scalars(Select(Child).where(Child.parent_email == child.parent_email, Child.name == child.name)).first()
    parent = db.scalars(Select(User).where(User.email == child.parent_email)).first()
    classroom = db.scalars(Select(Classroom).where(Classroom.id == child.classroom_id)).first()
    if name_and_email:
        raise HTTPException(status_code=404, detail="Child Already Exists")
    if not parent:
        raise HTTPException(status_code=404, detail="Parent Does Not Exist")
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom Does Not Exist")

    
   
    new_child = Child(**child.model_dump(exclude={"parent_uuid"}), parent_uuid=parent.uuid)
    db.add(new_child)
    db.commit()
    db.refresh(new_child)
    return new_child

@router.patch("/update_child")
def update_child(child_data:ChildUpdate,parent_email:str, db: Session = Depends(getdb)):
    child = db.scalars(Select(Child).where(Child.parent_email == parent_email)).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child Does Not Exist")
    update_dict = child_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(child, key, value)
    db.commit()
    db.refresh(child)
    return child

# either add a check here to auto change the classroom capacity or an endpoint specefically to assign a child to a classroom

@router.get("/child/{data}")
def get_child(data, db: Session = Depends(getdb)):
    try:
        uuid_data = UUID(data)
    except (ValueError, TypeError):
        uuid_data = None

    query = Select(Child).where(or_(Child.parent_email == data, Child.uuid == uuid_data ))
    result = db.scalars(query).first()
    return result

@router.get("/children")
def get_children(db: Session = Depends(getdb)):
    children = db.scalars(Select(Child).join(Classroom)).all()
    return children
from sqlalchemy.orm import Session
from .models import IDRecord

# Create (Save new ID record)
def create_id_record(db: Session,id_number: str , full_name: str, dob: str, face_image: bytes):
    
    # Check if this ID already exists
    existing = db.query(IDRecord).filter(IDRecord.id_number == id_number).first()
    if existing:
        return None  
    
    record = IDRecord(
        id_number=id_number,
        full_name=full_name,
        dob=dob,
        face_image=face_image
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record



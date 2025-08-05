from sqlalchemy import Column, Integer, String, LargeBinary
from .database import Base

class IDRecord(Base):
    __tablename__ = "id_records"

    id_number = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    dob = Column(String, nullable=True)
    face_image = Column(LargeBinary, nullable=True)

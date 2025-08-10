from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from typing import List, Optional
from sqlalchemy.orm import Session
import shutil
import os
from . import crud, models, database, ocr_utils
import re
import base64

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency for DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-id/")
def upload_id(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from OCR
    text = ocr_utils.extract_text(file_path)

    # Filtering the text 
    temptxt = text.split("\n")
    filtered = [txt for txt in temptxt if "," in txt or ":" in txt]

    # Default values
    full_name = "Not detected"
    id_number = "Not detected"
    dob = "Not detected"

    for line in filtered:
        # Full Name
        if "," in line and any(c.isalpha() for c in line) and not any(c.isdigit() for c in line):
            parts = line.split(", ")
            if len(parts) == 2 and full_name == "Not detected":
                last_name = parts[0].strip()
                first_middle = parts[1].strip()
                full_name = f"{first_middle} {last_name}"

        # ID Number
        match_id = re.search(r"\b\d{10}\b", line)
        if match_id:
            id_number = match_id.group()

        # Date of birth
        match_dob = re.search(r"\b\d{2}/\d{2}/\d{4}\b", line)
        if match_dob and "DOB" in line.upper():
            dob = match_dob.group()

    # Detect face & crop
    face_path = os.path.join(UPLOAD_DIR, f"face_{file.filename}")
    face_crop = ocr_utils.detect_face(file_path, face_path)

    # Read face as bytes and convert to Base64
    face_base64 = "Not detected"
    if face_crop:
        with open(face_crop, "rb") as f:
            face_bytes = f.read()
            face_base64 = base64.b64encode(face_bytes).decode("utf-8")
    # Check for duplicate ID
    existing = db.query(models.IDRecord).filter(models.IDRecord.id_number == id_number).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"ID number {id_number} already exists in the database.")

    # Save to DB
    record = crud.create_id_record(db, id_number, full_name, dob, face_bytes if face_crop else None)

    return {
        "full_name": full_name,
        "id_number": id_number,
        "dob": dob,
        "face_image": face_base64  
    }


# ... existing imports & code ...

@app.get("/records")
def list_records(db: Session = Depends(get_db)):
    rows = crud.get_all_records(db)
    # Keep list payload small (no face bytes here)
    return [
        {
            "id_number": r.id_number,
            "full_name": r.full_name,
            "dob": r.dob,
            "has_face": r.face_image is not None
        }
        for r in rows
    ]

@app.get("/records/{id_number}/face")
def get_face(id_number: str, db: Session = Depends(get_db)):
    r = crud.get_record_by_id_number(db, id_number)
    if not r:
        raise HTTPException(status_code=404, detail="Record not found")
    if not r.face_image:
        raise HTTPException(status_code=404, detail="No face image for this record")
    # Return raw bytes as JPEG (works for <img src="data:..." but here we'll use blob URL)
    return Response(content=r.face_image, media_type="image/jpeg")

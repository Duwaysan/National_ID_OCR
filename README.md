# 🆔 National ID OCR

A full-stack application that extracts personal information and detects faces from national ID images using OCR (Optical Character Recognition).  
Built with **FastAPI**, **React**, and **SQLite**.

---

## Features
- Upload a national ID image
- Extract:
  - Full Name
  - ID Number
  - Date of Birth
- Detect face from the ID
- Store extracted data in a database
- User-friendly frontend built with React

---

## 🚀 Tech Stack

**Backend:**
- [Python 3.x](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) - API framework
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - Text extraction
- [OpenCV](https://opencv.org/) - Face detection
- [SQLAlchemy](https://www.sqlalchemy.org/) + SQLite - Database

**Frontend:**
- [React](https://react.dev/) - UI framework
- [Axios](https://axios-http.com/) - API requests
- CSS - Styling

**Database:**
- SQLite
---

### Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Duwaysan/National_ID_OCR.git
cd National_ID_OCR
```
### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```
### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm install concurrently --save-dev
```
### 4. Run Both Backend & Frontend Together
```bash
npm run dev
```

---

## **6️⃣ API Documentation**
Example:
```md
## API Documentation

### **POST /upload-id/**
Uploads a national ID image, extracts information, and stores it in the database.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (image file)

**Response Example:**
```json
{
  "full_name": "KHALID ABDULAZIZ S ALDUWAYSAN",
  "id_number": "1234567890",
  "dob": "06/12/2002",
  "face_image": "Face detected",
  "db_id": 1
}
---

---

## **7️⃣ Assumptions & Limitations**
```md
## Assumptions & Limitations
- Works best with high-quality scanned ID images
- Only detects faces on the **left side** of the ID
- Designed for IDs following a standard format
- Currently uses **SQLite**; can be upgraded to PostgreSQL or MySQL


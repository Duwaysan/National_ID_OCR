# 🆔 National ID OCR

A **full-stack web application** that extracts information from a **Saudi National ID card** using OCR (Optical Character Recognition) and Face Detection.  
Built for the HurryPay technical challenge.

---

## ✨ Features
- 📤 Upload ID card image (JPG/PNG)
- 🔍 Extract:
  - Full Name (reformatted correctly)
  - ID Number
  - Date of Birth
  - Cropped face image
- 💾 Store extracted data in a database
- 🖥️ Display results on a modern React web interface

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

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/National_ID_OCR.git
cd National_ID_OCR
```
2️⃣ Install Backend Dependencies
```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
deactivate

cd ../frontend
npm install
npm install concurrently --save-dev
```
3️⃣ Run the whole project
```
npm run dev
```

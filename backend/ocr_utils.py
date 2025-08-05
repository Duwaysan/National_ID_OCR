import cv2
import pytesseract
from PIL import Image
import numpy as np

#### Do it if tesseract not in your system path ####
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path: str):
    """Extract raw text from image using Tesseract OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def detect_face(image_path: str, save_path: str):
    """Detect and crop face from the left half of the ID image with extra top/bottom margins."""
    image = cv2.imread(image_path)
    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Image dimensions
    height, width = gray.shape

    # Define margins (10% top and bottom)
    top_margin = int(height * 0.1)   # 10% of height
    bottom_margin = int(height * 0.1)

    # Crop the left half including margins
    y1 = max(0, 0 - top_margin)  # start higher than top
    y2 = min(height, height + bottom_margin)  # extend below bottom
    x2 = width // 2  # middle of image

    left_half = gray[y1:y2, :x2]
    left_half_color = image[y1:y2, :x2]

    # Haarcascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(left_half, scaleFactor=1.1, minNeighbors=4)

    if len(faces) == 0:
        return None

    # Pick the largest detected face
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)

    for (x, y, w, h) in faces[:1]:
        # Add margin around the detected face
        margin = 50
        x1_face = max(0, x - margin)
        y1_face = max(0, y - margin)
        x2_face = min(left_half_color.shape[1], x + w + margin)
        y2_face = min(left_half_color.shape[0], y + h + margin)

        face = left_half_color[y1_face:y2_face, x1_face:x2_face]
        cv2.imwrite(save_path, face)
        return save_path

    return None
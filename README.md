# 📄 Document OCR Extraction

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Image_Processing-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This project automatically reads text from documents (such as invoices, receipts, and bank statements) and extracts key information — date, amount, and document number — saving the results to a CSV file.

One click: OCR + Regex + CSV output.

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Author](#-author)

## ✨ Features

- **Text recognition (OCR):** Reads text in both Turkish and English using EasyOCR
- **Information extraction:**
  - Date (e.g. `12.05.2024`)
  - Amount (e.g. `1450.75 TL`)
  - Document / invoice number
- **Regex-based pattern matching:** Smart pattern search within extracted text
- **Result logging:** Extracted data from all documents is saved to `extracted_data.csv`
- **Bounding-box preview:** Detected text regions are highlighted on the image

## 🛠 Tech Stack

- Python 3.9+
- EasyOCR
- OpenCV
- Pandas
- Regex (`re` library)

## 🚀 Getting Started

1. Install the required libraries:

```bash
pip install easyocr opencv-python pandas
```

2. Set up the folder structure:

```
document-ocr-extraction/
├── documents/              → Folder containing the images to be processed
├── main.py                 → Main Python script
└── extracted_data.csv      → Output file (generated automatically)
```

3. Add your images:
   Place `.jpg`, `.jpeg`, or `.png` files inside the `documents/` folder.

4. Run the OCR process:

```bash
python main.py
```

The extracted information will be automatically saved to `extracted_data.csv`.

## 👤 Author

**Sedanur Peker**

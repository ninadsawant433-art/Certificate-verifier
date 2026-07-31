# 🔐 Blockchain-Based Certificate Verification System

A cyber-security focused web application that verifies the authenticity of existing digital certificates using **Blockchain**, **SHA-256 hashing**, **QR code extraction**, and **website security validation**. The system detects tampered certificates, identifies the issuing authority, and validates the credibility of the issuer's website to prevent phishing attacks.

---

## 🚀 Features

- 📄 Upload certificate (PDF)
- 🔍 Extract QR code from certificate
- 🔐 Verify certificate integrity using SHA-256 hashing
- ⛓️ Verify certificate details through Blockchain (Ethereum)
- 🌐 Identify the original issuing website
- 🛡️ Validate HTTPS and SSL certificate
- 🚫 Detect phishing or fake verification websites
- 📊 Display certificate trust score and verification report

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Flask

### Database
- MongoDB

### Blockchain
- Ethereum
- Web3.py
- Solidity Smart Contract

### Libraries
- OpenCV
- PyZbar
- PDF2Image
- Flask-PyMongo
- Cryptography
- Requests

---

## 📂 Project Structure

```
CertVerifier/
│
├── static/
├── templates/
├── uploads/
├── app.py
├── main.py
├── blockchain_module.py
├── input_module.py
├── website_module.py
├── CertificateVerifier_abi.json
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/CertVerifier.git
cd CertVerifier
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 Required Python Packages

```bash
pip install flask flask-pymongo pymongo web3 opencv-python pdf2image pyzbar pillow requests cryptography python-dotenv
```

---

## 📑 Poppler Installation (Windows)

This project uses **pdf2image** to convert PDF certificates into images.

1. Download Poppler:
https://github.com/oschwartz10612/poppler-windows/releases

2. Extract it.

3. Update the Poppler path inside `input_module.py`.

Example:

```python
POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"
```

---

## ▶️ Running the Project

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## 🔄 Verification Workflow

```
Upload Certificate
        │
        ▼
Convert PDF to Image
        │
        ▼
Extract QR Code
        │
        ▼
Identify Issuing Website
        │
        ▼
Blockchain Verification
        │
        ▼
SSL & Domain Validation
        │
        ▼
Generate Verification Report
```

---

## 📸 Screenshots

### 🏠 Home Page

![Home Page](screenshots/home.png)

---

### 📄 Upload Certificate

![Upload](Screenshots/Upload_Certificate.png)

---

### ✅ Verification Result

![Result](screenshots/result.png)


---

## 🔒 Security Features

- SHA-256 Hash Verification
- Blockchain-based Certificate Validation
- QR Code Authentication
- HTTPS Verification
- SSL Certificate Validation
- Domain Matching
- Phishing Detection
- Tampering Detection

---

## 📈 Future Enhancements

- IPFS Integration
- Multi-Issuer Support
- AI-based Phishing Detection
- Mobile Application
- Government Certificate Integration

---

## 👨‍💻 Author

**Ninad**

Masters of Computer Application

---

## 📄 License

This project is developed for educational and research purposes.
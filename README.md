# 🔒 Quantum Lock Chat

![bd1d649021654f8f9a9059e02a7c1278](https://github.com/wahidpanda/Encryption-Decryption-Quantum-Computing-Project/assets/110899864/308ffc4d-a941-40a4-a880-7c1c72c727b9)

Quantum Lock Chat is a **secure messaging and image encryption app** built using **Streamlit** and **Qiskit**, implementing **Quantum Key Distribution (QKD)** via the BB84 protocol. It allows users to:

- Register/Login with secure credentials
- Exchange quantum keys
- Encrypt and decrypt text messages and images
- Generate QR codes for shared quantum keys

## 🚀 Features

### 🔐 User Authentication
- Secure registration and login system
- Stores credentials in a CSV file (`user_credentials.csv`)

### ⚛️ Quantum Key Distribution (BB84 Protocol)
- Simulates BB84 protocol using Qiskit and QASM simulator
- Generates a shared key between two users based on random bases

### ✉️ Message Encryption
- Uses XOR encryption with quantum key
- Encrypts and decrypts messages based on generated keys
- Displays shared key as a QR code

### 🖼️ Image Encryption
- Encrypts and decrypts images using the quantum key
- Works on PNG/JPG/JPEG formats
- Decryption is performed via XOR (same as encryption)

### 📸 QR Code Generation
- Generates a QR code of the shared key
- Makes key sharing more user-friendly

---

## 🛠️ Technologies Used

- **Python 3**
- **Streamlit** for the web interface
- **Qiskit** for simulating quantum circuits
- **PIL (Pillow)** for image processing
- **NumPy** for numerical operations
- **qrcode** for QR code generation
- **CSV** for credential storage

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/quantum-lock-chat.git
   cd quantum-lock-chat

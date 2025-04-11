import streamlit as st
from PIL import Image
import numpy as np
import csv
import os
import qrcode
import io
from qiskit import QuantumCircuit, Aer, execute

# Function to create a CSV file to store user credentials
def create_credentials_file():
    with open("user_credentials.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password"])

# Function to register a new user
def register_user(username, password):
    with open("user_credentials.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    st.success("Registration successful. Please log in.")

# Function to check if a user exists in the CSV file and if the password matches
def login_user(username, password):
    with open("user_credentials.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}! You are now logged in.")
                return True
    st.error("Invalid username or password. Please try again.")
    return False

# Quantum BB84 key exchange using Qiskit
def bb84_qiskit_key_exchange(n=100):
    alice_bits = np.random.randint(2, size=n)
    alice_bases = np.random.randint(2, size=n)
    bob_bases = np.random.randint(2, size=n)
    bob_results = []

    for i in range(n):
        qc = QuantumCircuit(1, 1)

        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 1:
            qc.h(0)
        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure(0, 0)

        backend = Aer.get_backend('qasm_simulator')
        result = execute(qc, backend, shots=1).result()
        measured_bit = int(list(result.get_counts().keys())[0])
        bob_results.append(measured_bit)

    sifted_key = [alice_bits[i] for i in range(n) if alice_bases[i] == bob_bases[i]]
    return sifted_key

# Encrypt message using XOR with the shared key
def encrypt_message(message, key):
    encrypted_message = ''.join(chr(ord(message[i]) ^ key[i % len(key)]) for i in range(len(message)))
    return encrypted_message

# Decrypt message using XOR with the shared key
def decrypt_message(encrypted_message, key):
    decrypted_message = ''.join(chr(ord(encrypted_message[i]) ^ key[i % len(key)]) for i in range(len(encrypted_message)))
    return decrypted_message

# Generate QR code for the shared key
def generate_qr_code(shared_key):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )
    qr.add_data(shared_key)
    qr.make(fit=True)
    img = qr.make_image(fill_color="green", back_color="white")
    return img

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔒 Quantum Lock Chat")
        st.subheader("Encrypt your messages with real Quantum Key Distribution (QKD)")
        st.image("https://image.binance.vision/editor-uploads/bd1d649021654f8f9a9059e02a7c1278.gif", use_column_width=False, width=700)
        st.sidebar.title("Authentication")

        option = st.sidebar.radio("Choose an option", ("Login", "Register"))
        if option == "Register":
            new_username = st.sidebar.text_input("Username")
            new_password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Register"):
                register_user(new_username, new_password)
        elif option == "Login":
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Login"):
                login_user(username, password)

    elif st.sidebar.button("Logout"):
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.title("Navigation")
        navigation_option = st.sidebar.radio("Go to:", ("Secure Chat Interface",))

        if navigation_option == "Secure Chat Interface":
            st.subheader("Secure Chat Interface")
            st.write(f"Welcome to the Secure Chat Interface, {st.session_state.username}!")

            message_to_send = st.text_area("Type your message here to send:")
            if st.button("Send Message"):
                st.success("Message sent successfully!")
                shared_key = bb84_qiskit_key_exchange(len(message_to_send))
                encrypted_message = encrypt_message(message_to_send, shared_key)

                qr_code_img = generate_qr_code(''.join(map(str, shared_key)))
                img_byte_arr = io.BytesIO()
                qr_code_img.save(img_byte_arr, format='PNG')
                st.image(img_byte_arr, caption="QR Code for Shared Key", use_column_width=True)

                st.session_state.message_sent = message_to_send
                st.session_state.shared_key = shared_key
                st.session_state.encrypted_message = encrypted_message
                st.session_state.encrypted_message_sent = True

            if "encrypted_message_sent" in st.session_state and st.session_state.encrypted_message_sent:
                st.write("Encrypted Message:", st.session_state.encrypted_message)
                st.write("Shared Key:", ''.join(map(str, st.session_state.shared_key)))

            encrypted_message_received = st.text_input("Enter the encrypted message received:")
            shared_key_received = st.text_input("Enter the shared key received:")
            if st.button("Decrypt Message"):
                if encrypted_message_received:
                    decrypted_message = decrypt_message(encrypted_message_received, list(map(int, shared_key_received)))
                    st.write("Decrypted message:", decrypted_message)
                    st.success("Message decrypted successfully!")
                else:
                    st.error("Please enter a valid encrypted message.")

if __name__ == "__main__":
    main()

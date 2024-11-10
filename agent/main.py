import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, db
from scapy.all import sniff, IP, TCP, UDP, ICMP
import time
from datetime import datetime
import re
import threading

# Initialize Firebase Admin SDK
print("Initializing Firebase Admin SDK...")
# Define the service account credentials inline as a dictionary
service_account_file = {
  "type": "service_account",
  "project_id": "cs-challenge-f4c13",
  "private_key_id": "a1478fe1afefa5186709ab660704710e01d56ba4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDUwipwsQlDodZG\n3WOCsYmBZeh5fMxlKOsh05G3NYJ4E7FKEAqWo16aKhJx3lO+VSfWg7vAOchbGyD6\n/SNLPQ+dkpmtHKpwW+2n8qmdWC5YDIIhRd+/C8v5FPk8404iwGp+ER28qi7PKZsO\nX+0K8tQxLnEifaYITJhqYRIkf+NQpd8l1Ec7Nc6HVhXoys9NLsYepXwR9ZyHUD1J\n00ihYoBrk4/ADR04o32gIz6jnpXbEswWfyCK0npKnZYxDZLU+EBcvNE4+i9Hj6Y5\nzDV71yyiiM6piJ1ustCWOy8ayBABKRQ2NFEmrvJhz90IwLY2BlMCa5WGC6J/s5+a\n6mu2uwZ/AgMBAAECggEAOcuhEcnV1WyCM+/yF0+5JdCULWRsddJ+xUqe2+EKVyoq\nUA85gSBSE5j4N7yIjTy+vLQ+bYKE3dLpy6S2ULr+ofRwEKmn1yvxzFzMHLUWqc6E\nDxvXIyPGPhyndBXfZOtWQnbN2DF208nemDIQx5edctrF2vO9BaYhBUznS8j97CsU\nLHUYI/X3xLgbk5OP9tUnpkxMsvEmpbgCidv27Yf6aFkI4Db1no8ZNkx08CfC6ieQ\n4kKp6IDdZHd/4JdhRXtRNrlAikKVpIyyh5/Q1b7oiAqRMW9kIPHq6EYcqLO2p7np\ncc22T/fCypo6DgyaqltWde2ZF4xWzsmXOAbSthOxIQKBgQDxRj6JSobIJspFcD0z\nmNVAW/jWhuS3Q6k1B8Xp3DgZaGRdecH9fafrAU0/v+Fw2WvJSC0DTdDEZMlCD7r5\nHPpQZx0yNyZbXZCWqUrLsWQxT1KsZiHC4IH3CIYaYcJxKv1sQGlR3xRaab3Z32+S\nXtcazhsDTZlStv29M5bkG+YU0QKBgQDhvmDqxmRInTN56QdEJ+NYEege51AzUY/+\nEJREra9ixAmExEo0vvSdxfeyspuq989RATPJA7xqsA0fg49092lxj+yeva5FCVMY\nEpQSRLyoqE76eZNhFgxxWzEIt+x60uJCmjiu36NpasMECNpL9dAdkcuwYwSw299t\nTToJ1596TwKBgQDocyik1OxtwRF3PN956nDqBLIE3QlVlxZaRRbkbIqP0AeCF2BS\nfNFelG58UL0+H/q8fZEAceQEkqVjxAv7HXP8KpvyWTfXJpm6zXeGL228JBQejHdS\nbUJJYijxGeZfaW+m75eIjUfqo52JXr77YewToyZbVFO3YR2tPxrMwiQ1QQKBgD5G\n5zXdxYzC0ZCwWPDUkEObrQ3ZgqalubO9nynTQK9epcGa5V3n0FQ2aT9DRu7Drs4K\nJt8tyK0mJHitMsZx+wT5T637ZjhleicJ+Q+RJvrgc+ll4OLH0mbzYXOmSfcYdpMp\nOLoFuG88pNBYIOETz3ZY4nim2IRyJBFjXL+aXMTBAoGBANIq+GTgAQsAK/kNojMa\nDi14ErFjQWmmhX+ZeuMbMOpaZOU9WewT5N/3hzWhftmEr/fuF83FyPo5V3xXJ4NN\n3+M+eeFSVO3fmt6ZCdSZEraf2cBnpfgSdutRUvRD328MtyXR2KtP+EGR1PCP4aSZ\nSIQuuzEKnWV0HQ2myeC9BxAE\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-1ijdj@cs-challenge-f4c13.iam.gserviceaccount.com",
  "client_id": "112764959389897975827",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-1ijdj%40cs-challenge-f4c13.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_file)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cs-challenge-f4c13-default-rtdb.firebaseio.com/'
})
print("Firebase Admin SDK initialized.")


# Initialize metrics and descriptions for both sets of features
metrics = {
    "dur": 0, "sbytes": 0, "dbytes": 0, "Sload": 0, "swin": 0, "smeansz": 0, "Sjit": 0, "Stime": 0,
    "tcprtt": 0, "ct_srv_src": 0, "ct_srv_dst": 0, "ct_dst_ltm": 0, "ct_src_ltm": 0, "ct_dst_src_ltm": 0,
    "duration": 0, "byte_ratio": 0, "jit_ratio": 0, "inter_pkt_ratio": 0, "tcp_setup_ratio": 0,
    "total_load": 0, "byte_pkt_interaction_dst": 0, "load_jit_interaction_dst": 0, "tcp_seq_diff": 0,
    "Dst Port": 0, "Protocol": 0, "Fwd Pkt Len Min": 0, "Fwd Pkt Len Std": 0, "Bwd Pkt Len Min": 0,
    "Flow Byts/s": 0, "Flow IAT Mean": 0, "Flow IAT Std": 0, "Flow IAT Min": 0, "Fwd IAT Std": 0,
    "Bwd IAT Std": 0, "Bwd IAT Max": 0, "Bwd IAT Min": 0, "Fwd PSH Flags": 0, "Fwd URG Flags": 0,
    "Bwd Header Len": 0, "Bwd Pkts/s": 0, "Pkt Len Min": 0, "FIN Flag Cnt": 0, "RST Flag Cnt": 0,
    "PSH Flag Cnt": 0, "ACK Flag Cnt": 0, "URG Flag Cnt": 0, "Down/Up Ratio": 0, "Pkt Size Avg": 0,
    "Fwd Seg Size Avg": 0, "Bwd Seg Size Avg": 0, "Init Fwd Win Byts": 0, "Init Bwd Win Byts": 0,
    "Fwd Act Data Pkts": 0, "Fwd Seg Size Min": 0, "Active Std": 0, "Active Max": 0, "Active Min": 0,
    "Idle Std": 0, "Idle Max": 0, "Idle Min": 0
}

# Track additional details for computation
start_time = time.time()
packet_times = [] 
src_packet_sizes = []  
src_ip = None  
dst_ip = None  

# Initialize user_id as a global variable
user_id = None
user_full_name = None

# Function to save data to Firebase under the new structure
def save_to_firebase(data, user_id):
    date_key = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp for the key
    ref = db.reference(f'/userData/{user_id}/userTraffic/{date_key}')
    sanitized_data = sanitize_data(data)
    ref.set(sanitized_data)  # Use `set` for a specific key
    print(f"Data saved to Firebase for {date_key}")

# Function to sanitize data
def sanitize_data(data):
    sanitized_data = {}
    for key, value in data.items():
        sanitized_key = re.sub(r'[$#\[\]/.]', '', key)
        if value not in [None, ''] and isinstance(value, (int, float, str)):
            sanitized_value = re.sub(r'[$#\[\]/.]', '', str(value)) if isinstance(value, str) else value
            sanitized_data[sanitized_key] = sanitized_value
    return sanitized_data

# Function to validate metrics (ensure no empty values)
def validate_metrics(metrics):
    valid_metrics = {}
    for key, value in metrics.items():
        if value not in [None, '']:
            valid_metrics[key] = value
    return valid_metrics

# Function to authenticate user
def authenticate_user(email, password):
    users_ref = db.reference('/userData')
    users = users_ref.get()
    
    for user_id, user_data in users.items():
        if user_data['email'] == email and user_data['password'] == password:
            return user_id
    return None

# Function to handle packet capturing and processing
def packet_callback(packet):
    global metrics, start_time, packet_times, src_packet_sizes, src_ip, dst_ip, user_id
    try:
        metrics["dur"] = time.time() - start_time
        metrics["duration"] = metrics["dur"]
        packet_time = time.time()
        packet_times.append(packet_time)

        if packet.haslayer(IP):
            ip_layer = packet[IP]
            if not src_ip:
                src_ip = ip_layer.src
            if not dst_ip:
                dst_ip = ip_layer.dst
            if ip_layer.src == src_ip:
                metrics["sbytes"] += len(packet)
                src_packet_sizes.append(len(packet))
            else:
                metrics["dbytes"] += len(packet)

            metrics["Dst Port"] = ip_layer.dport if hasattr(ip_layer, 'dport') else 0
            metrics["Protocol"] = ip_layer.proto

        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            if ip_layer.src == src_ip:
                metrics["swin"] += tcp_layer.window
            if tcp_layer.ack and tcp_layer.seq:
                metrics["tcprtt"] = abs(tcp_layer.ack - tcp_layer.seq)
            if tcp_layer.flags == "S":
                metrics["tcp_setup_ratio"] += 1

        elif packet.haslayer(UDP):
            udp_layer = packet[UDP]
            metrics["Flow Byts/s"] = len(packet)

        elif packet.haslayer(ICMP):
            icmp_layer = packet[ICMP]

        metrics["Sload"] = metrics["sbytes"] / metrics["dur"] if metrics["dur"] else 0
        if src_packet_sizes:
            metrics["smeansz"] = sum(src_packet_sizes) / len(src_packet_sizes)
        if len(packet_times) > 1:
            inter_arrival_times = [packet_times[i+1] - packet_times[i] for i in range(len(packet_times)-1)]
            metrics["Sjit"] = sum(inter_arrival_times) / len(inter_arrival_times) if inter_arrival_times else 0
        else:
            metrics["Sjit"] = 0
        if len(packet_times) > 1:
            metrics["Stime"] = packet_times[-1] - packet_times[-2]
        else:
            metrics["Stime"] = 0

        metrics["byte_ratio"] = metrics["sbytes"] / metrics["dbytes"] if metrics["dbytes"] else 0
        metrics["total_load"] = metrics["sbytes"] + metrics["dbytes"]
        metrics["byte_pkt_interaction_dst"] = metrics["dbytes"] / len(packet_times) if len(packet_times) else 0
        metrics["load_jit_interaction_dst"] = metrics["Sload"] * metrics["Sjit"] if metrics["Sjit"] else 0
        metrics["tcp_seq_diff"] = abs(tcp_layer.seq - tcp_layer.ack) if packet.haslayer(TCP) and tcp_layer.ack else 0

        print(f"Current Metrics: {metrics}")
        validated_metrics = validate_metrics(metrics)
        save_to_firebase(validated_metrics, user_id)

    except Exception as e:
        print(f"Error processing packet: {e}")

# Function to start packet capture for a short time (e.g., 2 seconds)
def capture_traffic():
    print("Starting packet capture for a few seconds...")
    sniff(filter="ip", prn=packet_callback, timeout=2)  # Capture for 2 seconds

# Function to initiate capture every minute
def start_network_capture_periodically():
    capture_traffic()  # Perform capture once
    threading.Timer(60, start_network_capture_periodically).start()  # Schedule next capture after 60 seconds

# Tkinter GUI
def show_welcome_screen():
    welcome_label.pack_forget()
    login_frame.pack_forget()

    welcome_message = tk.Label(root, text=f"Welcome, {user_full_name}!", font=("Arial", 14))
    welcome_message.pack(pady=20)

    start_button = tk.Button(root, text="Start Packet Capture", command=start_network_capture_periodically, font=("Arial", 12))
    start_button.pack(pady=20)

def on_login():
    global user_id, user_full_name
    email = email_entry.get()
    password = password_entry.get()
    user_id = authenticate_user(email, password)

    if user_id:
        user_ref = db.reference(f"/userData/{user_id}")
        user_data = user_ref.get()
        user_full_name = user_data['fullName']
        show_welcome_screen()
    else:
        messagebox.showerror("Login Failed", "Invalid email or password.")

root = tk.Tk()
root.title("Network Capture and Firebase App")
root.geometry("400x300")

# Create Login Frame
login_frame = tk.Frame(root)
login_frame.pack(pady=50)

email_label = tk.Label(login_frame, text="Email")
email_label.grid(row=0, column=0, padx=10, pady=10)

email_entry = tk.Entry(login_frame)
email_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(login_frame, text="Password")
password_label.grid(row=1, column=0, padx=10, pady=10)

password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="Login", command=on_login)
login_button.grid(row=2, columnspan=2, pady=20)

# Initial welcome message
welcome_label = tk.Label(root, text="Welcome! Please login", font=("Arial", 14))
welcome_label.pack(pady=20)

root.mainloop()

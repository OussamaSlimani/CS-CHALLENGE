import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, db
from scapy.all import sniff, IP, TCP, UDP, ICMP
import time
from datetime import datetime
import re
import threading

# Define the service account credentials inline as a dictionary
service_account_file = {
    "type": "service_account",
    "project_id": "cs-challenge-f4c13",
    "private_key_id": "b216133fd8711cb657641b7ca6b2f32eceb3cf29",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxEx1o6+TX8mrD\nyBSW8fBlK+J0BZgdYKmKorL+soOLwZ4iGR3PnVKJZzYoVAdM0cv4/oVosd7nhc05\nVHgcL03CiQiHOubC969PvTVy8eJHHkwgky+hbZAsIA7FBgQ/4yGK1O98mk9MsRy4\nTvOK0v+ZTy2vhSHlkN7YVFX92BSSZqHltu4rsBClHo0pOuCxybqSaOYuREO9ObQg\nwMDenY187Pu4CL0H0u2mPTdBBrZDwgSLxilPcjv6G4lBQCCLKLCKNB+YIJ/llBEb\nrRFGT52SWarAIoCUW7l6iWhSlWXufyirvDKjnE7PhHo4X1iC1IR61E0Dzt2mYah4\nwKh50tEfAgMBAAECggEAPNB/zUUW90N+f3b7+0tkcJq9z3MMZyqHj+GI8AiHPTxl\n/vf5URCLBD26T+dsCmoTT5S6ZNaR45oEfagRCD0Gy8UcdLU6A8PlJdGpxaxlNl+l\nbZqfRSXH2h+4cto6I2byYif3iCfHDGPXpUUYR5lnx1N2MU3b8mfq4Qk171SC3DRn\nqUVRVfwcm4QfUtJAyrCli00umFJo7e1USmxa42BuXl6ubl1IjjReipbnKVraxS7c\nWYGY0LrovHgBxvERBj7vin7gGPUE2T6mmOou6+Hn6nkImc8SXwYYiI2uCv0PrsaK\ns3Bjsg8xlBPc25vAcTPxBUuWAzYT8yLciNEKb0Z2gQKBgQD166NfdSlk1Yo+DaNg\n1xuoMnfLodh73F91oId9DTjEKrW4ydWxOqLanAK3HyG3yj91hkmxkFLn5xsu2syh\nvYq8F6KbK8trws/316GiHVvNGwBpjseYijvOjSi+f/PjttThwgCaX9Ce6gETtwP3\ne2yMkkqHlkdqjsYLFYR1iJ8OEQKBgQC4VRnCuL0lA3sSkOfBxAHTRh18NYOmwRJE\nyDB4L4fMM3MIXdjjLiwnQGWE0MENNu6uxdEP2uxENBz9SLXrFsX4WAR0F6dwHi09\nQdoenEXMabB6nt15jdPDoo8J5oW581oZH2G05ha2XXePo4RHRJeq02vvNLR0H/Js\nQbujid98LwKBgQDx4gT+ZlIBsRvZbzaskMfOR12XOCijo51tKCk78d5M7KlzCWsb\neE4ocd0l2wQiL1b9tMkVUpyJJsKQ8nrl93XXDfRNZeUeqC5AW6LKvs/FzPI54Usn\nGYg74JIb1eTArNt09on7TZT4SbgneRL4wDiDh3yxIjo6cBYRXue7Z1by0QKBgQCP\nRrZrQCTkrDvxRmidl7jDe3BXp1DZQKDujZv/DxLCigsTqb53duAi8k72WTx1BQmp\nF2FUrZmPueH+jZG5VU4zplZv1iLzZsFLJ/BecqFeLZha9zi2zqKXIbeEvoWa76hM\ndrP/ZAirXyMbpsGek5Y/1W3D1Hee+2X293DdwMDRSQKBgFA30ACXMVqdImSVbEUn\nRBRPBV1FxK3dfxGhVC2H7yliM7+yTahTwW7G+fkRhxh6SAoTG8BPvo+FojYv3ahL\neaoiMfo/VYFT098WlV4aCtilwNF4NFf4oZqdeLcMuejZ18u9TN9uiHVrzFmq6Nne\nxRy+vD+kJHCvu7t2O2RkUvlI\n-----END PRIVATE KEY-----\n",
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

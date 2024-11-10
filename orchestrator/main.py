import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import subprocess
import threading
import time

# Firebase service account credentials
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

# Initialize Firebase
cred = credentials.Certificate(service_account_file)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cs-challenge-f4c13-default-rtdb.firebaseio.com/'
})

user_id = None  # Stores the logged-in user's ID
user_full_name = None

def run_powershell_command(command):
    """Execute a PowerShell command and return output."""
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    return result.stdout

def close_port(port_number):
    command = f"Set-NetFirewallRule -DisplayName 'Block Port {port_number}' -Direction Inbound -Action Block -LocalPort {port_number} -Protocol TCP"
    output = run_powershell_command(command)
    print(f"Closed Port: {port_number}\n{output}")
    return f"Port {port_number} has been closed."

def block_ip(ip_address):
    command = f"New-NetIPAddress -IPAddress {ip_address} -PrefixLength 32 -InterfaceAlias 'Ethernet' -PolicyStore PersistentStore"
    output = run_powershell_command(command)
    print(f"Blocked IP: {ip_address}\n{output}")
    return f"IP {ip_address} has been blocked."

def update_system():
    command = "Install-WindowsUpdate -AcceptAll -AutoReboot"
    output = run_powershell_command(command)
    print(f"System Update: {output}")
    return "System update initiated."

def authenticate_user(email, password):
    users_ref = db.reference('/userData')
    users = users_ref.get()
    for uid, user_info in users.items():
        if user_info['email'] == email and user_info['password'] == password:
            return uid, user_info['fullName']
    return None, None

def execute_pending_commands():
    global user_id
    user_ref = db.reference(f"/userData/{user_id}/commands")
    commands = user_ref.get()
    
    if commands:
        for command, details in commands.items():
            if not details.get("execute"):
                if command == "close_port":
                    result = close_port(details.get("port"))
                elif command == "block_ip":
                    result = block_ip(details.get("port"))
                elif command == "update_system":
                    result = update_system()
                else:
                    result = "Unknown command."
                
                messagebox.showinfo("Command Executed", result)
                
                # Update execute status to True in Firebase
                user_ref.child(command).update({"execute": True})

    threading.Timer(60, execute_pending_commands).start()

def show_command_screen():
    login_frame.pack_forget()

    # Create a new frame for the command screen
    command_frame = tk.Frame(root)
    command_frame.pack(pady=20)
    
    # Welcome message with user name
    welcome_label = tk.Label(command_frame, text=f"Welcome, {user_full_name}!", font=("Arial", 14))
    welcome_label.pack(pady=(0, 10))

    # Instruction label
    instruction_label = tk.Label(command_frame, text="You can close this tab after starting", font=("Arial", 12), fg="gray")
    instruction_label.pack(pady=(0, 20))

    # Button to start orchestration
    run_button = tk.Button(command_frame, text="Start the orchestration", command=execute_pending_commands, font=("Arial", 12), bg="#4CAF50", fg="white")
    run_button.pack()

def on_login():
    global user_id, user_full_name
    email = email_entry.get()
    password = password_entry.get()
    user_id, user_full_name = authenticate_user(email, password)

    if user_id:
        show_command_screen()
    else:
        messagebox.showerror("Login Failed", "Invalid email or password.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Command Execution App")
root.geometry("400x300")

# Login Frame
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

root.mainloop()

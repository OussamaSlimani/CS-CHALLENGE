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

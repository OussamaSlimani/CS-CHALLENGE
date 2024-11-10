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
  "private_key_id": "ef9732619d6dcbe8581a206ce10c1dfb215c0299",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDBjLBbW8CJ1W1B\nFsEVRc0NMN/JjXcnYjrTuZ50dHdXdArTTYtPabqbvVmnBX+XQwvlF1eo0MmVn6Nu\nJCNr27Y+C95W+Ai75unH0tzsDOjBqnA7bbp+uHzb0ZxRIAE9CB8HvMIC7pW0ra6r\nrMEncBxF0jAEqt09ar5TOetSfOZKcp6xPNYH9HZTNriRg1t6+1bvIA3pZ3Vrgnmt\nbNoNQZmH6KRmoKrHcHqbxRX4BahN8Eq5H0fWnKDmDeLozVZYGBi5bgiaTDqbjvqL\nRDsd0XJDCe73uIDP95/Pd2PX1lWabsDCpmMV0VqR5MwZWKoUiVKTdUziE0BpqIgs\nwIBYBjCnAgMBAAECggEABUwJNF1GeUwGBj00Yfvb2/vCcPNJZFW9fNEced0JU+aX\nhUDro+vycRPowdFv57JGDEPSeld8eao5mgITL7IYdfCm0FDpeRSdjhwPP8aURPiZ\n9oZoqQWTi51cK29pmUOa1cz5e+sO3dFpcZLz/LuGV1xxQ/w8VQbFPrHb5t4HaQu9\ntsKXSxn9kGnN23RFA5OoaBQQXT2LTjJI0ykYVJBuyIBcpLIydTwoEVG2zQSKZu7v\nUQJS4Wy4LV8OiZo80n3xpCtejgg6pgkmcucJX13K0MsaVRMHqgdNQl20J747hcMI\ntfixffot52ZW8Ov0cxtCGS1sFp8BWngkREgnXkySQQKBgQD+3G4tWUU/EtsBFuAs\nsDerXCmZCUMbvaBoco4WxFtoIqt9/qaKR3btxQOcjuAy87QFp1oYe1qbkSFX+Zom\nxd7+4RhxfR1iC1dWmcCv/JBNhRoqVv2kUpHHmZYXyG2Oa6hL+W//3izIOiqMzEgh\n+DWfLZp4tT9I5/oXPlqVA2rZRQKBgQDCah25Oc4txgsfF63ZZ46Tv1AkTdQdipoK\n+NOIA9LCu3SYGKuwc9c5KPEvmcS2oGG+VzAw4HQIdXYlrGfvaPNQzvDyt7umzGvA\n0wsKVIcrVo4Jkc5IA5jfR7oAJlyqS4b1q41436dxdfOTchp/kRCAwJXLmuqUL0F2\nPMhICkgi+wKBgQCPP46d5qNJRGvcPONbuuBPbMnkvpP9r6PNkTXUDiHicjo54zvw\nVSK/mhDhmlzhxqDU3K+DOzI+ZmB7dkvypx0j3ZlDkLNHPGCmyFzJjgf9ymZeje6a\nwd42dlkqnPkXJ+O8cENHabV6BVeNM/UHQt/AzH0ag6VCcUDcd6uqPfV8kQKBgQC+\nAZ4pMDCsldi6u5bCWq6DAcBeqt37PUHOJV//l9T9Ut3h5IKwApc/Gx+VaRBTeK3u\nrCHCMyvUNJCSw0wVNRpQSOA+J4mzvCg3nUs1/mTY21AYVDMqOLHIzr4fdV6tZQFy\nywaKMvPgNOoomaUCNhHN8+qywiYvS3wMBd2sYrgbzwKBgQC1ij1qWtTjtu3OwpK0\ncoIgOJAAFX99mvOVsV1LOgBeAayyWdeUT1vRKZKsdl+Q2bmYrfvSZ6AOtF2zBPKh\n10uTm768EM+4/GkyCWJvFZmdoTw9wdsrJ/YqDdLgZ5ukLGgtABxwCI2tTRY7ErUE\nl6Z7fdne5GipPTwzBUhsc0tRWA==\n-----END PRIVATE KEY-----\n",
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

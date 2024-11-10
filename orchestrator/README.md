# Command Execution App

A Tkinter-based Python app that lets users log in and execute commands, like closing ports, blocking IPs, and updating the system. User commands are stored in Firebase Realtime Database and are executed periodically.

## Features

- **Close Ports**: Blocks specified ports on the system.
- **Block IPs**: Blocks specified IP addresses.
- **System Updates**: Triggers system updates via PowerShell.
- **Command Management**: Monitors and executes pending commands from Firebase.

## Requirements

- **Python 3.8+**
- Packages: `firebase-admin`, `tkinter`

## Installation

**Install Dependencies**:

```bash
 pip install firebase-admin
```

**Firebase Setup**:

- Set up a Firebase project and download the Admin SDK JSON file.
- Replace the `service_account_file` with your Firebase credentials in the code.

**Run the App**:

```bash
python app.py
```

## Usage

1. **Run** `app.py` to start the GUI.
2. **Log in** using a valid email and password stored in Firebase.
3. **Execute Commands**:

   - The app fetches pending commands from Firebase and executes them every 60 seconds.
   - Supported commands include port closure, IP blocking, and system updates.

4. **Close the app** to end monitoring.

## Creating an Executable (.exe)

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Create the `.exe` file:

   ```bash
   python -m PyInstaller --onefile --windowed main.py
   ```

   The `.exe` will be in the `dist` folder.

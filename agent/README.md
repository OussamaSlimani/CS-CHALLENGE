# Network Capture and Firebase App

A Python app using Tkinter for a GUI that captures network traffic data and saves it to Firebase. Users can log in and start periodic packet capture. Captured metrics are sanitized and saved in Firebase Realtime Database.

## Requirements

- **Python 3.8+**
- Packages: `firebase-admin`, `scapy`, `tkinter`

## Installation

1. **Install Dependencies**:

   ```bash
   pip install firebase-admin scapy
   ```

2. **Firebase Setup**:

   - Replace `service_account_file` in the code with your Firebase Admin credentials, or load from a `.json` file.

3. **Run the App**:

```bash
   python app.py
```

## Creating an Executable (.exe)

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Create the `.exe` file:

   ```bash
   pyinstaller --onefile --windowed app.py
   ```

   The `.exe` will be in the `dist` folder.

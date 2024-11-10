import requests
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
print("Initializing Firebase Admin SDK...")
cred = credentials.Certificate("server/admin/credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cs-challenge-f4c13-default-rtdb.firebaseio.com'
})
print("Firebase Admin SDK initialized.")

# Firebase reference to the user data
ref = db.reference('/userData')

# URLs for the APIs
unsw_url = "https://unsw-nb15.onrender.com/predict/unsw_15"
cic_ids_url = "https://unsw-nb15.onrender.com/predict/cic_ids_2018"

# Function to call the UNSW-NB15 model API
def predict_unsw(data):
    print(f"Sending data to UNSW-NB15 model API: {data}")
    response = requests.post(unsw_url, json=data)
    if response.status_code == 200:
        result = response.json().get('predicted_class', 'error')
        print(f"UNSW-NB15 model prediction received: {result}")
        return result
    print("Error with UNSW-NB15 model API request.")
    return 'error'

# Function to call the CIC_IDS_2018 model API
def predict_cic_ids(data):
    print(f"Sending data to CIC_IDS_2018 model API: {data}")
    response = requests.post(cic_ids_url, json=data)
    if response.status_code == 200:
        result = response.json().get('predicted_class', 'error')
        print(f"CIC_IDS_2018 model prediction received: {result}")
        return result
    print("Error with CIC_IDS_2018 model API request.")
    return 'error'

# Function to update the Firebase database with the results
def update_firebase(user_id, timestamp, unsw_result, cic_ids_result):
    print(f"Updating Firebase for user {user_id}, timestamp {timestamp} with results:")
    print(f"  UNSW_NB15 Result: {unsw_result}")
    print(f"  CIC_IDS_2018 Result: {cic_ids_result}")
    # Reference to the specific user's traffic data
    user_traffic_ref = ref.child(user_id).child("userTraffic").child(timestamp)
    # Update the 'detections' field with model predictions
    user_traffic_ref.update({
        'detections': {
            "UNSW_NB15": unsw_result,
            "CIC_IDS_2018": cic_ids_result
        }
    })
    print("Firebase update complete.")

# Main function to process user traffic data
def process_traffic_data():
    print("Starting to process traffic data for each user...")
    # Iterate through each user in Firebase
    users = ref.get()
    if not users:
        print("No user data found in Firebase.")
        return

    for user_id, user_data in users.items():
        print(f"Processing data for user: {user_id}")
        # Iterate through each user's traffic data
        user_traffic = user_data.get("userTraffic", {})
        for timestamp, traffic_data in user_traffic.items():
            print(f"  Processing traffic data at timestamp: {timestamp}")
            
            # Check if detections already exist for this timestamp
            if "detections" in traffic_data:
                continue 

            # For UNSW_NB15 model
            unsw_data = {
                "dur": traffic_data["dur"],
                "sbytes": traffic_data["sbytes"],
                "dbytes": traffic_data["dbytes"],
                "Sload": traffic_data["Sload"],
                "swin": traffic_data["swin"],
                "smeansz": traffic_data["smeansz"],
                "Sjit": traffic_data["Sjit"],
                "Stime": traffic_data["Stime"],
                "tcprtt": traffic_data["tcprtt"],
                "ct_srv_src": traffic_data["ct_srv_src"],
                "ct_srv_dst": traffic_data["ct_srv_dst"],
                "ct_dst_ltm": traffic_data["ct_dst_ltm"],
                "ct_src_ltm": traffic_data["ct_src_ltm"],
                "ct_dst_src_ltm": traffic_data["ct_dst_src_ltm"],
                "duration": traffic_data["duration"],
                "byte_ratio": traffic_data["byte_ratio"],
                "jit_ratio": traffic_data["jit_ratio"],
                "inter_pkt_ratio": traffic_data["inter_pkt_ratio"],
                "tcp_setup_ratio": traffic_data["tcp_setup_ratio"],
                "total_load": traffic_data["total_load"],
                "byte_pkt_interaction_dst": traffic_data["byte_pkt_interaction_dst"],
                "load_jit_interaction_dst": traffic_data["load_jit_interaction_dst"],
                "tcp_seq_diff": traffic_data["tcp_seq_diff"]
            }

            # For CIC_IDS_2018 model
            cic_ids_data = {
                "Dst Port": traffic_data["Dst Port"],
                "Protocol": traffic_data["Protocol"],
                "Fwd Pkt Len Min": traffic_data["Fwd Pkt Len Min"],
                "Fwd Pkt Len Std": traffic_data["Fwd Pkt Len Std"],
                "Bwd Pkt Len Min": traffic_data["Bwd Pkt Len Min"],
                "Flow Byts/s": traffic_data["Flow Bytss"],  # Adjusted key
                "Flow IAT Mean": traffic_data["Flow IAT Mean"],
                "Flow IAT Std": traffic_data["Flow IAT Std"],
                "Flow IAT Min": traffic_data["Flow IAT Min"],
                "Fwd IAT Std": traffic_data["Fwd IAT Std"],
                "Bwd IAT Std": traffic_data["Bwd IAT Std"],
                "Bwd IAT Max": traffic_data["Bwd IAT Max"],
                "Bwd IAT Min": traffic_data["Bwd IAT Min"],
                "Fwd PSH Flags": traffic_data["Fwd PSH Flags"],
                "Fwd URG Flags": traffic_data["Fwd URG Flags"],
                "Bwd Header Len": traffic_data["Bwd Header Len"],
                "Bwd Pkts/s": traffic_data["Bwd Pktss"],
                "Pkt Len Min": traffic_data["Pkt Len Min"],
                "FIN Flag Cnt": traffic_data["FIN Flag Cnt"],
                "RST Flag Cnt": traffic_data["RST Flag Cnt"],
                "PSH Flag Cnt": traffic_data["PSH Flag Cnt"],
                "ACK Flag Cnt": traffic_data["ACK Flag Cnt"],
                "URG Flag Cnt": traffic_data["URG Flag Cnt"],
                "Down/Up Ratio": traffic_data["DownUp Ratio"],
                "Pkt Size Avg": traffic_data["Pkt Size Avg"],
                "Fwd Seg Size Avg": traffic_data["Fwd Seg Size Avg"],
                "Bwd Seg Size Avg": traffic_data["Bwd Seg Size Avg"],
                "Init Fwd Win Byts": traffic_data["Init Fwd Win Byts"],
                "Init Bwd Win Byts": traffic_data["Init Bwd Win Byts"],
                "Fwd Act Data Pkts": traffic_data["Fwd Act Data Pkts"],
                "Fwd Seg Size Min": traffic_data["Fwd Seg Size Min"],
                "Active Std": traffic_data["Active Std"],
                "Active Max": traffic_data["Active Max"],
                "Active Min": traffic_data["Active Min"],
                "Idle Std": traffic_data["Idle Std"],
                "Idle Max": traffic_data["Idle Max"],
                "Idle Min": traffic_data["Idle Min"]
            }

            # Get predictions from both models
            unsw_result = predict_unsw(unsw_data)
            cic_ids_result = predict_cic_ids(cic_ids_data)

            # Update Firebase with the results
            update_firebase(user_id, timestamp, unsw_result, cic_ids_result)

# Run the process
print("Initiating the traffic data processing workflow...")
process_traffic_data()
print("Traffic data processing completed.")

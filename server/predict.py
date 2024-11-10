import requests
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
print("Initializing Firebase Admin SDK...")
# Define the service account credentials inline as a dictionary
service_account_file = {
  "type": "service_account",
  "project_id": "cs-challenge-f4c13",
  "private_key_id": "485632e1d4c66012fadc791607af7fce94051d80",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCZMthwxpgs8TQ2\nWi5o2/SuuLzFlmpP0vS45FA0iA64B5FV9AyHk8QMg0rkso7Zjr6jv3fZmrzCzwqw\nEpWffuNNx8ncgJ5+ln0QPHDz0MUYXsAUq88J3Arn2xx9QFHOLu8eHOOkmk1kRI8Y\n6Pp7KY0piNZ9x4hYC2YQP8UU+KAH4TtTw3pXoYkvSlp+EhcTUZPsP/lPBKVUuu85\nNloT2M+w+kYKKlPggZztsA7/RcP2zpcfuWKYetllmeE6buXlrqzolSaaK+MiR+6I\nizZiX1w1r912GnWsh+5cNdN92MXEnrB4Oc/A4W6qex5dg4o+vdN5bau9Qykg6uAp\npNF5SzCPAgMBAAECggEAEhTNNOpLlapWRj/4kEm9pE2LgiqRm6BDX/saeEjCq/fA\nsItgWzQWhH+OfFWSxJyzZXI4vAcmVjvHgCaBYFTCkTCOY6cOjdRHKH5pum0ehhTQ\nyN/KTNiatOjIgQPxY8toT36LY6cOkVICLad5wMWTsp5C6o99SR73Sd2s7h+2C5fb\n+00cxmPcNZBbUqMTNItFhRQ14NPyzJFQij8/tVCP1ZDAtFjeZFG8iPET7kEy8Xrg\nyc2AGn5UDOayuzSE86QbfepdFOBK40gufOiog55W5bPnKIq75VFn8xUyQlL3v70u\naVEiIkCFbHwCl6TffsPtGeozvh78eKK+jwEiXenUyQKBgQDL4TQr2HE6y5GzutH/\nLv+SEstJZ9lVaZlsfILQC0uylDhUgHeHM3NtwVJArSKnWUU+kNa4u0nPgNkFpTW7\nwZetbahdIOXOWhtIdbTrcE1DFFeuT2us7HZLTYz6oS9e7bGCrXrGH4A8Ea9QTIhj\nM/E0rQ1cOCt76/CaG+/BAxWbjQKBgQDAXNhybDyQqtwRdyYVuFpHePS0gIsSeYHq\nrI6r303lE3igUPPPL2JrUekUV3YcXHmdxeo+5Z3oU4j4YUD4W9rse20Z/Tdk7BTk\np91tdLTqOzt+iNEfqNNGTiIquZrvq1/A2wL4LQZCe5+31kkwYycLOiWK+7f5vPaX\n8TA8i2JniwKBgBojSx775rhU9N8H6ng+vEEr66gDildq7GJ+K/8kE5ZXbklXFvvc\nWsYNbNAh4jl2NmxpAT45tKLHsAsLPTJPBXUUg+s8lnm4D5tgi8tLYHxjFUKhp/pJ\nbnkE/jf7hikza/iG6SCRVU1eLw2qYinltNy9+uKByQFgJD59qmUiUhjZAoGAfn3P\nGtbPsLWZxqZZ1diHDQ6dowAP81MROhbELoLFfwghvxHccPYQus9+/BBTK20nz7aw\nRTHKd1ZO8D1LcsU8HVtAL+HRhjyztHQp5+rheFEA20DueuoSG94PG5c3KbjAW1np\nBvbcceVG7qUrNXVN3FUdENpbbQ5z/Q/tjzJ8v+cCgYAsTXaVsiOsb7FmuuIM5Q/z\n7qFQ7TQkBLMb+OVgqP1rUoAeeu6cs6TX/sD+z6hRCqRJKUPRBHkMuKQfhJgdfk7n\nIm/rv3JqVALQuBj5R4y6/OBs8UMocERnzf5uSeZ6vanpJZ9sEnmaPxbFOsR4A8tn\nPtEd8PMEtegtZSPRZE20aw==\n-----END PRIVATE KEY-----\n",
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

# Firebase reference to the user data
ref = db.reference('/userData')

# URLs for the APIs
unsw_url = "http://127.0.0.1:5000/predict/unsw_15"
cic_ids_url = "http://127.0.0.1:5000/predict/cic_ids_2018"
kdd_url = "http://127.0.0.1:5000/predict/kdd"

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

# Function to call the KDD model API
def predict_kdd(data):
    print(f"Sending data to KDD model API: {data}")
    response = requests.post(kdd_url, json=data)
    if response.status_code == 200:
        result = response.json().get('predicted_class', 'error')
        print(f"KDD model prediction received: {result}")
        return result
    print("Error with KDD model API request.")
    return 'error'

# Function to generate commands based on model predictions
def generate_commands(unsw_result, cic_ids_result, kdd_result, traffic_data):
    commands = {}

    # Command logic based on UNSW-NB15 prediction
    if unsw_result != 'normal':
        commands['block_ip'] = {
            "execute": True,
            "port": traffic_data["Dst Port"]
        }
    
    # Command logic based on CIC_IDS_2018 prediction
    if cic_ids_result != 'beg':
        commands['close_port'] = {
            "execute": True,
            "port": traffic_data["Dst Port"]
        }
    
    # Command logic based on KDD prediction
    if kdd_result != 'normal':
        commands['update_system'] = {
            "execute": True
        }
    
    return commands

# Function to update the Firebase database with the results and generated commands
def update_firebase(user_id, timestamp, unsw_result, cic_ids_result, kdd_result, commands):
    print(f"Updating Firebase for user {user_id}, timestamp {timestamp} with results:")
    print(f"  UNSW_NB15 Result: {unsw_result}")
    print(f"  CIC_IDS_2018 Result: {cic_ids_result}")
    print(f"  KDD Result: {kdd_result}")
    print(f"  Commands: {commands}")
    
    # Reference to the specific user's traffic data
    user_traffic_ref = ref.child(user_id).child("userTraffic").child(timestamp)
    
    # Update the 'detections' field with model predictions
    user_traffic_ref.update({
        'detections': {
            "UNSW_NB15": unsw_result,
            "CIC_IDS_2018": cic_ids_result,
            "KDD": kdd_result,
        },
        'commands': commands
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

            # Prepare data for each model
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

            cic_ids_data = {
                "Dst Port": traffic_data["Dst Port"],
                "Protocol": traffic_data["Protocol"],
                "Fwd Pkt Len Min": traffic_data["Fwd Pkt Len Min"],
                "Fwd Pkt Len Std": traffic_data["Fwd Pkt Len Std"],
                "Bwd Pkt Len Min": traffic_data["Bwd Pkt Len Min"],
                "Flow Byts/s": traffic_data["Flow IAT Mean"], 
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

         # KDD data (fixing boolean issues)
            kdd_data = {
                "duration": 0.0,
                "src_bytes": 0.0000003558,
                "dst_bytes": 0.0,
                "land": 0.0,
                "wrong_fragment": 0.0,
                "urgent": 0.0,
                "hot": 0.0,
                "num_failed_logins": 0.0,
                "logged_in": 0.0,
                "num_compromised": 0.0,
                "root_shell": 0.0,
                "su_attempted": 0.0,
                "num_root": 0.0,
                "num_file_creations": 0.0,
                "num_shells": 0.0,
                "num_access_files": 0.0,
                "num_outbound_cmds": 0.0,
                "is_host_login": 0.0,
                "is_guest_login": 0.0,
                "count": 0.0039138943,
                "srv_count": 0.0039138943,
                "serror_rate": 0.0,
                "srv_serror_rate": 0.0,
                "rerror_rate": 0.0,
                "srv_rerror_rate": 0.0,
                "same_srv_rate": 1.0,
                "diff_srv_rate": 0.0,
                "srv_diff_host_rate": 0.0,
                "dst_host_count": 0.5882352941,
                "dst_host_srv_count": 0.0980392157,
                "dst_host_same_srv_rate": 0.17,
                "dst_host_diff_srv_rate": 0.03,
                "dst_host_same_src_port_rate": 0.17,
                "dst_host_srv_diff_host_rate": 0.0,
                "dst_host_serror_rate": 0.0,
                "dst_host_srv_serror_rate": 0.0,
                "dst_host_rerror_rate": 0.05,
                "dst_host_srv_rerror_rate": 0.0,
                "protocol_type_icmp": False,
                "protocol_type_udp": False,
                "service_IRC": False,
                "service_X11": False,
                "service_Z39_50": False,
                "service_aol": False,
                "service_auth": False,
                "service_bgp": False,
                "service_courier": False,
                "service_csnet_ns": False,
                "service_ctf": False,
                "service_daytime": False,
                "service_discard": False,
                "service_domain": False,
                "service_domain_u": False,
                "service_echo": False,
                "service_eco_i": False,
                "service_ecr_i": False,
                "service_efs": False,
                "service_exec": False,
                "service_finger": False,
                "service_ftp": False,
                "service_gopher": False,
                "service_harvest": False,
                "service_hostnames": False,
                "service_http": False,
                "service_http_2784": False,
                "service_http_443": False,
                "service_http_8001": False,
                "service_imap4": False,
                "service_iso_tsap": False,
                "service_klogin": False,
                "service_kshell": False,
                "service_ldap": False,
                "service_link": False,
                "service_login": False,
                "service_mtp": False,
                "service_name": False,
                "service_netbios_dgm": False,
                "service_netbios_ns": False,
                "service_netbios_ssn": False,
                "service_netstat": False,
                "service_nnsp": False,
                "service_nntp": False,
                "service_ntp_u": False,
                "service_other": False,
                "service_pm_dump": False,
                "service_pop_2": False,
                "service_pop_3": False,
                "service_printer": False,
                "service_private": False,
                "service_red_i": False,
                "service_remote_job": False,
                "service_rje": False,
                "service_shell": False,
                "service_smtp": False,
                "service_sql_net": False,
                "service_ssh": False,
                "service_sunrpc": False,
                "service_supdup": False,
                "service_systat": False,
                "service_telnet": False,
                "service_tftp_u": False,
                "service_tim_i": False,
                "service_time": False,
                "service_urh_i": False,
                "service_urp_i": False,
                "service_uucp": False,
                "service_uucp_path": False,
                "service_vmnet": False,
                "service_whois": False,
                "flag_OTH": False,
                "flag_REJ": False,
                "flag_RSTO": False,
                "flag_RSTOS0": False,
                "flag_RSTR": False,
                "flag_S0": False,
                "flag_S1": False,
                "flag_S2": False,
                "flag_S3": False,
                "flag_SH": False
            }

            # Call the model APIs for predictions
            unsw_result = predict_unsw(unsw_data)
            cic_ids_result = predict_cic_ids(cic_ids_data)
            kdd_result = predict_kdd(kdd_data)

            # Generate commands based on the results
            commands = generate_commands(unsw_result, cic_ids_result, kdd_result, traffic_data)

            # Update Firebase with the predictions and commands
            update_firebase(user_id, timestamp, unsw_result, cic_ids_result, kdd_result, commands)

process_traffic_data()
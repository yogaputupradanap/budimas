import base64
import json
import os
import requests
from flask import json, current_app, request
from google.cloud import pubsub_v1
from google.oauth2 import service_account

# Import urllib3 untuk mematikan peringatan InsecureRequestWarning saat verify=False
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def received_messages():
    messages = request.get_json()
    if not messages:
        raise nonServerErrorException(400, "No messages found in request")

    pubsub_message = messages.get("message", {})
    data = pubsub_message.get("data")
    if data:
        data = json.loads(base64.b64decode(data).decode("utf-8"))
        print("Received message data:", data)
        return data
    else:
        raise nonServerErrorException(400, "No data found in message")

class PubSub:
    publisher = None
    topics = ['create_jurnal']

    def __init__(self, project_id: str, credentials_json: str, topics: list[str] = None):
        is_dev = (os.getenv('FLASK_ENV') or "development") == 'development'
        if is_dev:
            print("Running in development mode, Pub/Sub operations will be simulated.")
            return
            
        creds_info = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        self.project_id = project_id
        self.topics = topics or []

        for topic in self.topics:
            topic_name = f"projects/{self.project_id}/topics/{topic}"
            try:
                self.publisher.get_topic(request={"topic": topic_name})
            except Exception:
                print("Creating topic:", topic_name)
                self.publisher.create_topic(name=topic_name)

    def publish(self, topic: str, data: dict):
        # 1. Cek environment dengan lebih teliti
        env = os.getenv('FLASK_ENV', 'development').lower()
        
        # 2. Tambahkan pengecekan host: jika jalan di 127.0.0.1, otomatis anggap dev
        is_localhost = request.host_url and ('127.0.0.1' in request.host_url or 'localhost' in request.host_url)
        
        if env == 'development' or is_localhost:
            print(f"--- [DEBUG] Terdeteksi Lokal/Dev Mode (Env: {env}) ---")
            return self.__publish_dev_mode(topic, data)

        # --- JALUR PRODUCTION (Google Cloud) ---
        # Hanya jalan jika benar-benar di server asli
        print(f"--- [PRODUCTION] Publishing to Google Cloud: {topic} ---")

        if not self.publisher:
            raise ValueError("Publisher client not initialized")

        if topic not in self.topics:
            raise ValueError(f"Topic {topic} not recognized")

        topic_name = f'projects/{self.project_id}/topics/{topic}'

        future = self.publisher.publish(topic_name, json.dumps(data).encode("utf-8"))
        return future.result()

    def __publish_dev_mode(self, topic: str, data: dict):
        """
        Simulasi pengiriman data ke handler lokal.
        """
        print(f"--- [DEV MODE] Simulating publish to topic: {topic} ---")
        
        try:
            # Encode data ke Base64 (meniru format asli Google Cloud Pub/Sub)
            data_messages = json.dumps(data).encode("utf-8")
            messages = base64.b64encode(data_messages).decode("utf-8")
            data_pubsub_pub = {"message": {"data": messages}}
            
            # URL - Pastikan ini sesuai dengan pendaftaran Blueprint
            # Jika masih 404, tambahkan /extra/ di tengahnya: /api/extra/pubsub/...
            url = "https://127.0.0.1:5000/api/pubsub/pubsub-handle"
            
            # Headers untuk memastikan Flask menerima sebagai JSON
            headers = {'Content-Type': 'application/json'}
            
            res = requests.post(
                url, 
                json=data_pubsub_pub,
                headers=headers,
                verify=False, 
                timeout=10
            )
            
            print(f"Handler Response: {res.status_code}")
            # Jika Response 404, berarti URL di atas salah alamat.
            # Jika Response 200, berarti SUKSES.
            
        except requests.exceptions.ConnectionError:
            print("ERROR: Gagal koneksi ke server lokal. Cek apakah Flask jalan di port 5000.")
        except Exception as e:
            print(f"ERROR di __publish_dev_mode: {str(e)}")
            
        return "dev-mode-simulated-publish"

    def close(self):
        if self.publisher:
            self.publisher.transport.close()
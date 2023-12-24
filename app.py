import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
import requests
import json
import random
import string


# ---
# Coded by Odd!
# Contributers: DuckyBlender, NorthernChicken and NotClavilux
# Github: https://github.com/OddDevelopment/OperaGX-Nitro-Gen
# Portfolio: https://odd.gay
# ---




class RequestThread(QThread):
    request_complete = pyqtSignal(str)

    @staticmethod
    def generate_random_string(length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))

    def __init__(self, url, headers, log_signal):
        super().__init__()
        self.url = url
        self.headers = headers
        self.log_signal = log_signal

    def run(self):
        session = requests.Session()

        while True:
            try:
                response = session.post(self.url, headers=self.headers, json={'partnerUserId': self.generate_random_string(64)})

                if response.status_code == 200:
                    token = response.json().get('token')
                    if token:
                        with open('codes.txt', 'a') as file:
                            file.write(f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n\n")
                        self.request_complete.emit("Token saved to codes.txt file.")
                elif response.status_code == 429:
                    self.request_complete.emit("Rate limit exceeded! Waiting one minute to allow for cooldown.")
                    self.sleep(60)
                elif response.status_code == 504:
                    self.request_complete.emit("Server timed out! Trying again in 5 seconds.")
                    self.sleep(5)
                else:
                    self.request_complete.emit(f"Request failed with status code {response.status_code}.")
                    self.request_complete.emit(f"Error message: {response.text}")
            except requests.RequestException as e:
                self.request_complete.emit(f"Request failed with exception: {str(e)}")

            self.sleep(1)

class NitroGenApp(QWidget):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('OperaGX Nitro Gen')
        self.setGeometry(100, 100, 600, 400)

        
        self.label = QLabel('OperaGX Nitro Generator', self)
        self.start_button = QPushButton('Start', self)
        self.stop_button = QPushButton('Stop', self)
        self.log_area = QTextEdit(self)

        
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.log_area)

        
        self.start_button.clicked.connect(self.start_script)
        self.stop_button.clicked.connect(self.stop_script)

        self.log_signal.connect(self.log_area.append)  

        
        self.stop_button.setEnabled(False)

        self.show()

    def start_script(self):
        self.log_area.clear()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.url = 'https://api.discord.gx.games/v1/direct-fulfillment'
        self.headers = {
              'authority': 'api.discord.gx.games',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.opera.com',
    'referer': 'https://www.opera.com/',
    'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'
        }

        self.request_thread = RequestThread(self.url, self.headers, self.log_signal)
        self.request_thread.request_complete.connect(self.log_message)
        self.request_thread.start()

    def stop_script(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        if hasattr(self, 'request_thread'):
            self.request_thread.terminate()

    def log_message(self, message):
        self.log_signal.emit(message)  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NitroGenApp()

    sys.exit(app.exec_())

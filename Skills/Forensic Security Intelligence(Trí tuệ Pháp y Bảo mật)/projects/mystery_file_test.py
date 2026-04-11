# Mystery File - DO NOT EXECUTE - FOR FORENSIC TESTING ONLY
import os
import base64
import socket

# Mock "Stolen" AWS Key
# Note: This is a generated test key, not real credentials.
AWS_KEY = "AKIA1234567890ABCDEF" 
AWS_SECRET = "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789aBcD"

def exfiltrate_data(data):
    # Suspicious pattern: Sending local data to a remote webhook
    target = "discordapp.com/api/webhooks/123456789"
    print(f"DEBUG: Exfiltrating to {target}")
    # In a real malware, this would use 'requests' or 'socket'
    eval("print('Dangerous execution via eval!')")

if __name__ == "__main__":
    exfiltrate_data("Sensitive Project Info")

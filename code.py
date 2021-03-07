import ctypes
import os
import site
import subprocess
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
import ttkthemes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
subprocess.run('taskkill /F /IM chromedriver.exe', capture_output=True)
subprocess.run('taskkill /F /IM chrome.exe', capture_output=True)
homedir = os.path.expanduser("~")
print("you must have whatsapp web connected to google chrome browser")


def on_click_quit():
    global send_flag
    global sent_message_flag
    global stop_flag
    if send_flag and not sent_message_flag and not stop_flag:
        stop_flag = True
        ok_button.configure(text="resume", font=("Consolas", 20))
        quit_button.configure(text="quit", font=("Consolas", 26))
    else:
        master.destroy()
        sys.exit()


def keys_controls(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")
    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")
    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")
    if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
        event.widget.event_generate("<<SelectAll>>")


LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]


font = CONSOLE_FONT_INFOEX()
font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
font.nFont = 12
font.dwFontSize.X = 12
font.dwFontSize.Y = 16
font.FontFamily = 54
font.FontWeight = 400
font.FaceName = "Courier New"
handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))
# todo ______________________________________________________________________

number_of_messages = 0
contact = ""
send_flag = False
send_flag_needed = False
ok_button_flag = False
sent_message_flag = False
fail_flag = False
stop_flag = False
waiting_flag = False
master = ttkthemes.themed_tk.ThemedTk()
master.configure(background="#2A3240")
master.get_themes()
master.set_theme("adapta")
master.title('Whatsapp Message Sender By Snir')
master.bind_all("<Key>", keys_controls, "+")
master.geometry('1200x750')
master.iconbitmap("your icon.ico file path")

def send_whatsapp(contact, message, number_of_messages):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    contact = contact
    text = message
    number_of_messages = number_of_messages
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={homedir}\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options, executable_path="your chromedriver.exe file path")
    driver.get("https://web.whatsapp.com")
    inp_xpath_search = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    input_box_search = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
    input_box_search.click()
    input_box_search.send_keys(contact)
    driver.implicitly_wait(0.3)
    input_box_search.send_keys(Keys.ENTER)
    xpath = '//*[@id="main"]/header/div[2]/div[1]/div/span'
    global waiting_flag
    waiting_flag = True

    try:
        contact_name = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(xpath))
        # print("quiting")
        # master.after(3000)
        # my_label.configure(text="quiting...")
        # master.update()
        # master.after(3000)
        # master.destroy()
        # quit()
        my_label.configure(text=f"send the message to '{contact_name.text}'?\npress the send button to confirm =>", fg="#E5C07B")
        ok_button.configure(text="send", font=("Consolas", 25), width=4)
        global send_flag_needed
        send_flag_needed = True
        while not send_flag:
            master.update()
            master.after(10)
        # my_label.configure(text="sending...")
        # yes_or_no = input(f"send message to {contact_name.text}?")
        if send_flag:
            quit_button.configure(text="stop", font=("Consolas", 26))
            inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
            input_box = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(inp_xpath))
            cnt = 1
            while cnt <= int(number_of_messages):
                if not stop_flag:
                    input_box.send_keys(text + Keys.ENTER)
                    my_label.configure(text="messages sent: " + str(cnt), fg="#E5C07B")
                    cnt += 1
            quit_button.configure(text="quit", font=("Consolas", 26))
            master.after(500)
            driver.quit()
            print(f"sent")
            global sent_message_flag
            sent_message_flag = True
            ok_button.configure(text="again", cursor="exchange")
            my_label.configure(text="messages sent successfully\npress again to send another message =>")

    except:
        my_label.configure(text=f"contact {contact} was not found", fg="red")
        print(f"contact {contact} was not found")
        global fail_flag
        fail_flag = True


def on_click_ok():
    global ok_button_flag
    global send_flag_needed
    global send_flag
    global stop_flag
    global sent_message_flag
    global fail_flag
    global waiting_flag
    if ok_button['text'] == "again":
        ok_button.configure(cursor="arrow")
        my_label.configure(text="")
        ok_button.configure(text="send")
        e1.delete("1.0", "end")
        e1.insert("1.0", "")
        e2.delete("1.0", "end")
        e2.insert("1.0", "")
        e3.delete(0, tk.END)
        e3.insert(0, "1")
        e4.delete(0, tk.END)
        e4.insert(0, "")
        scale.set(1)
        send_flag = False
        send_flag_needed = False
        ok_button_flag = False
        sent_message_flag = False
        fail_flag = False
        stop_flag = False
        waiting_flag = False
        return
    if stop_flag:
        stop_flag = False
        quit_button.configure(text="stop", font=("Consolas", 26))
    elif ok_button_flag and send_flag_needed:
        send_flag = True
    elif sent_message_flag and not fail_flag:
        my_label.config(text="already sent a message", background="#2A3240", font=("Consolas", 22), fg="red")
    elif not send_flag_needed and not ok_button_flag:
        if str(e1.get("1.0", "end")).strip() and str(e2.get("1.0", "end")).strip():
            if e4.get():
                while str(datetime.now())[11:-10] != str(e4.get()).replace(" ", ":"):
                    master.update()
                    time.sleep(0.1)
                    print("\r", str(datetime.now())[11:-7], e4.get(), end="")
                    my_label.config(text=f"current time: {str(datetime.now())[11:-7]}", fg="#E5C07B")
                print()
            contact = str(e1.get("1.0", "end")).strip()
            message = str(e2.get("1.0", "end")).strip()
            number_of_messages = e3.get()
            print(f"sending {message} to {contact} {number_of_messages} times")
            # my_label.config(text=f"sending {message} to {contact} {number_of_messages} times")
            my_label.config(text=f"searching for '{contact}'", fg="#E5C07B")
            master.configure(cursor="watch")
            t1 = threading.Thread(target=send_whatsapp, args=(contact, message, number_of_messages)).start()
            ok_button_flag = True
            while not waiting_flag:
                master.update()
            master.configure(cursor="arrow")
        else:
            print("enter the missing data")
            if not str(e1.get("1.0", "end")).strip() and not str(e2.get("1.0", "end")).strip():
                my_label.config(text="enter contact and message", fg="red")
            elif not str(e1.get("1.0", "end")).strip():
                my_label.config(text="enter the contact", fg="red")
            elif not str(e2.get("1.0", "end")).strip():
                my_label.config(text="enter the message", fg="red")

    elif fail_flag:
        my_label.config(text="can't send the message", fg="red")
    elif not send_flag_needed:
        my_label.config(text="please wait...", fg="red")




contact_label = tk.Label(master, text="Contact:", height=3, font=("Consolas", 32))
contact_label.grid(row=0)
contact_label.configure(background="#2A3240")
message_label = tk.Label(master, text="Message:", height=3, font=("Consolas", 32))
message_label.grid(row=1)
message_label.configure(background="#2A3240")
messages_num_label = tk.Label(master, text="Number of messages:", height=3, font=("Consolas", 32))
messages_num_label.grid(row=2)
messages_num_label.configure(background="#2A3240")
time_label = tk.Label(master, text="Time(optional):", height=3, font=("Consolas", 32))
time_label.grid(row=3)
time_label.configure(background="#2A3240")
global my_label
my_label = tk.Label(master, text="you must have whatsapp web connected\nto google chrome browser\nchrome will be closed after clicking send", height=4, font=("Consolas", 16))
my_label.place(width=600, x=130, y=650)
my_label.configure(background="#2A3240")
e1 = tk.Text(master, font=('Tahoma', 20), width=40, height=1)
e1.tag_configure('tag-right', justify='right')
e1.insert('end', '', 'tag-right')
e1.configure(background="#39455B")

e1.grid(row=0, column=1)

# e2 = tk.Entry(master, font=("Consolas", 32))
e2 = tk.Text(master, font=('Tahoma', 20), width=40, height=2)
e2.tag_configure('tag-right', justify='right')
e2.insert('end', '', 'tag-right')
e2.configure(background="#39455B")

e2.grid(row=1, column=1)

e3 = tk.Entry(master, font=("Consolas", 32))
e3.configure(background="#39455B")

e3.grid(row=2, column=1)
e3.delete(0, tk.END)
e3.insert(0, "1")
e4 = tk.Entry(master, font=("Consolas", 32))
e4.configure(background="#39455B")
e4.grid(row=3, column=1)
e4.delete(0, tk.END)
e4.insert(0, "")
ok_button = tk.Button(master, text='OK', command=on_click_ok, width=5, height=1, font=("Consolas", 30))
ok_button.place(height=75, width=130, x=700, y=636)
ok_button.configure(background="#3EDB14", activebackground="#00FF00")
quit_button = tk.Button(master, text='quit', command=on_click_quit, width=5, height=1, font=("Consolas", 26))
quit_button.place(height=75, width=130, x=830, y=636)
quit_button.configure(background="#C80018", activebackground="red")



def set_num(val):
    e3.delete(0, tk.END)
    e3.insert(0, str(round(float(val))))


style = tk.ttk.Style(master)

style.configure('custom.Horizontal.TScale', background='#39455B')
scale = tk.ttk.Scale(master, from_=1, to=50, orient=tk.HORIZONTAL, command=set_num, style='custom.Horizontal.TScale')
scale.place(height=50, width=330, x=675, y=372)

tk.mainloop()

import json
import time
import os
import tkinter as tk

JSON_FILE = "user_text.json"
SIZE = 5# how many input slots
MAX_TIME = 1000

sleep_time_key = "sleep_time"
SLEEP_TIME = 15  # seconds
user_sep_key = "input_sep"
USER_SEP = "|"


base_data = {
    "info":[" Write input where it is not X ",
            " Write it before there is an x on it ",
            " Have '|' before and after your input text when your done writing",
            "example of valid input is:  '|hello |' "
            ],
    sleep_time_key:SLEEP_TIME,
    user_sep_key:USER_SEP

    }

for i in range(SIZE):       #here we add where there can be input
    base_data[str(i)] = ""

#we add this to dict:
#    0:"",
#    1:"",
#    2:"",
#    3:"",
#    4:"",
#    5:"",
#    6:"",
#    7:"",
#    8:"",
#    9:""
#    ...
#    n



def create_json_file(base_data):
    directory = os.path.dirname(JSON_FILE)

    # Only create directory if JSON_FILE actually contains a folder path
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(base_data, f, indent=2)


def open_file_in_texteditor(path):
    try:
        os.startfile(path)   # Windows-native file open
    except Exception:
        # Fallback: open Explorer folder
        folder = os.path.dirname(path)
        os.startfile(folder)


def loop_try_get_user_input():
    global USER_SEP
    global SLEEP_TIME

    def get_new_sep():

        data = load_json()
        new_sep = data.get(user_sep_key)

        return new_sep
    
    def get_new_sleep_time():

        data = load_json()
        new_sleep_time = data.get(sleep_time_key)

        return new_sleep_time

    def load_json():
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_json_atomic(data):
        """Write JSON atomically to avoid corruption."""
        #temp_file = JSON_FILE + ".tmp"
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        #os.replace(temp_file, JSON_FILE)  # atomic on Windows

    ##def save_json_atomic(data):
    ##    """Write JSON atomically to avoid corruption."""
    ##    temp_file = JSON_FILE + ".tmp"
    ##    with open(temp_file, "w", encoding="utf-8") as f:
    ##        json.dump(data, f, indent=2)
    ##    os.replace(temp_file, JSON_FILE)  # atomic on Windows

    def reset_json_slots():

        data = load_json()

        for i in range(SIZE): 
            data[str(i)] = "" 
            save_json_atomic(data)

    def json_read(idx):
        
        full_file_content = load_json() 
        key = str(idx)
        return full_file_content.get(key, "")

    def write_to_json(value, idx):

        full_file_content = load_json()

        if idx is None:
            # find first empty or "X" slot
            for i in range(SIZE):
                if full_file_content.get(str(i), "") in ("", "X"):
                    idx = i
                    break

        full_file_content[str(idx)] = value
        save_json_atomic(full_file_content)

    def extract_input(user_input,USER_SEP):
        print("--")
        print("extracted text:",user_input)
        s = user_input.lower().strip()
        if s=="":
            print("empty separator")
            return None
        parts = s.split(USER_SEP)
        if len(parts)==3:
            print("ok")
            print("--")
            print(parts[1])
            return parts[1]
        else: 
            print("not ok")
            print("parts",parts)
            print("--")
            return None


    elapsed_time=0
    cur_read_idx = 0
    while elapsed_time < MAX_TIME:
        print("\n\n\n-----")

        USER_SEP = get_new_sep()
        SLEEP_TIME = get_new_sleep_time()

        user_input = json_read(cur_read_idx) 
        result = extract_input(user_input,USER_SEP)

        if result:
            return result
        else:
            i=0
            while i<=cur_read_idx:
                write_to_json("X",cur_read_idx) #write x at current index in json
                i+=1
            cur_read_idx+=1
            if cur_read_idx==SIZE: #reset if all filled in json
                reset_json_slots()
                cur_read_idx= 0
        
        time.sleep(SLEEP_TIME)
        elapsed_time+=SLEEP_TIME

def overwrite_json_with_message(valid_input):
    message = f"your input was : {valid_input}","The input is now  saved in you clipboard."," Press ctrl+v to use it"
    temp_file = JSON_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(message, f, indent=2)
    os.replace(temp_file, JSON_FILE)

def write_to_clipboard(text):
    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()







def main():

    create_json_file(base_data)

    open_file_in_texteditor(JSON_FILE)

    user_inp = loop_try_get_user_input()

    overwrite_json_with_message(user_inp)

    write_to_clipboard(user_inp)

if __name__=="__main__":
    main()
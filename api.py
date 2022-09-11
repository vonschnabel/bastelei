from flask import Flask, jsonify, request
import subprocess
import psutil

users = {0: {'user': 'int011', 'password': '12345678'},
         1: {'user': 'admin', 'password': 'Test111'}}


def checkIfProcessRunning(processName):
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Alarmsystem API</h1><p>Bitte /Alarm verwenden.</p>"

@app.route('/Alarm', methods=['POST'])
def foo():
    if checkIfProcessRunning('ffplay'):
#        print('Yes a ffplay process was running')
        return "Alarm is already running"
    else:
#        print('No ffplay process was running')
        authenticated = False
        data = request.json
        for i in range(0, len(users)):
            if(users[i]['user'] == data['userid'] and users[i]['password'] == data['password']):
                authenticated = True
        if(authenticated == True):
            subprocess.run('ffplay star_wars.mp3 -t 30 -autoexit -nodisp', shell=True)
            return "200"
        else:
            print("wrong credentials")
            return "404"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#import rospy

import os, signal, sys, time
import hashlib
from flask import Flask, send_from_directory, send_file, request, jsonify, render_template

#rospy.init_node('webserver', anonymous=True)

#port = rospy.get_param('~port', 8080)
#host = rospy.get_param('~host', '0.0.0.0')
#www_path = rospy.get_param('~path','../web')

host = '0.0.0.0'
port = 8080
#os.system("ustreamer --device=/dev/video0 --desired-fps=15 --host=0.0.0.0 --port=9998 &")
#os.system("ustreamer --device=/dev/video2 --desired-fps=30 --host=0.0.0.0 --port=9999 &")
# time.sleep(3)

app = Flask(__name__, static_folder='web' + '/static', template_folder='web' + '/templates')

def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)
    signal.signal(signal.SIGINT, func)

def on_exit(sig, func=None):
    print ("Exit handler triggered")
    sys.exit(1)  

set_exit_handler(on_exit)

database = {'karakolak': '66afc285a26345d250453921bbc86b65dead43c07f3a65a70c4c30ae5050dd5d'}

@app.route('/')
def server_index():
    return render_template("login.html")
 
@app.route('/control', methods=['POST', 'GET'])
def login():
    name = request.form['username']
    pwd = request.form['password']
    hash_object = hashlib.sha256(pwd.encode())
    pwd_hex = hash_object.hexdigest()
    if name not in database:
        return render_template('login.html', info = 'Invalid username')
    else:
        if database[name] != pwd_hex:
            return render_template('login.html', info = 'Invalid password')
        else:
            ip_address = request.host.split(':')[0]
            return render_template('index.html',
                ros_host = ip_address,
                # ros_robot = os.uname()[1]
            )

app.run(host=host, port=port, threaded=True)

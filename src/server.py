# import rospy

import os, signal, sys, time
from flask import Flask, send_from_directory, send_file, request, jsonify, render_template

# rospy.init_node('webserver', anonymous=True)

# port = rospy.get_param('~port', 8080)
# host = rospy.get_param('~host', '0.0.0.0')
# www_path = rospy.get_param('~path','../web')

host = '0.0.0.0'
port = 8080
os.system("ustreamer --device=/dev/video0 --host=0.0.0.0 --port=9999 &") #add ./ustreamer to path
time.sleep(3)

app = Flask(__name__, static_folder='../web' + '/static', template_folder='../web')

def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)
    signal.signal(signal.SIGINT, func)

def on_exit(sig, func=None):
    print ("Exit handler triggered")
    sys.exit(1)  

@app.route('/')
def server_index():
    ip_address = request.host.split(':')[0]
    return render_template('index.html',
            # ros_host = ip_address,
            # ros_robot = os.uname()[1]
            )

set_exit_handler(on_exit)

app.run(host=host, port=port, threaded=True)

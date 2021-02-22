import uuid
import os
import json

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import make_response
app = Flask(__name__)

# unique mapping from ip to uuid
ip2uuid = {}
def get_uuid(query_ip):
	if query_ip in ip2uuid.keys():
		return ip2uuid[query_ip]
	else:
		ip2uuid[query_ip] = str(uuid.uuid4().hex)
		return ip2uuid[query_ip]

@app.route('/hello/')
def hello():
	return "Hello World! If you see this message, it usually means the website is working and responding."

@app.route('/')
def render_default():
	# request_ip = request.remote_addr
	return render_template('default.html')

# @app.route('/submit', methods=["POST"])
# def process_submission():
# 	request_data = request.get_json()
# 	# append ip
# 	request_data["ip"] = request.remote_addr
# 	file_prefix = "{}_{}".format(request_data["benchmark"], get_uuid(request.remote_addr))
# 	file_postfix = 0
# 	while True:
# 		if os.path.isfile("./submissions/{}_{}.log".format(file_prefix, file_postfix)):
# 			file_postfix += 1
# 		else:
# 			break
# 	file_to_write = "{}_{}.log".format(file_prefix, file_postfix)
# 	print("# write submission to: {}".format(file_to_write))
# 	# write as json
# 	with open("./submissions/{}".format(file_to_write), "w") as f:
# 		json.dump(request_data, f)
# 	# then return
# 	return make_response(
# 		jsonify({'status':'successful'}), 200
# 	)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=4869)
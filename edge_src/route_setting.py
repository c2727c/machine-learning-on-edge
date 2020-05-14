from edge_src import app,edge_server
import logging
from flask import render_template, jsonify, request, make_response, send_from_directory
import os


@app.route('/setting/setconfig')
def setconfig():
	form = request.values
	value = form.get("value")
	name = form.get("name")
	app.config[name]=value
	print('SET app.config[{}] as '.format(name,app.config[name]))
	return jsonify('')




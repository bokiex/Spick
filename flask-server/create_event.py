from flask import Flask, request, jsonify,redirect
from flask_cors import CORS
import os
import sys
from datetime import datetime

from os import environ
import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

@app.route("/create_event", methods=['POST'])
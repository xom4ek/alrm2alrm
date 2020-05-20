from flask import Flask
from flask import request
import logging
import json
import requests
from datetime import datetime
from flask import jsonify
import os


app = Flask(__name__)

class Alert():
    def __init__(self, data_json):
        self.startsAt = data_json['startsAt']
        self.endsAt = data_json['endsAt']
        self.annotations = data_json['annotations']
        self.labels = data_json['labels']
        self.generatorURL = data_json['generatorURL']
        self.data = data_json

    def __repr__(self):
        return '<Alert {}>'.format(self.labels['alert_name'])


@app.route('/test', methods=['POST','GET'])
def test():
    if request.method == 'GET':
        return "just some test here", 200
    if request.method == 'POST':
        return request.get_data(),200


@app.route('/alerts', methods=['POST','GET'])
def main():
    try:
        if request.method == 'GET':
            return "Api for transform AlertManager JSON webhooks to antoher webhook", 200
        if request.method == 'POST':
            return send(handle_alerts(request.get_json()))
    except Exception as e:
        logging.error("Template alert fail {}".format(e))
        return "Error: {}".format(e.__str__()), 500


def handle_alerts(data):
    alerts = []
    for alert in data["alerts"]:
        try:
            alerts.append(Alert(alert))
        except Exception as e:
            logging.error("Storing alerts failed: %s", e)
    return(alerts)

def send(alerts):
    for alert in alerts:
        logging.info(alert.labels['alert_name'])
        logging.info(requests.post(webhook_url,json=[alert.data,],verify=False).text)
    return "OK",200


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    host = os.environ.get('HOST', '0.0.0.0')
    webhook_url = os.environ.get('WEBHOOK_URL', 'https://alertmanager.nglm.rt.ru:6443/api/v2/alerts')
    app.run(host=host, port=port,debug=True)

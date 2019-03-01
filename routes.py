import sqlalchemy

from flask import request, jsonify
from sentinelbackend import app
from sentinelbackend.utils import convert, getcountry
from sentinelbackend.virustotal import lookup_process, adv_scan, quickScan
from sentinelbackend.models import addToBlacklist, removeFromBlacklist, getRules, getScheduledFiles
import psutil


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/getProcesses', methods=['GET', 'POST'])
def getprocesses():
    if request.method == 'POST':
        processes = psutil.net_connections()
        result = list(map(convert, processes))
        return jsonify(
            {
                "processes": list(filter(lambda x: len(x['remoteAddr']), result))
            }
        )


@app.route('/lookupProcess', methods=['POST'])
def quickscan():
    if request.method == 'POST':
        return jsonify(
            {
                "results":  lookup_process(request.form.get('PID'))

            }
        )


@app.route('/blockIP', methods=['POST'])
def block_ip():
    if request.method == 'POST':
        response = addToBlacklist(request.form.get('IP'), request.form.get('port') if request.form.get('port') != None else "*")
        return response

@app.route('/unblockIP', methods=['POST'])
def unblock_ip():
    if request.method == 'POST':
        response = removeFromBlacklist(request.form.get('IP'), request.form.get('port') if request.form.get('port') != None else "*")
        return response


@app.route('/getRules', methods=['POST'])
def get_rules():
    return jsonify(
        {
            "rules": list(getRules())
        }
    )


@app.route('/advancedScan', methods=['POST'])
def advanced_scan():
    return jsonify(adv_scan(request.form.get('filepath')))


@app.route('/getScheduledFiles', methods=['POST'])
def getS():
    return jsonify(
        {
            "files": getScheduledFiles()
        }
    )


@app.route('/getReport', methods=['POST'])
def quick_scan():
    return jsonify(quickScan(request.form.get('filepath')))

@app.route('/killProcess', methods=['POST'])
def killProcess():
    if request.method == 'POST':
        try:
            pid = int(request.form.get('PID'))
            process = psutil.Process(pid)
            process.kill()
            return "process terminated"
        except:
            return "some error occured. Are you sure you have sudo priviledge"

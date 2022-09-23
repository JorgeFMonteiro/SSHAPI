from flask import Flask, request, abort
from os.path import exists as file_exists
from os import environ
from decorators import login_required, check_input
import paramiko

COMMAND_BLACKLIST = []
app = Flask(__name__)


def load_command_blacklist():
    if not file_exists("command-blacklist.txt"):
        return
    f = open("command-blacklist.txt", "r")
    data = f.read()
    lines = data.split("\n")
    for line in lines:
        COMMAND_BLACKLIST.append(line)


def check_command(command):
    for command_blacklist in COMMAND_BLACKLIST:
        if command_blacklist in command:
            return "Command {command} not allowed".format(command=command)


@app.route('/send-command', methods=['POST'])
@login_required
@check_input
def send_command():
    request_dict = request.json
    host = request_dict.get('host')
    user = request_dict.get('user')
    password = request_dict.get('password')
    command = request_dict.get('command')
    check_command_error = check_command(command)
    if check_command_error:
        abort(403, description=check_command_error)
    client = paramiko.client.SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password, timeout=5)
        _stdin, _stdout, _stderr = client.exec_command(command)
        response = _stdout.read().decode()
    except Exception as e:
        abort(503, description="Problems connecting: " + str(e))
    client.close()
    # Remove last \n from response string
    return response.strip()


load_command_blacklist()



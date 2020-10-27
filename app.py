from flask import Flask
from flask import request
from threading import Thread
import configparser
import main
import util

app = Flask(__name__)

@app.route("/suspend", methods=["POST"])
def set_suspension():
  util.set_config_val("suspended", request.form["suspend"])
  res = f"{'S' if int(request.form['suspend']) else 'Uns'}uspended service"
  print(res)
  return res

@app.route("/schedule")
def get_schedule():
  return f"Next run: {util.get_next_run_date()}"

t = Thread(target=main.setup)
t.start()

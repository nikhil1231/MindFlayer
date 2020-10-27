import time
import os
import threading
import schedule
import random
import configparser
import re
from datetime import datetime, timedelta

MEAN_WAIT_TIME = 30 * 60

testing = False

def run_scheduler_async(interval=1):
  cease_continuous_run = threading.Event()

  class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
      while not cease_continuous_run.is_set():
        schedule.run_pending()
        time.sleep(interval)

  continuous_thread = ScheduleThread()
  continuous_thread.start()
  return cease_continuous_run

def random_wait():
  time.sleep(max(0, random.gauss(MEAN_WAIT_TIME, MEAN_WAIT_TIME / 4)))

def start_session(wait=True):
  if int(get_config_val("suspended")):
    return
  if wait: random_wait()

  # Do swiping
  print('swiping')

  if not testing:
    set_last_run_date()
    set_session_scheduler()

  return schedule.CancelJob

def set_session_scheduler():
  run_time = get_run_time()
  if run_time == 0:
    start_session(wait=not testing)
  else:
    schedule.every().day.at(run_time).do(start_session, wait=not testing).tag("like_session")

def get_run_time():
  now = datetime.now()
  last_run = get_last_run_date()
  if now - last_run > timedelta(hours=12):
    return 0
  else:
    run_date = last_run + timedelta(hours=12)
    run_time = run_date.time()
    sleep_time = datetime.strptime(get_config_val('sleep_time'), "%H:%M").time()
    wake_time = datetime.strptime(get_config_val('wake_time'), "%H:%M").time()

    if sleep_time < run_time < wake_time:
      return wake_time.strftime("%H:%M")
    else:
      return run_time.strftime("%H:%M")

def get_next_run_date():
  next_run = schedule.jobs[0].next_run
  now = datetime.now()
  day = "today" if next_run.day == now.day else "tomorrow"
  return f"{day} at {next_run.strftime('%H:%M')}"

def set_last_run_date():
  set_config_val("last_run", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def get_last_run_date():
  if config_val_exists('last_run'):
    return datetime.strptime(get_config_val('last_run'), "%Y-%m-%d %H:%M:%S")
  else:
    return datetime.min

def get_config_val(key):
  return _get_config()["config"][key]

def set_config_val(key, val):
  config = _get_config()
  config["config"][key] = val
  _write_config(config)

def config_val_exists(key):
  return _get_config().has_option('config', key)

def init_default_config():
  config = configparser.ConfigParser()
  config.add_section("config")
  config["config"]["fb_email"] = "email"
  config["config"]["fb_password"] = "password"
  config["config"]["sleep_time"] = "9:00"
  config["config"]["wake_time"] = "00:00"
  config["config"]["suspended"] = 0

  _write_config(config)

def _get_config():
  config = configparser.ConfigParser()
  config.read("config.ini")
  return config

def _write_config(config):
  with open('config.ini', 'w') as configfile:
    config.write(configfile)

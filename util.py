import time
import os
import threading
import schedule
import config
import random
import re
from datetime import datetime, timedelta
import fb_auth_token
import tinder

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
  if int(config.get_val("suspended")):
    return
  if wait: random_wait()

  tinder.start_session()

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
    sleep_time = datetime.strptime(config.get_val('sleep_time'), "%H:%M").time()
    wake_time = datetime.strptime(config.get_val('wake_time'), "%H:%M").time()

    if sleep_time < run_time < wake_time:
      return wake_time.strftime("%H:%M")
    else:
      return run_time.strftime("%H:%M")

def get_next_run_date():
  if len(schedule.jobs) == 0:
    return "No jobs scheduled."
  next_run = schedule.jobs[0].next_run
  now = datetime.now()
  day = "today" if next_run.day == now.day else "tomorrow"
  return f"{day} at {next_run.strftime('%H:%M')}"

def set_last_run_date():
  config.set_val("last_run", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def get_last_run_date():
  if config.val_exists('last_run'):
    return datetime.strptime(config.get_val('last_run'), "%Y-%m-%d %H:%M:%S")
  else:
    return datetime.min

def get_tokens():
  if not config.val_exists('fb_token'):
    get_fb_token()
  if not config.val_exists('tinder_token'):
    get_tinder_token()

def get_fb_token():
  print("Getting Facebook token...")
  fb_token = fb_auth_token.get_fb_access_token(config.get_val('fb_email'), config.get_val('fb_password'))
  if not fb_token:
    print('Error getting Facebook token')
    return
  config.set_val('fb_token', fb_token)

  fb_id = fb_auth_token.get_fb_id(fb_token)
  if not fb_id:
    print('Error getting Facebook ID')
    return
  config.set_val('fb_id', fb_id)

def get_tinder_token():
  print("Getting Tinder token...")
  tinder.get_token()

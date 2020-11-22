import configparser

def get_val(key):
  return _get()["config"][key]

def set_val(key, val):
  config = _get()
  config["config"][key] = str(val)
  _write(config)

def val_exists(key):
  return _get().has_option('config', key)

def init_default():
  config = configparser.ConfigParser()
  config.add_section("config")
  config["config"]["fb_email"] = "email"
  config["config"]["fb_password"] = "password"
  config["config"]["sleep_time"] = "00:00"
  config["config"]["wake_time"] = "9:00"
  config["config"]["suspended"] = "0"

  _write(config)

def _get():
  config = configparser.ConfigParser()
  config.read("config.ini")
  return config

def _write(config):
  with open('config.ini', 'w') as configfile:
    config.write(configfile)

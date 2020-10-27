import os
import sys
import schedule
import util

def setup():
  # Initialise config.ini if it doesn't exist
  if not os.path.exists("config.ini"):
    util.init_default_config()

  # Set up the posting timetable
  util.set_session_scheduler()

  # Run the scheduler on its own thread
  util.run_scheduler_async()

if __name__ == "__main__":
  # For testing purposes
  if len(sys.argv) > 1 and sys.argv[1] == "test":
    util.testing = True
    util.start_session(wait=False)
    sys.exit()

  setup()
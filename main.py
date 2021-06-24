import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import sys
import schedule
import util
import config

def setup():
  # Initialise config.ini if it doesn't exist
  if not os.path.exists("config.ini"):
    config.init_default()

  # Ensure tokens exists
  util.get_tokens()

  # Set up the posting timetable
  util.set_session_scheduler()

  # Run the scheduler on its own thread
  util.run_scheduler_async()

if __name__ == "__main__":
  # For testing purposes
  if len(sys.argv) > 1:
    if "test" in sys.argv:
      util.testing = True
      util.start_session(wait=False)
    if "fb" in sys.argv:
      util.get_tokens()
    sys.exit()
  setup()

import tinder_api as api
import rater
import config

num_requests = 1

def get_token(fb_token, fb_user_id):
  return api.get_auth_token(fb_token, fb_user_id)

def start_session():
  api.authverif()

  for _ in range(num_requests):
    # Retrieve recommended profiles from Tinder.
    for person in api.get_recommendations()['results']:
      rating = rater.get_rating(person)
      print(rating)
      
      break

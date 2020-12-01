import tinder_api as api
import rater
import config

num_requests = 1

def get_token(fb_token, fb_user_id):
  return api.get_auth_token(fb_token, fb_user_id)

def hot_or_not(rating):
  return rating > float(config.get_val('standard'))

def _like(person_id):
  res = api.like(person_id)
  return res['likes_remaining']

def _dislike(person_id):
  api.dislike(person_id)

def start_session():
  api.authverif()

  likes_remaining = True
  num_likes = 0
  num_dislikes = 0

  while likes_remaining:
    # Retrieve recommended profiles from Tinder.
    for person in api.get_recommendations()['results']:
      person_id = person['_id']
      rating = rater.get_rating(person)

      if hot_or_not(rating):
        if not _like(person_id):
          likes_remaining = False
          break
        num_likes += 1
      else:
        _dislike(person_id)
        num_dislikes += 1
  
  print(f"Session complete: {num_likes} likes, {num_dislikes} dislikes")

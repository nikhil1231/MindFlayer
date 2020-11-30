import os
import numpy as np
import cv2
import re
import json
import urllib.request
import keras.models
from keras.preprocessing import image
import shutil

DATA_DIR = "data"

# Loads the model that is used for facial beauty prediction. 
# This model is a pretrained ResNet50 from Keras, further trained on the SCUT-FBP5500 dataset. 
FBP_model = keras.models.load_model('model2.h5')
    
# Needed for image preprocessing later.
CASCADE="Face_cascade.xml"
FACE_CASCADE=cv2.CascadeClassifier(CASCADE)

# Define function to extract and preprocess face images from photos. Results in 350x350 pixel images.
def extract_faces(image):
  processed_images = []

  image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

  # Minimum size of detected faces is set to 75x75 pixels.
  faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.16,minNeighbors=5,minSize=(75,75),flags=0)

  for x,y,w,h in faces:
    sub_img=image[y-15:y+h+15,x-15:x+w+15]
    side = np.max(np.array([sub_img.shape[0],sub_img.shape[1]]))
    sub_image_padded = cv2.copyMakeBorder(sub_img,int(np.floor((side-sub_img.shape[1])/2)),int(np.ceil((side-sub_img.shape[1])/2)),int(np.floor((side-sub_img.shape[0])/2)),int(np.ceil((side-sub_img.shape[0])/2)),cv2.BORDER_CONSTANT)
    sub_image_resized = cv2.resize(src = sub_image_padded,dsize=(350,350))
    processed_images.append(sub_image_resized)
  return processed_images

def get_rating(person):
  if DATA_DIR in os.listdir("."):
    shutil.rmtree(DATA_DIR)
  os.mkdir(DATA_DIR)

  ratings = []
  photo_num = 0
  person_id = person['_id']
  for photo in person["photos"]:
    photo_url = photo['processedFiles'][0]['url']
    urllib.request.urlretrieve(photo_url, f"{DATA_DIR}/{person_id}_{photo_num}.jpg")
    im = cv2.imread(f"{DATA_DIR}/{person_id}_{photo_num}.jpg")
    try:
      processed_images = extract_faces(im)
    except:
      pass
    
    # Ignore images with multiple
    if len(processed_images) == 0:
      continue
    
    face = processed_images[0]
    cv2.imwrite(f"{DATA_DIR}/{person_id}_{photo_num}_.jpg", face)
    img = image.load_img(f"{DATA_DIR}/{person_id}_{photo_num}_.jpg")
    img = image.img_to_array(img)

    if len(processed_images) == 1:
      # Apply the neural network to predict face beauty.
      pred = FBP_model.predict(img.reshape((1,) + img.shape))
      ratings.append(pred[0][0])
    photo_num += 1
  
  #TODO: move likes/dislikes to separate folders

  if len(ratings) == 0:
    return 0
  
  return sum(ratings)/len(ratings)
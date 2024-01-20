import numpy as np
from fastai.vision.all import *
from fastai.learner import load_learner
import urllib.request
import os
import sys
from utils import is_cat
import tempfile

def predict(model, url):
    """ Predict API: 
        (pred,pred_idx,probs) = model.predict(img) 
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        test_fn = os.path.join(temp_dir, 'test.jpg')
        urllib.request.urlretrieve(url, test_fn)
        f = open(test_fn, mode="rb")
        data = f.read()
        img = PILImage.create(data)
        is_cat,_,probs = model.predict(img)
        return is_cat, probs[1].item()

# Load model
learn = load_learner('models/model.pkl')

# Should be False
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Black_Labrador_Retriever_-_Male_IMG_3323.jpg/2880px-Black_Labrador_Retriever_-_Male_IMG_3323.jpg"
is_cat, probs = predict(learn, url)
if is_cat is True or probs > 0.1:
    print(f'Image "{url}" incorrectly labeled as cat')
    sys.exit(1)

# Should be True
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/2880px-Cat_August_2010-4.jpg"
is_cat, probs = predict(learn, url)
if is_cat is False or probs < 0.9: 
    print(f'Image "{url}" incorrectly labeled as dog')
    sys.exit(1)

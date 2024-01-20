import streamlit as st
from PIL import Image
import numpy as np
import os

from fastai.vision.all import *
from fastai.learner import load_learner

# Load model
model_file = os.getenv('MODEL_PATH', default=os.path.join('models', 'model.pkl'))
model = load_learner(model_file)

def make_prediction(image):
    is_cat,_,probs = model.predict(image)
    return is_cat, probs[1].item()

# Streamlit user interface
st.title('Cats and dogs classifier')

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Upload an image (only cats or dog pics)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Predict button
    if st.button('Is it a cat or a dog?'):

        is_cat, prob = make_prediction(image)
        prob = prob * 100

        if is_cat:
            st.write(f"It's a 🐈‍⬛ (I'm {prob:3.2f}% certain)")
        else:
            st.write(f"It's a 🐶 (I'm {prob:3.2f}% certain)")

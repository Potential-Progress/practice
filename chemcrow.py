import streamlit as st
from PIL import Image
with st.sidebar:
    chemcrow_logo = Image.open('icon/chemcrow.png')
    st.image(chemcrow_logo)

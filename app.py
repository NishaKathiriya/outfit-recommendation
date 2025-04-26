import streamlit as st
import pandas as pd
import os
import random

# Load metadata
df = pd.read_csv("clip_generated_metadata_final.csv")
OUTFIT_FOLDER = "media/outfits"

st.set_page_config(page_title="AI Fashion Recommender", layout="centered")
st.title("👗 Fashion Recommendation Engine")

with st.form("preferences_form"):
    style = st.radio("What style of clothing do you prefer?", ["Casual", "Formal", "Streetwear","Traditional" ,"Other"])
    texture = st.radio("What prints or textures do you prefer?", ["Plain", "Stripes", "Plaid", "Other"])
    brand = st.text_input("Do you have a favorite brand?", placeholder="Enter brand")
    occasion = st.radio("What’s the occasion you’re dressing for?", ["Work", "Party", "Formal Event", "Other"])
    material = st.radio("Do you have a preference of materials?", ["Cotton", "Linen", "Leather", "Synthetics"])
    fit = st.radio("Do you prefer tight or loose fitting clothes?", ["Tight clothes", "Loose fitting"])
    photo = st.camera_input("📸 Take your photo to analyze body shape (mocked)")
    submitted = st.form_submit_button("Get Recommendation")

if submitted and photo:
    st.success("Analyzing...")



    # Filter using inputs + body shape
    matches = df[
        (df["style"] == style) &
        (df["texture"] == texture) &
        (df["occasion"] == occasion) &
        (df["material"] == material) &
        (df["fit"] == fit) 
        
    ]

    if brand:
        matches = matches[matches["brand"].str.contains(brand, case=False)]

    if not matches.empty:
        selected = matches.sample(1).iloc[0]
        img_path = os.path.join(OUTFIT_FOLDER, selected["filename"])
        st.image(img_path, use_container_width=True)
    else:
        st.warning("No matching outfit found.")

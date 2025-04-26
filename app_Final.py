import streamlit as st
import pandas as pd
import os
import random

# Load metadata
df = pd.read_csv("clip_generated_metadata_final.csv")
OUTFIT_FOLDER = "media/outfits"

st.set_page_config(page_title="AI Fashion Recommender", layout="centered")
st.title("👗 Fashion Recommendation Engine - Full Outfit")

with st.form("preferences_form"):
    style = st.radio("What style of clothing do you prefer?", ["Casual", "Formal", "Streetwear", "Traditional", "Other"])
    texture = st.radio("What prints or textures do you prefer?", ["Plain", "Stripes", "Plaid", "Other"])
    brand = st.text_input("Do you have a favorite brand?", placeholder="Enter brand")
    occasion = st.radio("What’s the occasion you’re dressing for?", ["Work", "Party", "Formal Event", "Other"])
    material = st.radio("Do you have a preference of materials?", ["Cotton", "Linen", "Leather", "Synthetics"])
    fit = st.radio("Do you prefer tight or loose fitting clothes?", ["Tight clothes", "Loose fitting"])
    photo = st.camera_input("📸 Take your photo to analyze body shape (mocked)")
    submitted = st.form_submit_button("Get Recommendation")

if submitted and photo:
    st.success("Analyzing your preferences...")

    # Filter based on inputs
    filtered_df = df[
        (df["style"] == style) &
        (df["texture"] == texture) &
        (df["occasion"] == occasion) &
        (df["material"] == material) &
        (df["fit"] == fit)
    ]

    if brand:
        filtered_df = filtered_df[filtered_df["brand"].str.contains(brand, case=False, na=False)]

    # Select Top, Bottom, Footwear separately
    top_items = filtered_df[filtered_df["category"] == "Top"]
    bottom_items = filtered_df[filtered_df["category"] == "Bottom"]
    footwear_items = filtered_df[filtered_df["category"] == "Footwear"]

    if not top_items.empty and not bottom_items.empty and not footwear_items.empty:
        selected_top = top_items.sample(1).iloc[0]
        selected_bottom = bottom_items.sample(1).iloc[0]
        selected_footwear = footwear_items.sample(1).iloc[0]

        st.subheader("👕 Your Full Outfit Recommendation:")

        st.markdown("### Top")
        top_path = os.path.join(OUTFIT_FOLDER, selected_top["filename"])
        st.image(top_path, use_container_width=True)

        st.markdown("### Bottom")
        bottom_path = os.path.join(OUTFIT_FOLDER, selected_bottom["filename"])
        st.image(bottom_path, use_container_width=True)

        st.markdown("### Footwear")
        footwear_path = os.path.join(OUTFIT_FOLDER, selected_footwear["filename"])
        st.image(footwear_path, use_container_width=True)

    else:
        st.warning("Couldn't find a complete matching outfit. Try changing some preferences!")

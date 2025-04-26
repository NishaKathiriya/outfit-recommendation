import os
import pandas as pd
import random

# Image folder
IMAGE_FOLDER = "media/outfits"

# All options for each tag
tag_options = {
    "style": ["Casual", "Formal", "Streetwear", "Other"],
    "texture": ["Plain", "Stripes", "Plaid", "Other"],
    "brand": ["Zara", "Nike", "H&M", "Uniqlo", "Adidas", "Unknown"],
    "occasion": ["Work", "Party", "Formal Event", "Other"],
    "material": ["Cotton", "Linen", "Leather", "Synthetics"],
    "fit": ["Tight clothes", "Loose fitting"],
    "body_shape": ["Rectangle", "Pear", "Hourglass", "Inverted Triangle"]
}

# Generate metadata for each image
rows = []
for fname in os.listdir(IMAGE_FOLDER):
    if fname.lower().endswith((".jpg", ".png", ".jpeg")):
        row = {
            "filename": fname,
            "style": random.choice(tag_options["style"]),
            "texture": random.choice(tag_options["texture"]),
            "brand": random.choice(tag_options["brand"]),
            "occasion": random.choice(tag_options["occasion"]),
            "material": random.choice(tag_options["material"]),
            "fit": random.choice(tag_options["fit"]),
            "body_shape": random.choice(tag_options["body_shape"]),
        }
        rows.append(row)

# Save to CSV
df = pd.DataFrame(rows)
df.to_csv("metadata.csv", index=False)
print(f"✅ metadata.csv generated for {len(df)} images.")

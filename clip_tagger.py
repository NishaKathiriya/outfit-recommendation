import clip
import torch
from PIL import Image
import os
import pandas as pd
from tqdm import tqdm

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Define your label categories
label_sets = {
    "style": ["Casual", "Formal", "Streetwear", "Traditional"],
    "texture": ["Plain", "Stripes", "Plaid", "Patterned", "Other"],
    "brand": ["Zara", "H&M", "Adidas", "Uniqlo", "Unknown"],
    "occasion": ["Work", "Party", "Formal Event", "Wedding", "Other"],
    "material": ["Cotton", "Linen", "Silk", "Leather", "Synthetics"],
    "fit": ["Tight clothes", "Loose fitting"],
    "body_shape": ["Rectangle", "Pear", "Hourglass", "Inverted Triangle"]
}

# Folder of outfit images
image_folder = "media/outfits"
output_csv = "clip_generated_metadata.csv"
results = []

# Process each image
for idx, fname in enumerate(tqdm(os.listdir(image_folder))):
    if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(image_folder, fname)

    try:
        image = preprocess(Image.open(image_path).resize((224, 224))).unsqueeze(0).to(device)

    except Exception as e:
        print(f"❌ Skipping {fname} due to error: {e}")
        continue

    row = {"filename": fname}

    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)

    for label_type, options in label_sets.items():
        texts = clip.tokenize(options).to(device)
        with torch.no_grad():
            text_features = model.encode_text(texts)
            text_features /= text_features.norm(dim=-1, keepdim=True)

            similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            best_index = similarity.argmax().item()
            row[label_type] = options[best_index]

    results.append(row)

    # Auto-save every 500 images
    if (idx + 1) % 500 == 0:
        pd.DataFrame(results).to_csv(output_csv, index=False)
        print(f"✅ Saved checkpoint at image {idx+1}")

# Final save
pd.DataFrame(results).to_csv(output_csv, index=False)
print(f"\n✅ All tags saved to {output_csv}")

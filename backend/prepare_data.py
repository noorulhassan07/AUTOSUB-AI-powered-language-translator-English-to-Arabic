import pandas as pd
import os

# Try reading with latin1 or windows-1256
try:
    df = pd.read_csv("../datasets/parallel_translation/data.csv", encoding="utf-8")
except UnicodeDecodeError:
    try:
        df = pd.read_csv("../datasets/parallel_translation/data.csv", encoding="windows-1256")
    except:
        df = pd.read_csv("../datasets/parallel_translation/data.csv", encoding="latin1")

output_dir = "../datasets/parallel_translation/data_cleaned"
os.makedirs(output_dir, exist_ok=True)

# Clean & filter
df = df.dropna(subset=["Arabic", "Urdu", "English"])
df["Arabic"] = df["Arabic"].astype(str).str.strip()
df["Urdu"] = df["Urdu"].astype(str).str.strip()
df["English"] = df["English"].astype(str).str.strip()

# Write to clean .txt files
with open(os.path.join(output_dir, "en-ar.en"), "w", encoding="utf-8") as f_en, \
     open(os.path.join(output_dir, "en-ar.ar"), "w", encoding="utf-8") as f_ar, \
     open(os.path.join(output_dir, "ur-ar.ur"), "w", encoding="utf-8") as f_ur, \
     open(os.path.join(output_dir, "ur-ar.ar"), "w", encoding="utf-8") as f_uar:
    
    for _, row in df.iterrows():
        f_en.write(row["English"] + "\n")
        f_ar.write(row["Arabic"] + "\n")
        f_ur.write(row["Urdu"] + "\n")
        f_uar.write(row["Arabic"] + "\n")

print("✅ Dataset fixed, cleaned, and saved to: quran_cleaned/")

import os
import requests
import zipfile
import tarfile
import io
from tqdm import tqdm

# Verified working dataset URLs
DATASETS = {
    "en-ar": {
        "url": "https://data.statmt.org/opus-100-corpus/v1.0/supervised/en-ar/opus.en-ar-train.zip",
        "dir": "datasets/parallel_translation/en-ar",
        "type": "zip",
        "description": "OPUS-100 English-Arabic parallel corpus (1M sentence pairs)"
    },
    "ur-ar": {
        "url": "https://github.com/zeerakw/Urdu-Arabic-Parallel-Corpus/archive/refs/heads/main.zip",
        "dir": "datasets/parallel_translation/ur-ar",
        "type": "zip",
        "description": "Urdu-Arabic parallel corpus from GitHub"
    },
    "cv_english": {
        "url": "https://voice-prod-bundler-ee1969a6ce8178826482b88e843c335f.reviews.mozilla.org/v1/en/cv-corpus-12.0-2022-12-07/en.tar.gz",
        "dir": "datasets/english_speech",
        "type": "tar.gz",
        "description": "Mozilla Common Voice English (12.0)"
    },
    "cv_urdu": {
        "url": "https://voice-prod-bundler-ee1969a6ce8178826482b88e843c335f.reviews.mozilla.org/v1/ur/cv-corpus-12.0-2022-12-07/ur.tar.gz",
        "dir": "datasets/urdu_speech",
        "type": "tar.gz",
        "description": "Mozilla Common Voice Urdu (12.0)"
    },
    "slr68_urdu": {
        "url": "https://www.openslr.org/resources/68/ur_clean.tar.gz",
        "dir": "datasets/urdu_speech",
        "type": "tar.gz",
        "description": "OpenSLR Urdu Speech Dataset (clean subset)"
    }
}

def download_file(url, save_path):
    """Download a file with progress bar"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        
        with open(save_path, 'wb') as file, tqdm(
            desc=os.path.basename(save_path),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                bar.update(len(data))
                file.write(data)
        return True
    except Exception as e:
        print(f"Download error: {str(e)}")
        return False

def download_and_extract(name, info):
    """Download and extract dataset"""
    os.makedirs(info['dir'], exist_ok=True)
    print(f"\n📦 Downloading {name} dataset")
    print(f"   {info['description']}")
    
    # Temporary download path
    ext = info['type'].split('.')[-1]
    temp_path = os.path.join(info['dir'], f"temp_{name}.{ext}")
    
    # Download the file
    if not download_file(info['url'], temp_path):
        print(f"❌ Failed to download {name}")
        return False
    
    # Extract based on file type
    try:
        if info['type'] == "zip":
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                zip_ref.extractall(info['dir'])
        elif info['type'] == "tar.gz":
            with tarfile.open(temp_path, 'r:gz') as tar_ref:
                tar_ref.extractall(path=info['dir'])
        
        print(f"✅ Successfully extracted {name}")
        os.remove(temp_path)
        return True
        
    except Exception as e:
        print(f"❌ Extraction error: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

if __name__ == "__main__":
    print("🚀 AutoSub Dataset Downloader")
    print("=" * 50)
    
    success_count = 0
    for name, info in DATASETS.items():
        if download_and_extract(name, info):
            success_count += 1
        print("-" * 50)
    
    print(f"\n🎉 Completed: {success_count}/{len(DATASETS)} datasets downloaded successfully")
    print("Note: Some datasets may be large (several GB).")
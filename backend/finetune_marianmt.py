from transformers import MarianMTModel, MarianTokenizer, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset
import os
import pandas as pd

# Configuration
DATA_DIR = os.path.join("..", "datasets", "parallel_translation", "data_cleaned")
MODEL_NAME = {
    "en-ar": "Helsinki-NLP/opus-mt-en-ar",
}
OUTPUT_DIR = {
    "en-ar": os.path.join("..", "models", "finetuned_en_ar"),
}

def load_translation_dataset(source_file, target_file, max_samples=None):
    with open(source_file, "r", encoding="utf-8") as sf, open(target_file, "r", encoding="utf-8") as tf:
        source_lines = sf.readlines()
        target_lines = tf.readlines()

    pairs = [
        {"src": s.strip(), "tgt": t.strip()}
        for s, t in zip(source_lines, target_lines)
        if s.strip() and t.strip()
    ]

    if max_samples:
        pairs = pairs[:max_samples]

    return Dataset.from_dict({
        "src": [p["src"] for p in pairs],
        "tgt": [p["tgt"] for p in pairs],
    })

def preprocess_function(batch, tokenizer, max_length=128):
    inputs = tokenizer(batch["src"], padding="max_length", truncation=True, max_length=max_length)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(batch["tgt"], padding="max_length", truncation=True, max_length=max_length)
    inputs["labels"] = labels["input_ids"]
    return inputs

def fine_tune(lang_pair="en-ar", max_samples=5000):
    print(f"\n🔧 Fine-tuning: {lang_pair}")

    src_path = os.path.join(DATA_DIR, f"{lang_pair}.en")
    tgt_path = os.path.join(DATA_DIR, f"{lang_pair}.ar")
    output_dir = OUTPUT_DIR[lang_pair]

    dataset = load_translation_dataset(src_path, tgt_path, max_samples=max_samples)
    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME[lang_pair])
    model = MarianMTModel.from_pretrained(MODEL_NAME[lang_pair])

    print("🔠 Tokenizing...")
    tokenized = dataset.map(
        lambda batch: preprocess_function(batch, tokenizer),
        batched=True,
        remove_columns=["src", "tgt"]
    )

    args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=2,
        num_train_epochs=3,
        learning_rate=5e-5,
        eval_strategy="no",  # Changed from evaluation_strategy
        save_steps=100,
        logging_steps=10,
        save_total_limit=1,
        report_to="none"
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        tokenizer=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model)
    )

    print("🚀 Training...")
    trainer.train()

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"✅ Model saved to {output_dir}")

if __name__ == "__main__":
    print("="*50)
    print("AutoSub Fine-tuning Script")
    print("="*50)
    fine_tune()

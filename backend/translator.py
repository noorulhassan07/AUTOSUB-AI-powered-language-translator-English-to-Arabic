import whisper
import torch
from transformers import MarianMTModel, MarianTokenizer
from mic_stream import audio_queue

# ✅ Load the fine-tuned English-Arabic model from the checkpoint
tokenizer_en_ar = MarianTokenizer.from_pretrained("C:/Users/nooru/Desktop/ai project/models/finetuned_en_ar/checkpoint-7500")
translator_en_ar = MarianMTModel.from_pretrained("C:/Users/nooru/Desktop/ai project/models/finetuned_en_ar/checkpoint-7500")
#tokenizer_ur_ar = MarianTokenizer.from_pretrained("../models/finetuned_ur_ar")
#translator_ur_ar = MarianMTModel.from_pretrained("../models/finetuned_ur_ar")


tokenizer_ur_ar = tokenizer_en_ar
translator_ur_ar = translator_en_ar

def translate_text(text, lang):
    tokenizer = tokenizer_ur_ar if lang == "ur" else tokenizer_en_ar
    model = translator_ur_ar if lang == "ur" else translator_en_ar
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**inputs)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

def translation_worker(socketio):
    while True:
        if not audio_queue.empty():
            audio_file = audio_queue.get()
            result = asr_model.transcribe(audio_file, language=None)
            lang = result['language'] if result['language'] == 'ur' else 'en'
            translation = translate_text(result['text'], lang)
            socketio.emit("subtitles", {"original": result['text'], "translated": translation})
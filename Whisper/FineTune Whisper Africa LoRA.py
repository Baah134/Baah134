# -*- coding: utf-8 -*-
"""FineTune Whisper Africa LoRA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14aKc_Dtw5wfxae4wLrKGuOTwIp1LfzfH

# Finetuning Whisper on AfriSpeech using Parameter Efficient Fine-Tuning -Lora

This project involves fine-tuning OpenAI's Whisper model using LoRA (Low-Rank Adaptation) on the AfriSpeech dataset—a multilingual African speech corpus. The goal was to improve the model's transcription accuracy for under-resourced African languages.

**Key Details:**          
Base Model: openai/whisper-large.                   

Fine-Tuning Method: Parameter-efficient fine-tuning using PEFT's LoRA

Dataset: AfriSpeech- a curated dataset with audio-transcription pairs from multiple African languages.

Training Environment: Google Colab + bitsandbytes 8-bit quantization to reduce memory usage

Use Case: Improved ASR (Automatic Speech Recognition) for African language speech inputs

**Results:**      
Evaluated the fine-tuned model on a held-out set of 100 samples

Achieved lower WER (Word Error Rate) of 0.18 compared to the base Whisper model on this subset which was 0.4

Demonstrated better handling of African accents and language-specific phonemes

## Inital Setup

Installing Required Libraries
"""

!add-apt-repository -y ppa:jonathonf/ffmpeg-4
!apt update
!apt install -y ffmpeg

!pip install datasets>=2.6.1
!pip install git+https://github.com/huggingface/transformers
!pip install librosa
!pip install evaluate>=0.30
!pip install jiwer
!pip install gradio
!pip install -q bitsandbytes datasets accelerate loralib
!pip install -q git+https://github.com/huggingface/transformers.git@main git+https://github.com/huggingface/peft.git@main

from huggingface_hub import notebook_login

notebook_login()

# Select CUDA device index
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
model_name_or_path = "openai/whisper-large"
language = "English"
language_abbr = "en"
task = "transcribe"

"""## Load Dataset"""

# Mount Drive and Set Paths
from google.colab import drive
drive.mount('/content/drive')

# Define paths
train_audio_dir = '/content/drive/MyDrive/Fine_Tuning/Train_Data/'
test_audio_dir  = '/content/drive/MyDrive/Fine_Tuning/Hundred/'

train_csv = '/content/drive/MyDrive/Fine_Tuning/train_extracted_data.csv'
test_csv  = '/content/drive/MyDrive/Fine_Tuning/Hundred_Transcriptions.csv'


import os
import librosa
import pandas as pd

#Load CSVs and Build Transcription Dictionaries
train_df = pd.read_csv(train_csv)
test_df = pd.read_csv(test_csv)

train_df['filename'] = train_df['filename'].astype(str)
test_df['audio_name'] = test_df['audio_name'].astype(str)

train_transcripts = dict(zip(train_df['filename'], train_df['transcription']))
test_transcripts  = dict(zip(test_df['audio_name'],  test_df['transcript']))

# Function to Load Dataset
def load_dataset(audio_dir, transcript_dict):
    audio_files_in_dir = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]

    data = []
    for audio_file_with_ext in audio_files_in_dir:
        # Get the filename without the .wav extension
        audio_file_base = os.path.splitext(audio_file_with_ext)[0]

        # Check if the base filename is in the transcript dictionary (for test data)
        if audio_file_base in transcript_dict:
            audio_path = os.path.join(audio_dir, audio_file_with_ext)
            waveform, _ = librosa.load(audio_path, sr=16000)
            data.append({
                "audio": waveform,
                "text": transcript_dict[audio_file_base], # Use the base filename for lookup
                "path": audio_path
            })
        # Also check if the full filename is in the transcript dictionary (for train data)
        elif audio_file_with_ext in transcript_dict:
            audio_path = os.path.join(audio_dir, audio_file_with_ext)
            waveform, _ = librosa.load(audio_path, sr=16000)
            data.append({
                "audio": waveform,
                "text": transcript_dict[audio_file_with_ext],
                "path": audio_path
            })
        else:
            print(f"Warning: No transcription found for {audio_file_with_ext} in {audio_dir}")

    return data

# Load and Prepare Datasets
train_data = load_dataset(train_audio_dir, train_transcripts)
test_data  = load_dataset(test_audio_dir,  test_transcripts)


# Print First 5 Samples
print("\nFirst 5 training samples:")
for i, sample in enumerate(train_data[:5]):
    print(f"\nSample {i+1}:")
    print(f"  Audio Path: {sample['path']}")
    print(f"  Transcription: {sample['text'][:200]}")  # limit to 200 chars

print("\nFirst 5 test samples:")
for i, sample in enumerate(test_data[:5]):
    print(f"\nSample {i+1}:")
    print(f"  Audio Path: {sample['path']}")
    print(f"  Transcription: {sample['text'][:200]}")

"""## Prepare Feature Extractor, Tokenizer and Data"""

from transformers import WhisperFeatureExtractor

feature_extractor = WhisperFeatureExtractor.from_pretrained(model_name_or_path)

from transformers import WhisperTokenizer

tokenizer = WhisperTokenizer.from_pretrained(model_name_or_path, language=language, task=task)

from transformers import WhisperProcessor

processor = WhisperProcessor.from_pretrained(model_name_or_path, language=language, task=task)

"""### Prepare Data

Re-sampling audio to 16000Hz for Whisper to work with and preparing tokens
"""

def prepare_dataset(example):
    # Convert raw waveform to input features (log-Mel spectrograms)
    example["input_features"] = feature_extractor(
        example["audio"], sampling_rate=16000
    ).input_features[0]

    # Tokenize transcript
    example["labels"] = tokenizer(example["text"]).input_ids
    return example

      # Apply to all training and test samples
train_data = [prepare_dataset(sample) for sample in train_data]
test_data  = [prepare_dataset(sample) for sample in test_data]

      #  View Final Prepared Example
print("Train Sample:")
print(train_data[0])
print("\nTest Sample:")
print(test_data[0])

"""## Training and Evaluation

### Define a Data Collator
"""

import torch

from dataclasses import dataclass
from typing import Any, Dict, List, Union


@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    processor: Any

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # split inputs and labels since they have to be of different lengths and need different padding methods
        # first treat the audio inputs by simply returning torch tensors
        input_features = [{"input_features": feature["input_features"]} for feature in features]
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")

        # get the tokenized label sequences
        label_features = [{"input_ids": feature["labels"]} for feature in features]
        # pad the labels to max length
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")

        # replace padding with -100 to ignore loss correctly
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

        # if bos token is appended in previous tokenization step,
        # cut bos token here as it's append later anyways
        if (labels[:, 0] == self.processor.tokenizer.bos_token_id).all().cpu().item():
            labels = labels[:, 1:]

        batch["labels"] = labels

        if "num_items_in_batch" in batch:

          del batch["num_items_in_batch"]


        return batch

"""Initialising the data collator"""

data_collator = DataCollatorSpeechSeq2SeqWithPadding(processor=processor)

"""### Evaluation Metrics

The word error rate (WER) will be used as the metric for evaluation.
"""

import evaluate

metric = evaluate.load("wer")

"""We then simply have to define a function that takes our model
predictions and returns the WER metric. This function, called
`compute_metrics`, first replaces `-100` with the `pad_token_id`
in the `label_ids` (undoing the step we applied in the
data collator to ignore padded tokens correctly in the loss).
It then decodes the predicted and label ids to strings. Finally,
it computes the WER between the predictions and reference labels:
"""

def compute_metrics(pred):
    pred_ids = pred.predictions
    label_ids = pred.label_ids

    # replace -100 with the pad_token_id
    label_ids[label_ids == -100] = tokenizer.pad_token_id

    # we do not want to group tokens when computing the metrics
    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = tokenizer.batch_decode(label_ids, skip_special_tokens=True)

    wer = 100 * metric.compute(predictions=pred_str, references=label_str)

    return {"wer": wer}

"""### Load a Pre-Trained Checkpoint

Loads the pre-trained Whisper large checkpoint.
"""

from transformers import WhisperForConditionalGeneration

model = WhisperForConditionalGeneration.from_pretrained(model_name_or_path, load_in_8bit=True, device_map="auto")

"""Override generation arguments - no tokens are forced as decoder outputs (see [`forced_decoder_ids`](https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.generation_utils.GenerationMixin.generate.forced_decoder_ids)), no tokens are suppressed during generation (see [`suppress_tokens`](https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.generation_utils.GenerationMixin.generate.suppress_tokens)):"""

model.config.forced_decoder_ids = None
model.config.suppress_tokens = []

"""### Post-processing on the model

Finally, we need to apply some post-processing on the 8-bit model to enable training, let's freeze all our layers, and cast the layer-norm in `float32` for stability. We also cast the output of the last layer in `float32` for the same reasons.
"""

from peft import prepare_model_for_kbit_training

model = prepare_model_for_kbit_training(model)

# Unfreeze proj_out
for name, param in model.named_parameters():
    if "proj_out" in name:
        param.requires_grad = True

"""### Apply LoRA

LoRA is applied in this step. A `PeftModel` is loaded and we specify that we are going to use low-rank adapters (LoRA) using `get_peft_model` utility function from `peft`.
"""

from peft import LoraConfig, PeftModel, LoraModel, LoraConfig, get_peft_model

config = LoraConfig(r=32, lora_alpha=64, target_modules=["q_proj", "v_proj"], lora_dropout=0.05, bias="none")

model = get_peft_model(model, config)
model.print_trainable_parameters()

"""Only using **1%** of the total trainable parameters, thereby performing **Parameter-Efficient Fine-Tuning**

### Define the Training Configuration

In the final step, we define all the parameters related to training.
"""

from transformers import Seq2SeqTrainingArguments

training_args = Seq2SeqTrainingArguments(
   output_dir="./whisper-afrispeech",
    per_device_train_batch_size=8,
    gradient_accumulation_steps=1,
    learning_rate=1e-3,
    warmup_steps=50,
    num_train_epochs=2,
    eval_strategy="epoch",
    fp16=True,
    per_device_eval_batch_size=8,
    generation_max_length=128,
    logging_steps=25,
    remove_unused_columns=False,
    label_names=["labels"],
)

from transformers import Seq2SeqTrainer

trainer = Seq2SeqTrainer(
    args=training_args,
    model=model,
    train_dataset=train_data,
    eval_dataset=test_data,
    data_collator=data_collator,
    tokenizer=processor.feature_extractor,
)
model.config.use_cache = False

trainer.train()

model_name_or_path = "openai/whisper-large"
peft_type = model.peft_config["default"].peft_type
peft_model_id = "Baah134/" + f"{model_name_or_path}-{peft_type}-colab".replace("/", "-")

model.push_to_hub(peft_model_id)
print(peft_model_id)

"""# Evaluation and Inference

Loads model from Hugging Face Repo
"""

from peft import PeftModel, PeftConfig
from transformers import WhisperForConditionalGeneration, Seq2SeqTrainer

peft_model_id = "Baah134/openai-whisper-large-PeftType.LORA-colab"
peft_config = PeftConfig.from_pretrained(peft_model_id)
model = WhisperForConditionalGeneration.from_pretrained(
    peft_config.base_model_name_or_path, load_in_8bit=True, device_map="auto"
)
model = PeftModel.from_pretrained(model, peft_model_id)

from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
import gc

eval_dataloader = DataLoader(test_data, batch_size=8, collate_fn=data_collator)

model.eval()
for step, batch in enumerate(tqdm(eval_dataloader)):
    with torch.cuda.amp.autocast():
        with torch.no_grad():
            generated_tokens = (
                model.generate(
                    input_features=batch["input_features"].to("cuda"),
                    decoder_input_ids=batch["labels"][:, :4].to("cuda"),
                    max_new_tokens=255,
                )
                .cpu()
                .numpy()
            )
            labels = batch["labels"].cpu().numpy()
            labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
            decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
            metric.add_batch(
                predictions=decoded_preds,
                references=decoded_labels,
            )
    del generated_tokens, labels, batch
    gc.collect()
wer = 100 * metric.compute()
print(f"{wer=}")

"""Print first batch for qualitative analysis."""

from jiwer import wer as jiwer_wer

# Get one batch from the dataloader
batch = next(iter(eval_dataloader))

model.eval()
with torch.cuda.amp.autocast():
    with torch.no_grad():
        generated_tokens = (
            model.generate(
                input_features=batch["input_features"].to("cuda"),
                decoder_input_ids=batch["labels"][:, :4].to("cuda"),
                max_new_tokens=255,
            )
            .cpu()
            .numpy()
        )

# Process labels and decode
labels = batch["labels"].cpu().numpy()
labels = np.where(labels != -100, labels, processor.tokenizer.pad_token_id)
decoded_preds = processor.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
decoded_labels = processor.tokenizer.batch_decode(labels, skip_special_tokens=True)

# Print first batch results
print("=== Sample Results (First Batch) ===\n")
for i, (ref, pred) in enumerate(zip(decoded_labels, decoded_preds)):
    sample_wer = jiwer_wer(ref, pred) * 100
    print(f"Sample {i+1}")
    print(f"Ground Truth : {ref}")
    print(f"Prediction    : {pred}")
    print(f"WER           : {sample_wer:.2f}%\n")
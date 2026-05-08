# -*- coding: utf-8 -*-
import sys

print(sys.version)

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

train_df = pd.read_excel('/content/drive/MyDrive/train_df_v3.xlsx')

train_df.info()

train_df.drop_duplicates(subset='filtered_texts', keep='first', inplace=True, ignore_index=True)

train_df

train_df['labels'].value_counts()

# 0번 데이터 40퍼 개수 구하기
((749+432+294)/2)*6

train_0 = train_df[train_df['labels'] == 0] # 레이블 0만 추출
train_0_set = train_0.sample(n=4425, random_state = 0) # 레이블 0 데이터 프레임에서 랜덤으로 n개 추출
train_notclean = train_df[train_df['labels'] != 0] # labels = 0 인 값 제거한 데이터 프레임
train_df2 = pd.concat([train_0_set, train_notclean])

train_df2

train_df2.to_excel('kcbert_train_60per_v2.xlsx')

"""### 텍스트 전처리"""

!pip3 install soynlp emoji

import re
import emoji
from soynlp.normalizer import repeat_normalize

pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-ㅣ가-힣]+')
url_pattern = re.compile(
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

def clean(x):
    x = pattern.sub(' ', x)
    x = emoji.replace_emoji(x, replace='') #emoji 삭제
    x = url_pattern.sub('', x)
    x = x.strip()
    x = repeat_normalize(x, num_repeats=2)
    return x

# texts 컬럼에서 특수문자를 제거
train_df2['clean_texts'] = train_df2['filtered_texts'].apply(clean)

from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(
    train_df2['filtered_texts'], train_df2['labels'], test_size=0.3, random_state = 0
)

X_train = X_train.tolist()
y_train = y_train.tolist()

X_val = X_val.tolist()
y_val = y_val.tolist()

from transformers import AutoTokenizer, AutoModelForSequenceClassification


tokenizer = AutoTokenizer.from_pretrained("beomi/kcbert-base")
model = AutoModelForSequenceClassification.from_pretrained("beomi/kcbert-base", num_labels = 4)

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW

class CustomDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = self.texts[index]
        label = self.labels[index]

        encoding = self.tokenizer(text, padding='max_length', truncation=True, max_length=self.max_length, return_tensors='pt')
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()

        return {'input_ids': input_ids, 'attention_mask': attention_mask, 'label': label}

# 원하는 최대 시퀀스 길이
max_length = 64

t_labels = torch.tensor(y_train, dtype=torch.long)
v_labels = torch.tensor(y_val, dtype=torch.long)
train_dataset = CustomDataset(X_train, t_labels, tokenizer, max_length)
val_dataset = CustomDataset(X_val, v_labels , tokenizer, max_length)

"""### 하이퍼 파라미터 튜닝"""

from transformers import get_linear_schedule_with_warmup

def train_and_evaluate(model, learning_rate, epochs, batch_size, device):
    # 데이터 로더 생성
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    valid_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True)

    # 모델
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # 옵티마이저 및 손실 함수 설정
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

    total_steps = len(train_dataloader) * epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

    for epoch in range(epochs):
        model.train()
        total_loss = 0

        for batch in train_dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            scheduler.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_dataloader)
        print(f"Epoch {epoch+1}/{epochs} - Avg Loss: {avg_loss:.4f}")

        model.eval()
        val_total_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for val_batch in valid_dataloader:
                val_input_ids = val_batch['input_ids'].to(device)
                val_attention_mask = val_batch['attention_mask'].to(device)
                val_labels = val_batch['label'].to(device)

                # 손실 계산
                val_outputs = model(val_input_ids, attention_mask=val_attention_mask)
                val_logits = val_outputs.logits
                val_loss = criterion(val_logits, val_labels)
                val_total_loss += val_loss.item()

                # 정확도 계산
                val_preds = val_logits.argmax(dim=1)
                correct += (val_preds == val_labels).sum().item()
                total += val_labels.size(0)

        val_avg_loss = val_total_loss / len(valid_dataloader)
        val_accuracy = correct / total
        print(f"Validation Loss: {val_avg_loss:.4f} - Validation Accuracy: {val_accuracy:.4f}")

    return val_avg_loss, val_accuracy

# 하이퍼파라미터 설정
learning_rates = [2e-5, 3e-05]
epochs_list = [5, 6, 7, 8]
batch_sizes = [8, 16]

best_val_accuracy = 0
best_hyperparams = {}

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

for learning_rate in learning_rates:
    for epochs in epochs_list:
      for batch_size in batch_sizes:
        print(f"Training with learning rate: {learning_rate}, epochs: {epochs}, batch_size: {batch_size}")
        model = AutoModelForSequenceClassification.from_pretrained("beomi/kcbert-base", num_labels = 4)  # 모델을 다시 초기화
        val_loss, val_accuracy = train_and_evaluate(model, learning_rate, epochs, batch_size, device)

        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            best_hyperparams = {'learning_rate': learning_rate, 'epochs': epochs, 'batch_size': batch_size}

print(f"Best Hyperparameters: {best_hyperparams} with Validation Accuracy: {best_val_accuracy:.4f}")

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# 하이퍼파라미터 설정
learning_rate = 3e-05
epochs = 6
batch_size = 8

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
valid_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True)

# 옵티마이저 및 손실 함수 설정
optimizer = AdamW(model.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

# 모델 재학습
for epoch in range(epochs):
    model.train()
    total_loss = 0

    for batch in train_dataloader:
        input_ids = batch['input_ids']
        attention_mask = batch['attention_mask']
        labels = batch['label']

        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)

        # 그래디언트 초기화
        optimizer.zero_grad()
        # 모델에 입력을 주어 예측을 생성합니다.
        outputs = model(input_ids, attention_mask=attention_mask)
        # 모델 출력에서 로짓(분류에 대한 점수)을 얻습니다.
        logits = outputs.logits
        # 손실을 계산합니다.
        loss = criterion(logits, labels)
        # 역전파를 통해 그래디언트 계산
        loss.backward()
        # 옵티마이저를 사용해 가중치를 업데이트
        optimizer.step()
        # 에포크 전체 손실을 누적합니다.
        total_loss += loss.item()

    # 에포크 평균 손실 계산
    avg_loss = total_loss / len(train_dataloader)
    # 에포크별 손실 출력
    print(f"Epoch {epoch+1}/{epochs} - Avg Loss: {avg_loss:.4f}")

    # 모델 평가
    model.eval()
    val_total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for val_batch in valid_dataloader:
            # Validation 데이터 가져오기
            val_input_ids = val_batch['input_ids']
            val_attention_mask = val_batch['attention_mask']
            val_labels = val_batch['label']

            val_input_ids = val_input_ids.to(device)
            val_attention_mask = val_attention_mask.to(device)
            val_labels = val_labels.to(device)

            # 모델 예측
            val_outputs = model(val_input_ids, attention_mask=val_attention_mask)
            val_logits = val_outputs.logits

            # 손실 계산
            val_loss = criterion(val_logits, val_labels)
            val_total_loss += val_loss.item()

            # 정확도 계산
            val_preds = val_logits.argmax(dim=1)
            correct += (val_preds == val_labels).sum().item()
            total += val_labels.size(0)

    val_avg_loss = val_total_loss / len(valid_dataloader)
    val_accuracy = correct / total
    print(f"Validation Loss: {val_avg_loss:.4f} - Validation Accuracy: {val_accuracy:.4f}")

import torch

model_save_path = '/content/drive/MyDrive/model/KcBERT_v7_60per.pth'
torch.save(model.state_dict(), model_save_path)
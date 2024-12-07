import pandas as pd
from transformers import BertTokenizer
from sklearn.preprocessing import LabelEncoder

# Charger les données
df = pd.read_csv("articles.csv")

# Convertir les articles en texte
df['article'] = df['article'].astype(str)

# Utiliser un tokenizer pré-entraîné de BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenisation des articles
tokenized_data = tokenizer(df['article'].tolist(), padding='max_length', truncation=True, return_tensors='pt')

# Encodage des sujets
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['subject'])

# Obtenir les labels sous forme de tableau
labels = df['label'].values

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertForSequenceClassification, AdamW

# Créer un Dataset personnalisé pour les articles
class ArticleDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Créer le DataLoader
dataset = ArticleDataset(tokenized_data, labels)
train_loader = DataLoader(dataset, batch_size=8, shuffle=True)

# Charger le modèle BERT pour la classification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label_encoder.classes_))
optimizer = AdamW(model.parameters(), lr=5e-5)

# Entraîner le modèle
model.train()
for epoch in range(3):
    for batch in train_loader:
        input_ids = batch['input_ids'].squeeze(1)
        attention_mask = batch['attention_mask'].squeeze(1)
        labels = batch['labels']

        # Calculer la perte et mettre à jour les poids
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    print(f"Époque {epoch + 1} terminée, perte : {loss.item()}")

# Enregistrer le modèle
model.save_pretrained("bert_model_subject_classification")
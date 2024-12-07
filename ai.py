from sklearn.preprocessing import LabelEncoder
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn.functional as F

# Charger le tokenizer et le modèle
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert_model_subject_classification")

# Ajuster le LabelEncoder avec les classes cibles
# Remplacez par vos propres labels
classes = ["sport", "politique", "economie", "intelligence+artificielle", "quantique"]
label_encoder = LabelEncoder()
label_encoder.fit(classes)

# Exemple d'article à classifier
article = input('''>>
''')

# Tokeniser l'article
inputs = tokenizer(article, padding="max_length", truncation=True, return_tensors="pt")

# Prédire le sujet
model.eval()
with torch.no_grad():
    outputs = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
    logits = outputs.logits

# Appliquer softmax pour obtenir les probabilités
probabilities = F.softmax(logits, dim=1).squeeze()

top_3_indices = torch.topk(probabilities, 3).indices
top_3_probs = torch.topk(probabilities, 3).values

# Convertir les indices en labels
top_3_labels = label_encoder.inverse_transform(top_3_indices.numpy())

# Afficher les résultats
print("Sujets prédits avec probabilités :")
for label, prob in zip(top_3_labels, top_3_probs):
    print(f"{label}: {prob.item() * 100:.2f}%")
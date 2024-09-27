from transformers import AutoModelForSequenceClassification, XLMRobertaTokenizer
import torch

# Load tokenizer and model
tokenizer = XLMRobertaTokenizer.from_pretrained("LocalDoc/language_detection")
model = AutoModelForSequenceClassification.from_pretrained("LocalDoc/language_detection")

# Prepare text
text = "Это тестовая фраза!"
encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)

# Prediction
model.eval()
with torch.no_grad():
    outputs = model(**encoded_input)

# Process the outputs
logits = outputs.logits
probabilities = torch.nn.functional.softmax(logits, dim=-1)
predicted_class_index = probabilities.argmax().item()
labels = ["az", "ar", "bg", "de", "el", "en", "es", "fr", "hi", "it", "ja", "nl", "pl", "pt", "ru", "sw", "th", "tr", "ur", "vi", "zh"]
predicted_label = labels[predicted_class_index]
print(f"Predicted Language: {predicted_label}")

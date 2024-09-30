from transformers import AutoModelForSequenceClassification, XLMRobertaTokenizer
import torch

tokenizer = XLMRobertaTokenizer.from_pretrained("LocalDoc/language_detection")
model = AutoModelForSequenceClassification.from_pretrained("LocalDoc/language_detection")


def lang(text: str):
    encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)

    model.eval()
    with torch.inference_mode():
        outputs = model(**encoded_input)

    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    predicted_class_index = probabilities.argmax().item()
    labels = ["az", "ar", "bg", "de", "el", "English", "es", "fr", "hi", "it", "ja", "nl", "pl", "pt", "Russian", "sw", "th", "tr", "ur", "vi", "zh"]
    predicted_label = labels[predicted_class_index]
    return predicted_label

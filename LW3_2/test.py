# import re
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# WHITESPACE_HANDLER = lambda k: re.sub(r'\s+', ' ', re.sub(r'\n+', ' ', k.strip()))

# article_text = """Videos that say approved vaccines are dangerous and cause autism, cancer or infertility are among those that will be taken down, the company said.  The policy includes the termination of accounts of anti-vaccine influencers.  Tech giants have been criticised for not doing more to counter false health information on their sites.  In July, US President Joe Biden said social media platforms were largely responsible for people's scepticism in getting vaccinated by spreading misinformation, and appealed for them to address the issue.  YouTube, which is owned by Google, said 130,000 videos were removed from its platform since last year, when it implemented a ban on content spreading misinformation about Covid vaccines.  In a blog post, the company said it had seen false claims about Covid jabs "spill over into misinformation about vaccines in general". The new policy covers long-approved vaccines, such as those against measles or hepatitis B.  "We're expanding our medical misinformation policies on YouTube with new guidelines on currently administered vaccines that are approved and confirmed to be safe and effective by local health authorities and the WHO," the post said, referring to the World Health Organization."""

# model_name = "csebuetnlp/mT5_multilingual_XLSum"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


# input_ids = tokenizer.encode(
#     [WHITESPACE_HANDLER(article_text)],
#     return_tensors="pt",
#     padding="max_length",
#     truncation=True,
#     max_length=512
# )["input_ids"]

# output_ids = model.generate(
#     input_ids=input_ids,
#     max_length=84,
#     no_repeat_ngram_size=2,
#     num_beams=4
# )[0]

# summary = tokenizer.decode(
#     output_ids,
#     skip_special_tokens=True,
#     clean_up_tokenization_spaces=False
# )

# print(summary)

# import torch
# from transformers import GPT2Tokenizer, T5ForConditionalGeneration 
# tokenizer = GPT2Tokenizer.from_pretrained('RussianNLP/FRED-T5-Summarizer',eos_token='</s>')
# model = T5ForConditionalGeneration.from_pretrained('RussianNLP/FRED-T5-Summarizer')
# device='cuda'
# model.to(device)

# input_text='<LM> Сократи текст.\n В деревне, затерянной среди зелёных холмов, жил старик по имени Иван. Его жизнь протекала медленно и размеренно. Каждое утро Иван выходил на поля, чтобы заботиться о своём скромном участке земли. Он выращивал картофель и морковь, которые были его главным источником пищи. Вечера старик проводил у камина, читая книги и вспоминая молодость. Жизнь в деревне была тяжёлая, но Иван находил в ней простые радости.'
# input_ids=torch.tensor([tokenizer.encode(input_text)]).to(device)
# outputs=model.generate(input_ids,eos_token_id=tokenizer.eos_token_id,
#                     num_beams=5,
#                     min_new_tokens=17,
#                     max_new_tokens=200,
#                     do_sample=True,
#                     no_repeat_ngram_size=4,
#                     top_p=0.9)
# print(tokenizer.decode(outputs[0][1:]))


from openai import OpenAI

client = OpenAI(
    api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
    base_url="https://api.vsegpt.ru/v1",
)

prompt = "Сократи текст и оставь только самое важное"

messages = []
#messages.append({"role": "system", "content": system_text})
messages.append({"role": "user", "content": prompt})

response_big = client.chat.completions.create(
    model="openai/gpt-4o-mini", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
    messages=messages,
    temperature=0.7,
    n=1,
    max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
    extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
)

#print("Response BIG:",response_big)
response = response_big.choices[0].message.content
print("Response:",response)


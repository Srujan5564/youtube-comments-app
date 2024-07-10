from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

# our pretrained model is distibert-base-uncased
checkpoint = "distilbert-base-uncased"

# loding our model form after fine-tuning a pre-trained model
# model = AutoModelForSequenceClassification.from_pretrained("/home/srujan/Projects/Youtube-comments-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("Srujan5564/my-distilbert")


# defining a tonkenizer
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

# creating a pipeline for predicitions
pipe = TextClassificationPipeline(model = model, tokenizer = tokenizer, top_k=1) #return_all_scores = True)

# comment = "i hate u"
# pred = pipe(comment)
# print(pred)

def predict_sentiment(comment,key="score"):
    return pipe(comment)[0][0]["label"]


# print(predict_sentiment(comment))








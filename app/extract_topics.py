import json
import pickle
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter

# Process messages according to pre-trainined Naive Bayes classifier
# Remove off-topic messages

    # import requests

def preprocess(sentence):
    return [wordnet_lemmatizer.lemmatize(word.lower()) for word in word_tokenize(sentence)]

def get_features(text, setting):
    if setting == 'bow':
        return {word: count for word, count in Counter(preprocess(text)).items() if not word in stoplist}
    else:
        return {word: True for word in preprocess(text) if not word in stoplist}

# load classifier
classifier_f = open("naivebayes.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

# load stoplist and lemmatizer
stoplist = stopwords.words('english')
wordnet_lemmatizer = WordNetLemmatizer()
data = json.loads(open('example.json').read())

# classify text
messages = []
on_topic_messages = []
for i in range(len(data["items"])):
    message = (data["items"][i]["text"])
    messages.append(message)
    fs = get_features(message, 'bow')
    prob_dist = classifier.prob_classify(fs)
    prob_on = prob_dist.prob('on')
    prob_off = prob_dist.prob('off')
    if prob_on >= 0.5 and prob_off <= 0.5:
        on_topic_messages.append(message)
print(on_topic_messages)
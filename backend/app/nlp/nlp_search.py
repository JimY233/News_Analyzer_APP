import nltk
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('punkt')
import logging

def convert(text): 
    content = ""
    if isinstance(text,str):
        content = text
    elif isinstance(text,tuple) or isinstance(text,list):
        content = "".join('%s' %i for i in text) 
    return content

def search_nlp(search,text):
    content = convertfunc.convert(text)
    word = nltk.word_tokenize(content)
    freqdist = FreqDist(word)
    if search in freqdist.keys():
        dist = freqdist[search]
        return dist
    else:
        return 0

def nlp_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment = sid.polarity_scores(text)
    return sentiment

def main():
    text = "Today the weather in Boston is sunny. The weather today is pretty good and thus I feel happy"
    print(search_nlp("weather",text))
    print(nlp_sentiment(text))

if __name__ == "__main__":
    main()



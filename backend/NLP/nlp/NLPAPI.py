import os

# Imports the Google Cloud client library
from google.cloud import language_v1

#from google.oauth2 import service_account
#import json

#Use github secret passed as environment var
#service_account_info = json.loads(os.environ['GOOGLE_SECRET'])
#credentials = service_account.Credentials.from_service_account_info(service_account_info)                                
#client = language_v1.LanguageServiceClient(credentials=credentials)

#credential_path = r"C:\Users\yjm57\OneDrive\Desktop\key\ec500-9845474843db.json"
credential_path = r"/home/ubuntu/key/ec500-840463134781.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Instantiates a client
client = language_v1.LanguageServiceClient()


def NLP_analyze(text):
    # The text to analyze
    #text = u"Hello, world!"
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    #print("Text: {}".format(text))
    #print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

    return sentiment


if __name__ == '__main__':
    text = u"Hello, world!"
    print(NLP_analyze(text))


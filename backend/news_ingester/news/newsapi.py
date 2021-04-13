import pprint
import requests

secret = 'b511f31e10b24ecf8501eb67d0f507e6'

def newsapi(keyword, num=1):
    # Define the endpoint
    url = 'https://newsapi.org/v2/everything?'

    # Specify the query and number of returns
    parameters = {
        'q': keyword, 
        'pageSize': num,  # maximum is 100, number of results per page, since page is 1 by default
        #'page': 1,
        'apiKey': secret, 
        'language':'en',
        'sort_by':'relevancy',
    }

    # Make the request
    response = requests.get(url, params=parameters)

    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    #pprint.pprint(response_json)

    #for i in response_json['articles']:
        #print(i['title'])
        #print(i['content'])

    return response_json


if __name__ == '__main__':
    keyword = 'covid19'
    num = 1
    response_json = newsapi(keyword,num)

    for i in response_json['articles']:
        print(i['title']+i['content'])



import requests
import json

api_key = "b45e063a-f2bf-4751-a06f-25f5e2af0728"

def gapi(keyword, num=1):
    # set up base url
    base_url = "https://content.guardianapis.com/"

    # set up parameters
    search_keyword = keyword
    data_format = 'json'
    page = 1
    page_size = num
    showfields = 'body'

    payload = {
        'api-key':              "b45e063a-f2bf-4751-a06f-25f5e2af0728",
        'q':                    keyword,
        'format':               'json',
        'page-size':            num,
        'show-fields':          'all'

    }

    # combine url
    finalized_url = "{}search?q={}&format={}&order-by=relevance&page={}&page-size={}&api-key={}&show-fields={}".format(base_url, search_keyword, data_format, page, page_size, api_key, showfields)

    # perform the request and print the query
    response = requests.get(url = finalized_url, params = {})

    print(response.json()['response']['results'][0]['webTitle'])
    print(response.json()['response']['results'][0]['webUrl'])
    print(response.json()['response']['results'][0]['fields']['body'])

    # output the responses to a file
    return response.json()['response']

if __name__ == '__main__':
    gapi("covid")
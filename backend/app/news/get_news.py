import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp

def download_news(url):
    '''
    r1 = requests.get(url)
    coverpage = r1.content
    soup1 = BeautifulSoup(coverpage, 'html.parser')
    div = BeautifulSoup(r1.content).find("div",{"class":"cnn_strylftcntnt"})
    print("".join([p.text for p in div.find_all_next("p")]))
    '''

    r = requests.get(url)

    data = BeautifulSoup(r.content).find_all("div",{"class":"cnnMPContentHeadline"})

    pp([d.a["href"] for d in data[:10]])

    for link in (d.a["href"] for d in data):
        r = requests.get(link)
        div = BeautifulSoup(r.content).find("div",{"class":"cnn_strylftcntnt"})
        if div:
            print("Text for {}".format(link))
            print("".join([p.text for p in div.find_all_next("p")]))
        else:
            print("No text for link {}".format(link))
        print()



if __name__ == '__main__':
    url = "https://www.cnn.com/world"
    download_news(url)

import string
from nltk.corpus import stopwords
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
from nltk.stem.wordnet import WordNetLemmatizer


def removePunctuations(text, ignore="", removeNumbers=True):

    if(ignore != ""):
        punctuationsWithoutFullStop = string.punctuation.replace(ignore, "")
        # this is to ignore full  stops
    else:
        punctuationsWithoutFullStop = string.punctuation
    # full stops will remain in the string
    transtable = {ord(c): None for c in punctuationsWithoutFullStop}
    newText = text.translate(transtable)
    if(removeNumbers is True):
        newText = re.sub('[0-9]+', "", newText)
    return newText


def removeStopWords(splitText):
    filtered_words = [
        w for w in splitText if w not in stopwords.words('english')]
    return filtered_words


def fetchSentsFromPages(urlList):
    contents = []
    for count in range(0, 12):
        link = urlList[count]
        try:
            request_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'Connection': 'keep-alive',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
            request = Request(link, headers=request_headers)
            res = urlopen(request)
        except:
            continue
        soup = BeautifulSoup(''.join(res.read().decode('utf-8')), "lxml")
        # remove all script and style elements
        for script in soup(["script", "style", "a"]):
            script.extract()
        body = soup.html.body.get_text()
        body = body.replace("\n", " ")
        body = body.replace("\t", " ")
        body = body.replace("\r", " ")
        # body = body.lower()
        # body = stemWords(body, rmStopWords=True)
        # sentenece tokenize  also use concordance.
        # body_tokens= word_tokenize(body)
        # text =Text(body_tokens)
        # body = removePunctuations(body, ignore=".")
        attr = link.lstrip("http://localhost/").rstrip(".html").lstrip('wiki/')
        contents.append((attr,body))
    return contents


def stemWords(sent, rmStopWords=False):
    sent = sent.split()
    if(rmStopWords is True):
        sent = removeStopWords(sent)
    retSent = []
    for word in sent:
        retSent.append(WordNetLemmatizer().lemmatize(word, 'v'))
    sent = " ".join(retSent)
    return sent

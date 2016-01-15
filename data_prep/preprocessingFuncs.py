import string
from nltk.corpus import stopwords
from urllib.request import urlopen
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
    for count in range(0, 1):
        link = urlList[count]
        try:
            res = urlopen(link)
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
        body = body.lower()
        body = stemWords(body, rmStopWords=True)
        # sentenece tokenize  also use concordance.
        # body_tokens= word_tokenize(body)
        # text =Text(body_tokens)
        body = removePunctuations(body, ignore=".")
        contents.append(body)
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

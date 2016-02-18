import re
from nltk import sent_tokenize
from data_prep.open_nlp import OpenNLP
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob.np_extractors import ConllExtractor
import sys


def parseContents(contentList):
    tupleList = []
    posTagger = OpenNLP("/home/rohith/nitk/apache-opennlp-1.6.0", "POSTagger", "en-pos-maxent.bin")
    chunker = OpenNLP("/home/rohith/nitk/apache-opennlp-1.6.0", "ChunkerME", "en-chunker.bin")
    for item in contentList:
        attr = item[0]
        content = item[1]
        
        content = content.replace('\n','')
        sentences = sent_tokenize(content)
        for sentence in sentences:
            print('#'+sentence, file=sys.stderr)
            extractor = ConllExtractor()
            np = TextBlob(sentence, np_extractor=extractor).noun_phrases
            yield attr, np.lemmatize()
#             pos = posTagger.parse(sentence)
#             chunks = chunker.parse(pos)
#             chunks = chunks.decode()
#             # finding first matching NP
#             NP1 = re.search(r"\[NP (\w+\s?[$&+,:;=?@#|'<>.^*()%!-]*)+\]",chunks)
#             if NP1:
#                 chunks = chunks.replace(NP1.group(), '')
#                 NP1 = NP1.group().replace('[NP','').replace(']','')
#                 NP1 = re.sub(r"_(\w)+", '', NP1).strip()
#             
#             # finding first VP
#             VP = re.search(r"\[VP (\w+\s?[$&+,:;=?@#|'<>.^*()%!-]*)+\]",chunks)
#             if VP:
#                 chunks = chunks.replace(VP.group(), '')
#                 VP = VP.group().replace('[VP','').replace(']','')
#                 VP = re.sub(r"_(\w)+", '', VP).strip()
#                 # if VP is a stopword then select next NP as VP
#                 if VP in stopwords.words():
#                     VP = re.search(r"\[NP (\w+\s?[$&+,:;=?@#|'<>.^*()%!-]*)+\]",chunks)
#                     if VP:
#                         chunks = chunks.replace(VP.group(), '')
#                         VP = VP.group().replace('[NP','').replace(']','')
#                         VP = re.sub(r"_(\w)+", '', VP).strip() 
#             
#             # finding 2nd NP 
#             NP2 = re.search(r"\[NP (\w+\s?[$&+,:;=?@#|'<>.^*()%!-]*)+\]",chunks)
#             if NP2:
#                 chunks = chunks.replace(NP2.group(), '')
#                 NP2 = NP2.group().replace('[NP','').replace(']','')
#                 NP2 = re.sub(r"_(\w)+", '', NP2).strip()  
#                                          
#             if NP1 and VP and NP2:
#                 # print(str((NP1, VP, NP2)), file=sys.stderr)
#                 #yield (NP1, VP, NP2)
#                 return

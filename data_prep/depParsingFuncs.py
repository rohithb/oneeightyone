import re
from .stanford_parser import StanfordParser


def parseContents(contentList):
    typedDep = ""
    depGraphList = []
    str1 = []
    # to make the whole list into a single item
    str1.append('. '.join(contentList))
    # otherwise the parser need to be
    # initialised many times.
    parser = StanfordParser("/home/rohith/nitk/stanford-parser")
    for content in str1:
        typedDep += parser.parse(content)
        typedDep = re.sub('[0-9-]+', "", typedDep)  # to remove numbers and '-'
        rx = re.compile("\((.+), (.+)\)")
        depGraphList.append(rx.findall(typedDep))
        # import string
        # string.split(inputString, '\n')  # --> ['Line 1', 'Line 2', 'Line 3']
    return depGraphList

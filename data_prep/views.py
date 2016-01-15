from django.http import HttpResponse
from .preprocessingFuncs import fetchSentsFromPages
from .depParsingFuncs import parseContents
import logging


logger = logging.getLogger(__name__)


def fetchBackgroundInfo(request):

    urlList = ['https://en.wikipedia.org/wiki/Startup_company',
               'https://en.wikipedia.org/wiki/Takeover',
               'https://en.wikipedia.org/wiki/Mergers_and_acquisitions']
    contents = fetchSentsFromPages(urlList)
    logger.info('Contents fetched')
    depGraphList = parseContents(contents)
    return HttpResponse(depGraphList)

"""
CSE7390 Quest 3: Web Scraping with BeautifulSoup

The following python module will scrape text from three URLs.
For each URL, a dictionary of words(keys) and their frequencies(values) will be generated.
A dictionary of dictionaries will then be created that maps each URL to its word:frequency dictionary.
These dictionaries will then be stored as pickle files.

Methods are also included to generate a pickle file from a dictionary,
generate a JSON file from the pickle file,
and generate a dictionary of the three most frequent words and their associated frequencies.
"""

__STUDENT_ID__  = "47555408"
__CODING_NAME__ = "tkyaagba"

#import declarations
import re
import urllib.request
import pickle
import pprint

from bs4 import BeautifulSoup

#Dictionary of SMU Schools and Colleges
__SMU_COLLEGES__ = {
    'arts':'meadows', #not fully secure
    'business':'cox',
    'education':'simmons',#not fully secure
    'engineering':'lyle',
    'humanities': 'dedman',
    'law':'law', #not fully secure #school of law is also called 'dedman' but smu.edu/law will redirect to 'law.smu.edu/smu-dedman-school-of-law'
    'smu': '',
    'theology':'perkins',
    }

__SMU_URL__ = "http://www.smu.edu"

#generates a valid URL given the name of an SMU college
def genUrl(college):
    return '%s/%s' % (__SMU_URL__, __SMU_COLLEGES__[college])

#Method takes a URL argument and returns a <class 'bytes'> object containing the HTML code (content AND markups)
def getHtml(someUrl):
    urlObj = urllib.request.Request(someUrl)
    urlReader = urllib.request.urlopen(urlObj)
    urlContentBytes = urlReader.read()
    return urlContentBytes

#Method takes a URL, strips out the scripts, CSS, HTML tags and returns only the text content
def getTextFromHtml(someUrl):
    webText = getHtml(someUrl)
    soup = BeautifulSoup(webText,"html.parser")
    #remove scripts and style specifications
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]
    return soup.get_text()

#Method takes a string argument and returns a dictionary with each unique word as a key and its frequency of occurrence as the value
def getWordAndFreq(someString):
    #create list of all words in the string, ignore case
    wordList = re.findall(r'\w+', someString, flags=re.IGNORECASE)
    #create a list of all unique words.
    uniqueWords = set(wordList)
    twoDimList = [re.findall(item, someString, flags=re.IGNORECASE) for item in uniqueWords]
    frequencyList = [len(item) for item in twoDimList]
    wordAndFreq = dict(zip(uniqueWords,frequencyList))
    return wordAndFreq

#Method takes a dictionary and filename as arguments, then creates a pickle file from the dictionary
def genPickleFromUrlList(urlList, pickleFileName):
    pickle.dump(urlList, pickleFileName)
    
#pprint.PrettyPrinter(indent=3).pprint(getWordAndFreq(getTextFromHtml(genUrl('smu'))))
#pprint.PrettyPrinter(indent=3).pprint(getWordAndFreq(getTextFromHtml(genUrl('engineering'))))
pprint.PrettyPrinter(indent=3).pprint(getWordAndFreq(getTextFromHtml(genUrl('business'))))
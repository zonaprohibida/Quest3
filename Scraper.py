"""
CSE7390 Quest 3: Web Scraping with BeautifulSoup

The following python module will scrape text from three URLs.
For each URL, a dictionary of words(keys) and their frequencies(values) will be generated.
A dictionary of dictionaries will then be created that maps each URL to its word:frequency dictionary.
These dictionaries will then be stored as pickle files.

Methods are also included to:
1. Generate a pickle file from a dictionary,
2. Generate a JSON file from the pickle file,
3. Generate a dictionary of the three most frequent words and their associated frequencies.
"""

__STUDENT_ID__  = "47555408"
__CODING_NAME__ = "tkyaagba"

#import declarations
import re
import urllib.request
import pickle
import json
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
__PICKLE_FILE__ = "urlDictFile.pickle"
__JSON_FILE__ = "urlDictFile.json"
__COLLEGE_LIST__ = ['smu', 'engineering', 'business']


"""
A valid url for the website of an SMU college takes the following form:
https://www.smu.edu/<collegeName>
where <collegeName> is any of the values listed in the __SMU_COLLEGES__ dictionary
i.e. if genUrl() is passed 'engineering' as an argument, it will return 'https://www.smu.edu/lyle
"""
#generates a valid URL given the name of an SMU college
def genUrl(college):
    return '%s/%s' % (__SMU_URL__, __SMU_COLLEGES__[college])

#takes a URL argument and returns a <class 'bytes'> object containing the HTML code (content AND markups)
def getHtml(someUrl):
    urlObj = urllib.request.Request(someUrl)
    urlReader = urllib.request.urlopen(urlObj)
    urlContentBytes = urlReader.read()
    return urlContentBytes

#takes a URL, strips out the scripts, CSS, HTML tags and returns only the text content
def getTextFromHtml(someUrl):
    webText = getHtml(someUrl)
    soup = BeautifulSoup(webText,"html.parser")
    #remove scripts and style specifications
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]
    return soup.get_text().lower()

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

def genDictFromCollegeName(college):
    validUrl = genUrl(college)
    urlTextContent = getTextFromHtml(validUrl)
    wordDict = getWordAndFreq(urlTextContent)
    return wordDict

def genDictOfDicts(collegeList):
    dictOfDicts = {}
    for college in collegeList:
        validUrl = genUrl(college)
        dictOfDicts[validUrl] = genDictFromCollegeName(college)
    return dictOfDicts

#Method takes a dictionary and filename as arguments, then creates a pickle file from the dictionary
def genPickleFromUrlList(urlList, pickleFileName):
    with open(pickleFileName, 'wb') as fileWriter:
        pickle.dump(urlList, fileWriter)

#Takes a pickle filename and a JSON filename as arguments and stores the data from the pickle file in a JSON file
def genJsonFromPickle(pickleFileName, JsonFileName):
    with open(pickleFileName, 'rb') as fileReader:
        unpickledData = pickle.load(fileReader)
    
    with open(JsonFileName, 'w') as fileWriter:
        json.dump(unpickledData, fileWriter, indent=4, sort_keys=True)

def genTopWords(someDict, n):
    sortedTuples = sorted(someDict.items(), key = lambda x: x[1], reverse=True)
    topN = sortedTuples[:n]
    return [dict(topN).keys(), dict(topN).values()]
        

#Method takes a pickle file name, and an integer as arguments
def genDictTopWords(pickleFileName, nTopWords):
    
    with open(pickleFileName, 'rb') as fileReader:
        fullDict = pickle.load(fileReader)
    
    filteredDict = {}
    for key in fullDict:
        filteredDict[key] = genTopWords(fullDict[key], nTopWords)
        
    return filteredDict

def main():
    #create dictionary of dictionaries
    superDict = genDictOfDicts(__COLLEGE_LIST__)
    
    #create pickle file from dictionary above
    genPickleFromUrlList(superDict, __PICKLE_FILE__)
    
    #create JSON file from pickle file
    genJsonFromPickle(__PICKLE_FILE__, __JSON_FILE__)
    
    # get 20 most frequent words from each URL and print to console
    someDict = genDictTopWords(__PICKLE_FILE__, 20)
    pp = pprint.PrettyPrinter(indent=3)
    pp.pprint(someDict)

if __name__ == '__main__':
    main()    
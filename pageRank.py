import re
from os import listdir
from os.path import isfile, join


class WebPage():
    def __init__(self,filename):
        self.filename = filename
        self.loadPage(filename)
        self.outlinkCount = 0
        self.inLinks = []
        self.outLinks = []        
        self.parseLinks()
        self.pageRankScore = 1


    def loadPage(self,filename):
        try:
            f = open(filename,"r")
            self.source = f.read()
        except:
            self.source = None

    def addInLink(self, otherpage):
        self.inLinks.append(otherpage)

    def wipeInLinks(self):
        self.inLinks = []
        
    def parseLinks(self):
        anchors = re.finditer("<a href=\".*\"",self.source)
        for anchor in anchors:
            thislink = anchor.group(0)
            url = re.search("\".*\"", thislink).group(0)
            self.outLinks.append(url[1:-1])
            self.outlinkCount += 1
            
def getHTMLFileList():
    files = [f for f in listdir() if isfile(f) if f[-4:]=="html" or f[-3:]=="htm"]
    return files

def makeWebPages():
    files = getHTMLFileList()
    pages = [WebPage(file) for file in files]
    return pages


def makePageLookupTable(pages):
    # make a lookup table of these pages based on filename
    pagesDict = {}
    for page in pages:
        pagesDict[page.filename] = page  # make a pointer to this page
    return pagesDict


def printPageRanks(pages):
    print("Page Ranks are now")
    for page in pages:
        print(page.filename , " : ", page.pageRankScore)

        
def generatePageRanks(pages):
    pagesDict = makePageLookupTable(pages)
    # refresh all the inlinks
    for page in pages:
        page.wipeInLinks()
    for page in pages:
        for outlink in page.outLinks:
            pagesDict[outlink].addInLink(page)

    dampener = 0.85            
    for iterations in range(5):
        #generate all the new pageranks
        for thisPage in pages:
            thisPage.pageRankScore = (1-dampener)
            for thisLinkedPage in thisPage.inLinks:
                #print(thisLinkedPage.filename, thisLinkedPage.pageRankScore, thisLinkedPage.outlinkCount)
                thisPage.pageRankScore += dampener * (thisLinkedPage.pageRankScore / thisLinkedPage.outlinkCount)
	
        print("New Rankings have been generated")
        printPageRanks(pages)


pages = makeWebPages()
printPageRanks(pages)
generatePageRanks(pages)
printPageRanks(pages)

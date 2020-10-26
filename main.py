import operator
import time

intSize = 2  # In bytes


def getText():
    f = open("short.txt", "r")

    text = f.read()
    n = len(text)
    print("File read successfull.\nWords Read:", n)
    return text, n


def getMemorySaved(texts): # Heuristic Function (tells which phrase will lead to how much size reduction)
    count = {}

    for text in texts:
        windowSize = intSize
        while(windowSize < 15):
            for i in range(len(text)-windowSize+1):
                phrase = text[i:i+windowSize]
                if len(phrase) > intSize:
                    try:
                        count[phrase] += 1
                    except KeyError:
                        count[phrase] = 1
            windowSize += 1

    memSaved = {}

    for phrase in count:
        if count[phrase] * (len(phrase) - intSize) - len(phrase) > 0:
            memSaved[phrase] = count[phrase] * \
                (len(phrase) - intSize) - len(phrase)

    return memSaved


def greedyCompress(texts, n):
    memSaved = getMemorySaved(texts)
    mx = 0
    bestPhrase = ""

    for phrase in memSaved:
        if(memSaved[phrase] > mx):
            mx = memSaved[phrase]
            bestPhrase = phrase

    if mx > 0:
        newTexts = []

        for text in texts:
            newTexts += text.split(bestPhrase)

        saved, phrases = greedyCompress(newTexts, n+1)

        return mx + saved, phrases + [bestPhrase]

    return 0, []


def gdfsaCompress(texts, b):
    memSaved = getMemorySaved(texts)

    if b == 1:
        return greedyCompress(texts, 0) # If branching factor is 1, GDFS becomes greedy

    branchingFactor = min(b, len(memSaved))

    topMemorySavers = dict(sorted(memSaved.items(
    ), key=operator.itemgetter(1), reverse=True)[:branchingFactor])

    mostSaved = 0
    bestPhrases = []

    for phrase in topMemorySavers:
        newTexts = []
        for text in texts:
            newTexts += text.split(phrase)

        saved, phrases = gdfsaCompress(newTexts, b-1)

        if mostSaved < topMemorySavers[phrase] + saved:
            mostSaved = topMemorySavers[phrase] + saved
            bestPhrases = phrases + [phrase]

    return mostSaved, bestPhrases


if __name__ == "__main__":
    text, n = getText()

    start = time.time()
    bytesSaved, phrasesCompressed = greedyCompress([text], 0)
    end = time.time()

    print("Compression using Greedy:", int(10000*bytesSaved/n)/100, "%")
    print("Total Phrases Compressed", len(phrasesCompressed))
    print("Time taken by Greedy:", end-start, "Seconds")
    print(phrasesCompressed)

    start = time.time()
    bytesSaved, phrasesCompressed = gdfsaCompress([text], 4)
    end = time.time()

    print("Compression using GDFSA:", int(10000*bytesSaved/n)/100, "%")
    print("Total Phrases Compressed", len(phrasesCompressed))
    print("Time taken by GDFSA:", end-start, "Seconds")
    print(phrasesCompressed)

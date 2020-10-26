import operator

intSize = 2  # In bytes


def getText():
    f = open("file.txt", "r")
    text = f.read()
    n = len(text)
    print("File read successfull.\nWords Read:", n)
    return text, n


def getMemorySaved(texts):
    count = {}

    for text in texts:
        windowSize = intSize
        while(windowSize < 20):
            for i in range(len(text)-windowSize):
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


def greedyCompress(texts):
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

        saved, phrases = greedyCompress(newTexts)

        return mx + saved, phrases + [bestPhrase]

    return 0, []


def gdfsCompress(texts, b):
    memSaved = getMemorySaved(texts)

    if b == 1:
        return greedyCompress(texts)

    branchingFactor = min(b, len(memSaved))

    topMemorySavers = dict(sorted(memSaved.items(
    ), key=operator.itemgetter(1), reverse=True)[:branchingFactor])

    mostSaved = 0
    bestPhrases = []

    for phrase in topMemorySavers:
        newTexts = []
        for text in texts:
            newTexts += text.split(phrase)

        saved, phrases = gdfsCompress(newTexts, b-1)

        if mostSaved < topMemorySavers[phrase] + saved:
            mostSaved = topMemorySavers[phrase] + saved
            bestPhrases = phrases + [phrase]

    return mostSaved, bestPhrases


if __name__ == "__main__":
    text, n = getText()

    bytesSaved, phrasesCompressed = greedyCompress([text])

    print("Compression using Greedy:", int(
        10000*bytesSaved/n)/100, "%")
    print("Total Phrases Compressed", len(phrasesCompressed))

    bytesSaved, phrasesCompressed = gdfsCompress([text], 4)

    print("Compression using Greedy-DFS:", int(10000*bytesSaved/n)/100, "%")
    print("Total Phrases Compressed", len(phrasesCompressed))

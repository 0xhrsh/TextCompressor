intSize = 2  # In bytes


def getText():
    f = open("file.txt", "r")
    text = f.read()
    n = len(text)

    return text, n


def getMemorySaved(texts):
    count = {}

    for text in texts:
        windowSize = intSize
        while(windowSize < len(text)):
            for i in range(len(text)-windowSize):
                phase = text[i:i+windowSize]
                if len(phase) > intSize:
                    try:
                        count[phase] += 1
                    except KeyError:
                        count[phase] = 1
            windowSize += 1

    memSaved = {}

    for phase in count:
        memSaved[phase] = count[phase] * (len(phase) - intSize) - len(phase)

    return memSaved


def greedyCompress(texts):
    memSaved = getMemorySaved(texts)
    mx = 0

    for phase in memSaved:
        if(memSaved[phase] > mx):
            mx = memSaved[phase]
            bestPhase = phase

    if mx > 0:
        print(bestPhase, mx)
        newTexts = []

        for text in texts:
            newTexts += text.split(bestPhase)

        return mx + greedyCompress(newTexts)

    return 0


if __name__ == "__main__":
    text, n = getText()
    memSaved = getMemorySaved(text)

    print(greedyCompress([text]))

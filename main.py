intSize = 2  # In bytes


def getFile():
    f = open("file.txt", "r")
    s = f.read()
    n = len(s)

    return s, n


def createHashMap(s):
    store = {}
    windowSize = intSize

    while(windowSize < len(s)):
        for i in range(len(s)-windowSize):
            phase = s[i:i+windowSize]
            if len(phase) > intSize:
                try:
                    store[phase] += 1
                except KeyError:
                    store[phase] = 1
        windowSize += 1

    memoryCompressed = {}

    for phase in store:
        memoryCompressed[phase] = store[phase] * \
            (len(phase) - intSize) - len(phase)

    return memoryCompressed


if __name__ == "__main__":
    s, n = getFile()
    store = createHashMap(s)

    maxi = 0

    for x in store:
        if(store[x] > maxi):
            maxi = store[x]
            s = x

    print(s, maxi)

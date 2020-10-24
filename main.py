def getFile():
    f = open("file.txt", "r")
    s = f.read()
    n = len(s)

    return s, n


def createHashMap(s):
    store = {}
    for word in s.split():
        try:
            store[word] += 1
        except KeyError:
            store[word] = 1
    return store


def compress(store, n):
    newLength = n

    for word in store:
        if len(word)*store[word] > 4:
            newLength -= len(word)*store[word] - 4

    print("Original Size of the file:", n, "bytes")
    print("Compressed Size of the file:", newLength, "bytes")
    print()
    print("% Compression:", int(10000*(n-newLength)/n)/100, "%")


if __name__ == "__main__":
    s, n = getFile()
    store = createHashMap(s)

    compress(store, n)

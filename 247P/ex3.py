import os
import zipfile
from fileProcessing import FP
import collections

invertedIndex = collections.defaultdict()


def invertingIndex(txt, docName):
    for i, term in enumerate(txt):
        # if docName == '11100' and i == 17287:
        #     print(txt[i-1], term, txt[i+1])
        if term not in invertedIndex:
            invertedIndex[term] = {}
        if docName not in invertedIndex[term]:
            invertedIndex[term][docName] = []
        invertedIndex[term][docName].append(i)


def main():
    input_dir = '../SWE247P project/input-transform'
    output_dir = '../SWE247P project/inv-index/output.txt'

    def readAll(input_path):
        if os.path.isdir(input_path):
            for f in os.listdir(input_path):
                if f[-4:] == '.txt':
                    txt = fp.readTXT(input_path+'/'+f)
                    invertingIndex(txt.split(' '), f[:-4])
                else:
                    readAll(input_path + '/' + f)

    fp = FP()
    readAll(input_dir)
    res = ""
    for term in sorted(invertedIndex):
        # print(term)
        temp = term + ' '
        for doc in sorted(invertedIndex[term]):
            temp += doc + ':' + str(len(invertedIndex[term][doc])) + ':'
            for pos in invertedIndex[term][doc]:
                temp += str(pos) + ','
            temp = temp[:-1]+';'

        res += temp[:-1] + '\n'

    fp.writeTXT(res, output_dir)


if __name__ == "__main__":
    main()

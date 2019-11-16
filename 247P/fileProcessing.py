import os
import zipfile
import collections


class FP:
    def __init__(self):
        return

    def readZip(self, zip_src):
        if zipfile.is_zipfile(zip_src):
            files = zipfile.ZipFile(zip_src, 'r')

            for f in files.namelist():
                return files.read(f).decode('utf8', errors='ignore')

    # def readAll(self, input_path, output_path):
    #     print(input_path, output_path, os.path.isdir(input_path))
    #     if os.path.isdir(input_path):
    #         if not os.path.exists(output_path):
    #             os.makedirs(output_path)
    #         for f in os.listdir(input_path):
    #             if zipfile.is_zipfile(input_path + '/' + f):
    #                 yield readZip(input_path + '/' + f, output_path + '/' + f)
    #             else:
    #                 print(f)
    #                 yield self.readAll(input_path + '/' + f, output_path + '/' + f)

    def writeTXT(self, content, dir):
        with open(dir, "w") as f:
            f.write(content)

    def readTXT(self, dir):
        with open(dir, "r") as f:
            return f.read()

    def txt2Dict(self, dir):
        res = collections.defaultdict()
        with open(dir) as fp:
            line = fp.readline()[:-2]
            while line:
                term, index = line.split(' ')
                res[term] = {}
                docs = index.split(';')
                for doc in docs:
                    docName, freq, pos = doc.split(':')
                    res[term][docName] = list(map(int, pos.split(',')))
                # print(res[term])
                line = fp.readline()[:-2]
        return res

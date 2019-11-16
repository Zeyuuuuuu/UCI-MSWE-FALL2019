from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
from fileProcessing import FP
import os
import zipfile
import re


class ProcessingText:

    def processing(self, inputText):
        my_stop_words = {'u.s.'}
        stop_words = set(stopwords.words('english')) | my_stop_words
        # {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 
        # 'there', 'about', 'once', 'during', 'out', 'very', 'having', 
        # 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 
        # 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 
        # 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 
        # 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 
        # 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 
        # 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 
        # 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 
        # 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 
        # 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not',
        #  'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 
        # 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 
        # 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}
        # tokenization
        word_tokens = word_tokenize(
            re.sub('[%s]' % re.escape(string.punctuation), ' ', inputText))
        # print(word_tokens)
        # Porter stemming and word-stopping
        ps = PorterStemmer()
        filtered_sentence = []
        for w in word_tokens:
            if w.lower() not in stop_words:
                # print(w)
                filtered_sentence.append(ps.stem(w))
        return filtered_sentence


def test():
    test = "i on"
    test2 = "d to"
    # 11100.txt
    test1ori = "responds to"
    # 10861.txt
    test2ori = "carried on,"
    for c in test1ori:
        print(c, c.encode('utf8'))
    for c in test2ori:
        print(c, c.encode('utf8'))
    pt = ProcessingText()
    inputText = "Document will ''describe ON on On oN marketing strategies carried out by U.S. companies'' for their agricultural chemicals, '' __ report predictions for market share of such chemicals, or report market statistics for agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, stimulate demand, price cut, volume of sales."
    print(pt.processing(inputText))
    # test = ' '.join(['Document', 'a', 'A', '\'s', 'I', 'BY'])
    # print(test)
    # ps = PorterStemmer()
    # stop_words = set(stopwords.words('english')) | {'a', '\'s', 'i', 'by'}
    # for t in word_tokenize(test):
    #     print(t, ps.stem(t), ps.stem(t) in stop_words)


def main():
    input_dir = '../SWE247P project/input-files'
    output_dir = '../SWE247P project/input-transform'
    pt = ProcessingText()

    def readAll(input_path, output_path):
        if os.path.isdir(input_path):
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            for f in os.listdir(input_path):
                if zipfile.is_zipfile(input_path + '/' + f):
                    content = fp.readZip(input_path + '/' + f)
                    fp.writeTXT(' '.join(pt.processing(content)),
                                output_path+'/'+f[:-4]+'.txt')
                else:
                    readAll(input_path + '/' + f, output_path + '/' + f)

    fp = FP()
    readAll(input_dir, output_dir)


if __name__ == "__main__":

    main()
    # test()

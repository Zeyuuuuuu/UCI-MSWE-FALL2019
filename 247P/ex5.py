from fileProcessing import FP
from ex2 import ProcessingText
import heapq
import math


class SearchEngine:
    def __init__(self, indexTxt):
        self.fp = FP()
        self.invertedIndex = self.fp.txt2Dict(indexTxt)
        self.absTermWeightInDoc = {}
        self.pt = ProcessingText()
        self.score = {}
        self.N = 1001
        self.inverseDocumentFrequencyWeights = {}


# Score(d, q) = Score_counts(d, q) + Score_positions(d, q), where
# Score_counts(d, q) = SUM(count(t, d)) for all terms t in q and
# Score_positions(d, q) = SUM(1 / Shortest(t_i, t_i+1, d)) for 0 <= i < terms t in q

    def query(self, q):
        queryTerm = self.pt.processing(q)
        queryTermSet = set(queryTerm)
        if tuple(queryTerm) not in self.score:
            # score[0] cosScore
            # score[1] posScore
            score = [{}, {}]
            normTermWeightsInQuery = {}
            normTermWeightsInDoc = {}
            termWeightsSquareSumInDoc = {}
            
            # nomalized cos
            # print(queryTerm,queryTermSet)
            # term wieght in documents
            for term in queryTermSet:
                if term in self.invertedIndex:
                    # inverse document frequency weight
                    if term not in self.inverseDocumentFrequencyWeights:
                        self.inverseDocumentFrequencyWeights[term] = math.log(self.N / len(self.invertedIndex[term]))

                    for docName in self.invertedIndex[term]:
                        if docName not in self.absTermWeightInDoc:
                            self.absTermWeightInDoc[docName] = {}
                        if term not in self.absTermWeightInDoc[docName]:
                            self.absTermWeightInDoc[docName][term] = (math.log(len(self.invertedIndex[term][docName])) +1) * \
                                self.inverseDocumentFrequencyWeights[term]
                        if docName not in termWeightsSquareSumInDoc:
                            termWeightsSquareSumInDoc[docName] = 0
                        termWeightsSquareSumInDoc[docName] += self.absTermWeightInDoc[docName][term] * self.absTermWeightInDoc[docName][term]

            # nomalize
            for term in queryTermSet:
                if term in self.invertedIndex:
                    for docName in self.invertedIndex[term]:
                        if docName not in normTermWeightsInDoc:
                            normTermWeightsInDoc[docName] = {}
                        # print(term,docName)
                        normTermWeightsInDoc[docName][term] = self.absTermWeightInDoc[docName][term] / math.sqrt(termWeightsSquareSumInDoc[docName])

            # term weight in query
            termWeightsSquareSumQ = 0
            for term in queryTermSet:
                if term in self.invertedIndex:
                    normTermWeightsInQuery[term] = (math.log(queryTerm.count(term)) +1) * self.inverseDocumentFrequencyWeights[term]
                    termWeightsSquareSumQ += normTermWeightsInQuery[term] * normTermWeightsInQuery[term]
            # nomalize
            for term in queryTermSet:
                if term in self.invertedIndex:
                    normTermWeightsInQuery[term] /= math.sqrt(termWeightsSquareSumQ)

            # square len sum of query
            squareLenSumQ = 0
            squareLenSumDocs = {}
            for term in queryTermSet:
                if term in self.invertedIndex:
                    squareLenSumQ += normTermWeightsInQuery[term] * normTermWeightsInQuery[term]
                    for doc in self.invertedIndex[term]:
                        if doc not in squareLenSumDocs:
                            squareLenSumDocs[doc] = 0
                        squareLenSumDocs[doc] += normTermWeightsInDoc[doc][term] * normTermWeightsInDoc[doc][term]
            lenSunQ = math.sqrt(squareLenSumQ)

            # cos score
            for doc in normTermWeightsInDoc:
                for term in queryTermSet:
                    if term in normTermWeightsInDoc[doc]:
                        if doc not in score[0]:
                            score[0][doc] = 0
                        score[0][doc] += normTermWeightsInDoc[doc][term] * normTermWeightsInQuery[term]

            # nomalized cos score
            for doc in score[0]:
                score[0][doc] /= lenSunQ * math.sqrt(squareLenSumDocs[doc])

            maxDoc = ['']*10
            # position score
            if len(queryTerm) > 1:
                for i, term in enumerate(queryTerm):
                    if term in self.invertedIndex:
                        for docName in self.invertedIndex[term]:
                            if docName not in score[1]:
                                score[1][docName] = 0
                            if i < len(queryTerm) - 1 and docName in self.invertedIndex[queryTerm[i + 1]]:
                                posi = self.invertedIndex[term][docName]
                                posj = self.invertedIndex[queryTerm[i + 1]][docName]
                                distance = float('inf')
                                for pi in posi:
                                    for pj in posj:
                                        if abs(pi - pj) < distance:
                                            distance = abs(pi - pj)
                                if distance < float('inf'):
                                    score[1][docName] += 1 / distance

                maxDoc = heapq.nlargest(10,score[0],key=lambda x: score[0][x] + score[1][x] /(len(queryTerm) - 1))
                self.score[tuple(queryTerm)] = [(d, score[0][d], score[1][d]/(len(queryTerm) - 1)) for d in maxDoc]
            else:
                maxDoc = heapq.nlargest(10,score[0],key=lambda x: score[0][x])
                self.score[tuple(queryTerm)] = [(d, score[0][d], 0) for d in maxDoc]
            
        return self.score[tuple(queryTerm)]


def main():
    se = SearchEngine('../SWE247P project/inv-index/output.txt')
    while True:
        q = input("Q> ")
        # print(q)
        ans = se.query(q)
        # print(ans)
        if not ans:
            print('No documents found')
        else:
            print('Top 10 results:')
            count = 1
            for f, cos,pos in ans:
                print(str(count) + '. file: ' + f + ' score: ' + str(cos+pos)+' cos score: '+str(cos) + ' pos score: ' + str(pos))
                count += 1


if __name__ == "__main__":
    main()

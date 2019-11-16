from fileProcessing import FP
from ex2 import ProcessingText
import heapq


class SearchEngine:
    def __init__(self, indexTxt):
        self.fp = FP()
        self.invertedIndex = self.fp.txt2Dict(indexTxt)

        self.pt = ProcessingText()
        self.score = {}

# Score(d, q) = Score_counts(d, q) + Score_positions(d, q), where
# Score_counts(d, q) = SUM(count(t, d)) for all terms t in q and
# Score_positions(d, q) = SUM(1 / Shortest(t_i, t_i+1, d)) for 0 <= i < terms t in q

    def query(self, q):
        queryTerm = self.pt.processing(q)
        if tuple(queryTerm) not in self.score:
            scoreOfQuery = {}

            # score count
            for term in set(queryTerm):
                if term in self.invertedIndex:
                    for docName in self.invertedIndex[term]:
                        if docName not in scoreOfQuery:
                            scoreOfQuery[docName] = 0
                        scoreOfQuery[docName] += len(
                            self.invertedIndex[term][docName])

            # score position
            for i, term in enumerate(queryTerm):
                if term in self.invertedIndex:
                    for docName in self.invertedIndex[term]:
                        if i < len(queryTerm)-1 and docName in self.invertedIndex[queryTerm[i+1]]:
                            posi = self.invertedIndex[term][docName]
                            posj = self.invertedIndex[queryTerm[i+1]][docName]
                            distance = float('inf')
                            for pi in posi:
                                for pj in posj:
                                    if abs(pi - pj) < distance:
                                        distance = abs(pi-pj)
                            if distance < float('inf'):
                                scoreOfQuery[docName] += 1 / distance

            maxDoc = heapq.nlargest(
                10, scoreOfQuery, key=lambda x: scoreOfQuery[x])
            # print(scoreOfQuery, maxDoc)
            self.score[tuple(queryTerm)] = [(d, scoreOfQuery[d])
                                            for d in maxDoc]
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
            for f, s in ans:
                print(str(count) + '. file: ' + f + ' score: ' + str(s))
                count += 1


if __name__ == "__main__":
    main()

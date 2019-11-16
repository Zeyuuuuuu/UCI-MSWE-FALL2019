import re, sys, collections,threadpool


class TermFrequency:

    def main(self):
        stopwords = set(open('stop_words').read().split(','))

        def countFile(fileName):
            words = re.findall('\w{3,}', open(fileName).read().lower())
            self.counts += collections.Counter(w for w in words if w not in stopwords)
            
        self.counts = collections.Counter()
        list_of_args = ['anonymit.txt','cDc-0200.txt','crossbow.txt','gems.txt']
        pool = threadpool.ThreadPool(10)   # define the size of the pool
        requests = threadpool.makeRequests(countFile, list_of_args) 
        [pool.putRequest(req) for req in requests]  # all the reqs are thrown to the pool 
        pool.wait()  # quit after all the threads stop
        for (w, c) in self.counts.most_common(25):
            print(w, '-', c)



if __name__ == "__main__":
    tf = TermFrequency()
    tf.main()
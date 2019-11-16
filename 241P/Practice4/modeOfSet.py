import collections
def modeOfSet(arr):
    count = collections.Counter(arr)
    return max(count,key = lambda x:count[x])


print(modeOfSet([1,23,1,3,2,5,4,1,2,1,5,5]))
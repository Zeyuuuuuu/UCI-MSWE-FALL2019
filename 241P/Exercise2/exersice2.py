import string,re,time,xlwt,random
from xlwt import *
import sys
 
sys.setrecursionlimit(1000000)
class InsertionSort:
	# @insertionSort, TLE, On2, O1, visited every nodes, move the bigger one on the left to the right, insert into the right place
    def sort(self,nums): 
        for i in range(1, len(nums)): 
            key = nums[i]
            j = i-1
            while j >= 0 and key < nums[j]: 
                    nums[j + 1] = nums[j] 
                    j -= 1
            nums[j + 1] = key
        return nums

class SelectionSort:
	# @selectionSort, TLE, On2, O1, find the min num from i to the end
    def sort(self,nums):
        for i in range(len(nums)):
            min_index = nums[i:].index(min(nums[i:]))
            nums[i + min_index],nums[i] = nums[i],nums[i+min_index]
        return nums

class HeapSort:
    # @heapSort Onlogn Ologn
    def sort(self, nums):
        def heapify(nums, n, i): 
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            
            if l < n and nums[i] < nums[l]: 
                largest = l 

            if r < n and nums[largest] < nums[r]: 
                largest = r 

            if largest != i: 
                nums[i], nums[largest] = nums[largest], nums[i]
                
                heapify(nums, n, largest)
                
        n = len(nums) 

        for i in range(n, -1, -1): 
            heapify(nums, n, i) 

        for i in range(n-1, 0, -1): 
            nums[i], nums[0] = nums[0], nums[i]
            heapify(nums, i, 0) 
        return nums

class MergeSort:
    # @mergeSort  Onlogn On
    # rec, two sorted parts, two pointers scan,add the smallest to the answer list
    def sort(self, nums): 
        if len(nums) > 1: 
            mid = len(nums)//2
            L = nums[:mid] 
            R = nums[mid:] 

            self.sort(L)
            self.sort(R)

            i = j = k = 0

            while i < len(L) and j < len(R): 
                if L[i] < R[j]: 
                    nums[k] = L[i] 
                    i+=1
                else: 
                    nums[k] = R[j] 
                    j+=1
                k+=1
 
            while i < len(L): 
                nums[k] = L[i] 
                i+=1
                k+=1

            while j < len(R): 
                nums[k] = R[j] 
                j+=1
                k+=1
   
        return nums

class QuickSort:
	# @quickSort Onlogn Ologn (Rec) Find pivot, make everything left smaller, everything right bigger
    # one pointer
    def __init__(self, *args, **kwargs):
        self.count = 0
    def partition1(self,nums,low,high):
            i = low
            index = random.randint(low,high)
            nums[index],nums[high] = nums[high],nums[index]
            pivot = nums[high]
            for j in range(low , high):
                if nums[j] < pivot: 
                    nums[i], nums[j] = nums[j], nums[i] 
                    i += 1 
            nums[i], nums[high] = nums[high], nums[i] 
            return i
    def partition(self,nums,low,high):
        i, j = low, high 
        pivot = nums[i]
        while i < j:
            while i < j and pivot <= nums[j]:
                j -= 1
            nums[i] = nums[j]
            while i < j and pivot >= nums[i]:
                i += 1
            nums[j] = nums[i]
        nums[i] = pivot
        return i
    def quicksort(self,nums,low, high,count=0):
        self.count = max(self.count,count)
        if low < high:
            pi = self.partition(nums,low, high) 
            # print(nums)
            self.quicksort(nums,low, pi-1,count+1)
            self.quicksort(nums,pi+1, high,count+1)
        else:
            return
    
    def sort(self,nums):
        num2 = nums
        self.quicksort(nums,0,len(nums)-1)
        print(self.count)
        self.count = 0
        self.sort2(num2)
        print(self.count)
        return nums

    def sort2(self, nums,count=0):
        self.count = max(self.count,count)
        if len(nums) <= 1:
            return nums
        pivot = random.choice(nums)
        lt = [v for v in nums if v < pivot]
        eq = [v for v in nums if v == pivot]
        gt = [v for v in nums if v > pivot]
        return self.sort2(lt,count+1) + eq + self.sort2(gt,count+1)

     
def test():
    # insertionSort = InsertionSort()
    # print(insertionSort.sort([1,2,23,12,4,12,5,6,6,23,5,2]))
    # selectionSort = SelectionSort()
    # print(selectionSort.sort([1,2,23,12,4,12,5,6,6,23,5,2]))
    # mergeSort = MergeSort()
    # print(mergeSort.sort([1,2,23,12,4,12,5,6,6,23,5,2]))
    # heapSort = HeapSort()
    # print(heapSort.sort([1,2,23,12,4,12,5,6,6,23,5,2]))
    quickSort = QuickSort()
    quickSort.sort([2]*10000+[x for x in range(100,-1,-1)])



def main():
    fread = open('pride-and-prejudice.txt')
    linesR = fread.readlines()
    dictionary = []

    for line in linesR:
        s = re.sub('[%s]' % re.escape(string.punctuation), ' ', line)
        listR = s.split()
        for word in listR:
            dictionary.append(word)
    sd = sorted(dictionary)

    file = Workbook(encoding = 'utf-8')
    table = file.add_sheet('Sort')

    data = [[0]*5 for _ in range(10)]
    i = 0
    # for i in range(10):
    insertSort = InsertionSort()
    d = [x for x in dictionary]
    print('0',d == sd,d == dictionary)
    t = time.monotonic_ns()
    nd = insertSort.sort(d)
    data[i][0] = time.monotonic_ns() - t
    print(sd == nd)

    selectionSort = SelectionSort()
    d = [x for x in dictionary]
    print('1',d == sd,d == dictionary)
    t = time.monotonic_ns()
    nd = selectionSort.sort(d)
    data[i][1] = time.monotonic_ns() - t
    print(sd == nd)
    
    heapSort = HeapSort()
    d = [x for x in dictionary]
    print('2',d == sd,d == dictionary)
    t = time.monotonic_ns()
    nd = heapSort.sort(d)
    data[i][2] = time.monotonic_ns() - t
    print(sd == nd)

    mergeSort = MergeSort()
    d = [x for x in dictionary]
    print('3',d == sd,d == dictionary)
    t = time.monotonic_ns()
    nd = mergeSort.sort(d)
    data[i][3] = time.monotonic_ns() - t
    print(sd == nd)

    quickSort = QuickSort()
    d = [x for x in dictionary]
    print('4',d == sd,d == dictionary)
    t = time.monotonic_ns()
    nd = quickSort.sort2(d)
    data[i][4] = time.monotonic_ns() - t
    print(sd == nd)
    print(data)
    # for i in range(10):
    #     for j in range(5):
    #         table.write(i,j,data[i][j])

    # # file.save('output.xlsx')
    # # d = [x for x in dictionary]
    # quickSort = QuickSort()
    # # print('4',d == sd,d == dictionary)
    # # nd = quickSort.sort2(d)
    # # print(sd == nd)

    # d = [x for x in dictionary]
    # print('4',d == sd,d == dictionary)
    # nd = quickSort.sort(d)
    # print(sd == nd)

if __name__ == "__main__":
    #main()
    test()


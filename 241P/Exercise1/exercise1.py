class ListNode:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class LinkedListSet:
    def __init__(self):
        self.size = 0
        self.head = ListNode(0)
        self.tail = ListNode(0)
        self.head.next = self.tail

    def __len__(self):
        return self.size

    def size(self):
        return self.size

    def __contains__(self, val):
        return self.contains(val)

    def contains(self, val):
        val = str(val)
        node = self.head
        while node.next != self.tail:
            node = node.next
            if node.val == val:
                return True
        return False

    def add(self, val):
        val = str(val)
        if self.contains(val):
            return False
        node = self.head
        while node.next != self.tail:
            node = node.next
        node.next = ListNode(val, self.tail)
        self.size += 1
        return True

    def __str__(self):
        res = '['
        node = self.head
        while node.next != self.tail:
            node = node.next
            res += node.val + ','
        return res[:-1] + ']'



class BinaryTreeSet:
    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def size(self):
        return self.size

    def __contains__(self, val):
        return self.contains(val)

    def contains(self, val):
        val = str(val)
        node = self.root
        while node:
            if node.val > val:
                node = node.left
            elif node.val < val:
                node = node.right
            else:
                return True
        return False

    def add(self, val):
        val = str(val)
        if not self.root:
            self.root = TreeNode(val)
            self.size += 1
            return True
        node = self.root
        while node:
            if node.val > val:
                if not node.left:
                    node.left = TreeNode(val)
                    self.size += 1
                    return True
                node = node.left
            elif node.val < val:
                if not node.right:
                    node.right = TreeNode(val)
                    self.size += 1
                    return True
                node = node.right
            else:
                return False

    def __str__(self):
        node = self.root
        res = '['
        while node:
            if node.left:
                pre = node.left
                while pre.right and pre.right != node:
                    pre = pre.right
                if pre.right:
                    pre.right = None
                    res += node.val + ','
                    node = node.right
                else:
                    pre.right = node
                    node = node.left
            else:
                res += node.val + ','
                node = node.right
        return res[:-1] + ']'


class HashTableSet:
    def __init__(self):
        self.numOfSlots = 10000
        self.cell = [None]*self.numOfSlots
        self.size = 0

    def __len__(self):
        return self.size

    def size(self):
        return self.size

    def __contains__(self, val):
        return self.contains(val)

    def contains(self, val):
        val = str(val)
        index = hash(val) % self.numOfSlots
        if not self.cell[index]:
            return False
        else:
            node = self.cell[index]
            while node:
                if node.val == val:
                    return True
                node = node.next
            return False

    def add(self, val):
        val = str(val)
        index = hash(val) % self.numOfSlots
        if not self.cell[index]:
            self.cell[index] = ListNode(val)
            self.size += 1
            return True
        else:
            node = self.cell[index]
            while node:
                if node.val == val:
                    return False
                if not node.next:
                    node.next = ListNode(val)
                    self.size += 1
                    return True
                node = node.next

    def __str__(self):
        res = '['
        for i in range(self.numOfSlots):
            node = self.cell[i]
            while node:
                res += node.val + ','
                node = node.next
        return res[:-1] + ']'
from xlwt import *
import string,re,time,xlwt

def experiment(dictionary,test,mySet):
    obj = time.gmtime(0)  
    epoch = time.asctime(obj) 
    addData,checkData = [],[]
    lenData = []
    count = 0
    for word in dictionary:
        if count % 10 == 0:
            lenData.append(len(mySet))
            s = time.monotonic_ns()
        mySet.add(word)
        if count % 10 == 0:
            e = time.monotonic_ns()
            addData.append(e-s)
        count += 1

    myCount = 0
    count = 0
    for t in test:
        count += 1
        s = time.monotonic_ns()
        check = mySet.contains(t)
        e = time.monotonic_ns()
        checkData.append(e-s)
        if not check:
            myCount += 1
    time4 = time.monotonic_ns()

    print(len(mySet),myCount)
    return(addData,checkData,lenData)

def main():
    fread = open('pride-and-prejudice.txt')
    fsearch = open('words-shuffled.txt')
    linesR,linesS = fread.readlines(),fsearch.readlines()
    set1,set2,set3 = LinkedListSet(),BinaryTreeSet(),HashTableSet()
    dictionary = []
    testWords = []

    for line in linesR:
        s = re.sub('[%s]' % re.escape(string.punctuation), ' ', line)
        listR = s.split()
        for word in listR:
            dictionary.append(word)
    
    for line in linesS:
        listS = line.split()
        testWords.append(listS[0])
    
    file = Workbook(encoding = 'utf-8')
    table1 = file.add_sheet('LinkedListSet')
    table2 = file.add_sheet('BinarySearchTreeSet')
    table3 = file.add_sheet('HashTableSet')
    data1 = [None]*21
    data2 = [None]*21
    data3 = [None]*21

    lendata = []

    for i in range(10):
        data1[i],data1[11+i],_ = experiment(dictionary,testWords,LinkedListSet())
        data2[i],data2[11+i],_ = experiment(dictionary,testWords,BinaryTreeSet())
        data3[i],data3[11+i],_ = experiment(dictionary,testWords,HashTableSet())
    _,_,lendata = experiment(dictionary,testWords,HashTableSet())
    for i,p in enumerate(data1):
        if p:
            for j,q in enumerate(p):
                if q:
                    table1.write(j+2,i+1,q)
    for i,p in enumerate(data2):
        if p:  
            for j,q in enumerate(p):
                if q:
                    table2.write(j+2,i+1,q)
    for i,p in enumerate(data3):
        if p:
            for j,q in enumerate(p):
                if q:
                    table3.write(j+2,i+1,q)
    for i,d in enumerate(lendata):
        table1.write(i+2,0,d)
        table2.write(i+2,0,d)
        table3.write(i+2,0,d)
    file.save('output.xlsx')
def test():
    nums = [1,2,3,4,1,2,31,23,2,1,24,12,3,'aaa','asdasda','asdasd','aaa']
    print('LinkedListSet Test')
    print('')
    set1 = LinkedListSet()
    for num in nums:
        print(num,set1.add((num)))
    print(len(set1))
    print(set1)
    print(set1.contains((1)))
    print(set1.contains((99)))
    print((31) in set1)
    print('')
    print('BinaryTreeSet Test')
    print('')
    set2 = BinaryTreeSet()
    for num in nums:
        print(num, set2.add(num))
    print(len(set2))
    print(set2)
    print(set2.contains(1))
    print(set2.contains(9))
    print(31 in set2)
    print('')
    print('HashTableSet Test')
    print('')
    set3 = HashTableSet()
    for num in nums:
        print(num, set3.add((num)))
    print(len(set3))
    print(set3)
    print(set3.contains(1))
    print(set3.contains(9))
    print(31 in set3)

if __name__ == "__main__":
    main()




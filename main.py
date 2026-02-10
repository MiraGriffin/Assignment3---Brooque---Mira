from typing import *
from dataclasses import dataclass
import unittest
import sys
sys.setrecursionlimit(10**6)

# Returns an array of, where at index, i, it is the number of 
# times the the character with ASCII code -- from 1 to 256 i is 
# featured in the text
def cnt_freq(text : str) -> List[int]:
    freq = [0] * 256
    for char in text:
        ascii = ord(char)
        freq[ascii] += 1
    return freq

# Data Definitions
@dataclass(frozen=True)
class HLeaf:
	count: int
	char: str

@dataclass(frozen=True)      
class HNode:
    count: int
    char: str
    left: HTree
    right: HTree

@dataclass(frozen = True)
class HTLNode:
    tree : HTree
    next : HTList

HTree : TypeAlias = Union [HNode, HLeaf]
HTList : TypeAlias = Union[HTree, HTLNode]

# Huffman Tree Functions
def tree_lt(tree_1: HTree, tree_2: HTree) -> bool:
       
       if tree_1.count < tree_2.count or (tree_1.count == tree_2.count and tree_1.char < tree_2.char):
		        return True

# Returns the HTree at index 'i' of 'ht_list', if 'i' is a valid
# index in 'ht_list'
def list_ref(ht_list : HTList, i : int) -> Optional[HTree]:
    match ht_list:
        case HLeaf() | HNode():
            if i == 0:
                return ht_list
            else:
                return None
        case HTLNode(tree, next):
            if i == 0:
                return tree
            else:
                return list_ref(next, i - 1)

# Returns an HTList of the each character's ASCII code and it's 
# frequency in 'text'
def base_tree_list(text : str) -> HTList:
    freq = cnt_freq(text)
    lst : HTList = HLeaf(freq[255], chr(255))
    for i in range(254, -1, -1):
        leaf = HLeaf(freq[i], chr(i))
        lst = HTLNode(leaf, lst)
    return lst

# Inserts an HTree into aa properly sorted HTList at the correct
# location so that it is still sorted correctly
def tree_list_insert(ht_list : HTList, htree : HTree) -> HTList:
    match ht_list:
        case HLeaf() | HNode():
            if tree_lt(htree, ht_list):
                return HTLNode(htree, ht_list)
            else:
                return HTLNode(ht_list, htree)
        case HTLNode(tree, next):
            if tree_lt(htree, tree):
                return HTLNode(htree, ht_list)
            else:
                return HTLNode(tree, tree_list_insert(next, htree))
            

class Tests(unittest.TestCase):
    text1 : str = "aaa"
    text2 : str = "ddddddddddddddddccccccccbbbbaaff"
    text3 : str = "ABCD"
    text4 : str = ""

    def test_cnt_freq(self):
        self.assertEqual(cnt_freq(self.text1)[95:99],
                         [0, 0, 3, 0])
        self.assertEqual(cnt_freq(self.text2)[96:104],
                        [0, 2, 4, 8, 16, 0, 2, 0] )
        self.assertEqual(cnt_freq(self.text3)[65:70],
                         [1, 1, 1, 1, 0])
        self.assertEqual(cnt_freq(self.text4), [0] * 256)


    leaf_a : HLeaf = HLeaf(5, 'a')
    leaf_b : HLeaf = HLeaf(7, 'b')
    leaf_c : HLeaf = HLeaf(10, 'c')

    tree_lst : HTList = HTLNode(leaf_a, HTLNode(leaf_b, leaf_c))

    def test_list_ref(self):
        self.assertEqual(list_ref(self.tree_lst, 0), self.leaf_a)
        self.assertEqual(list_ref(self.tree_lst, 1), self.leaf_b)
        self.assertEqual(list_ref(self.tree_lst, 2), self.leaf_c)
        self.assertEqual(list_ref(self.tree_lst, 3), None)
    

    def test_base_tree_list(self):
        self.assertEqual(list_ref(base_tree_list(self.text1), 97), HLeaf(3, 'a'))
        self.assertEqual(list_ref(base_tree_list(self.text2), 98), HLeaf(4, 'b'))
        self.assertEqual(list_ref(base_tree_list(self.text3), 65), HLeaf(1, 'A'))
        self.assertEqual(list_ref(base_tree_list(self.text4), 97), HLeaf(0, 'a'))

    def test_tree_list_insert(self):
        self.assertEqual()
        






if (__name__ == '__main__'):
    unittest.main()
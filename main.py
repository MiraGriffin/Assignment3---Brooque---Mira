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

# Returns the HTree at index 'i' of 'ht_list'
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


class Tests(unittest.TestCase):
    text1 : str = "aaa"
    text2 : str = "ddddddddddddddddccccccccbbbbaaff"
    text3 : str = "ABCD"
    text4 : str = ""
    htree1 :
    ht_list1 : HTList = HTLNode(a, HTLNode)

    def test_cnt_freq(self):
        self.assertEqual(cnt_freq(self.text1)[95:99],
                         [0, 0, 3, 0])
        self.assertEqual(cnt_freq(self.text2)[96:104],
                        [0, 2, 4, 8, 16, 0, 2, 0] )
        self.assertEqual(cnt_freq(self.text3)[65:70],
                         [1, 1, 1, 1, 0])
        self.assertEqual(cnt_freq(self.text4), [0] * 256)











if (__name__ == '__main__'):
    unittest.main()
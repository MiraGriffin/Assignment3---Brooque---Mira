from typing import *
from dataclasses import dataclass
import unittest
import sys
sys.setrecursionlimit(10**6)

# Functions
# Returns an array of, where at index, i, it is the number of 
# times the the character with ASCII code -- from 1 to 256 i is 
# featured in the text
def cnt_freq(text : str) -> List[int]:
    freq = [0] * 256
    for char in text:
        ascii = ord(char)
        freq[ascii] += 1
    return freq


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

HTree : TypeAlias = Union [None, HLeaf]
HTLTree: TypeAlias = Union[None, HNode]


def tree_lt(tree_1: HTree, tree_2: HTree) -> bool:
       
       if tree_1.count < tree_2.count or (tree_1.count == tree_2.count and tree_1.char < tree_2.char):
		        return True




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









if (__name__ == '__main__'):
    unittest.main()
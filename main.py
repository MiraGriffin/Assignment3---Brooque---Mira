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
HTree : TypeAlias = Union ["HNode", "HLeaf"]

@dataclass(frozen=True)
class HLeaf:
	count: int
	char: str

@dataclass(frozen=True)      
class HNode:
    count: int
    char: str
    left: "HTree"
    right: "HTree"

@dataclass(frozen = True)
class HTLNode:
    tree : "HTree"
    next : "HTList"


HTList : TypeAlias = Union[HTLNode, None]

# Huffman Tree Functions
def tree_lt(tree_1: HTree, tree_2: HTree) -> bool:
    return (tree_1.count < tree_2.count or 
            (tree_1.count == tree_2.count and tree_1.char < tree_2.char))


# Returns the length of 'ht_lst'
def list_len(ht_list: HTList) -> int:
    match ht_list:
        case None:
            return 0
        case HTLNode(_, next):
            return 1 + list_len(next)

# Returns the HTree at index 'i' of 'ht_list', if 'i' is a valid
# index in 'ht_list'
def list_ref(ht_list : HTList, i : int) -> Optional[HTree]:
    match ht_list:
        case None:
            raise IndexError("Index out of bounds")
        case HTLNode(tree, next):
            if i == 0:
                return tree
            else:
                return list_ref(next, i - 1)

# Returns an HTList of the each character's ASCII code and it's 
# frequency in 'text'
def base_tree_list(freq : List[int]) -> HTList:
     lst: HTList = HLeaf(freq[255], chr(255))
     for i in range(254, -1, -1):
         lst = HTLNode(HLeaf(freq[i], chr(i)), lst)
     return lst


# Inserts an HTree into aa properly sorted HTList at the correct
# location so that it is still sorted correctly
def tree_list_insert(ht_list : HTList, htree : HTree) -> HTList:
     match ht_list:
         case None:
                return HTLNode(htree, None)
         case HTLNode(tree, next):
            if tree_lt(htree, tree):
                return HTLNode(htree, ht_list)
            else:
                return HTLNode(tree, tree_list_insert(next, htree))
            
# Returns a new sorted version of 'ht_list'
def initial_tree_sort(ht_list : HTList) -> HTList:
    match ht_list:
        case None:
             return None
        case HTLNode(tree, next):
            sorted = initial_tree_sort(next)
            return tree_list_insert(sorted, tree)
            
# Returns an HTList where the first two nodes of 'ht_list'-- if it is of length two 
# or more-- are combined into an HNode
def coalesce_once(ht_list : HTList) -> HTList:
    match ht_list:
        case HTLNode(first, HTLNode(second, next)):
            if first.char < second.char:
                new_char = first.char
            else:
                new_char = second.char
            new_node = HNode(first.count + second.count, new_char, first, second)
            return tree_list_insert(next, new_node)
        case _:
            raise ValueError("List must contain two or more HTLNodes")

         
# Returns an HTList where it recursively combines the first two nodes 'ht_list' --
# of length 1 or more -- into an HTree until the list only contains one HTree
def coalesce_all(ht_list : HTList) -> HTree:
    match ht_list:
        case None:
            raise ValueError("List must contain two or more HTLNodes")
        case HTLNode(tree, None):
            return tree
        case _:
            return coalesce_all(coalesce_once(ht_list))

# Construct a Huffman tree from 's'.
def string_to_HTree(s : str) -> HTree:
    treelist = base_tree_list(cnt_freq(s))
    sorted_treelist = initial_tree_sort(treelist)
    return coalesce_all(sorted_treelist)  

# Creates an array from 'h_tree' where each value in the array has a string of 0's--
# that represents lefts-- and 1's -- that represents rights-- to show the characters
# ocation in the tree, and the index of the array corresponds to the characters ASCII code
def build_encoder_array(h_tree : HTree) -> list[str]:
    encoder = [''] * 256
    def helper(h_tree : HTree, path : str) -> None:
        match h_tree:
            case HLeaf(_, char):
                encoder[ord(char)] = path
            case HNode(_, char, left, right):
                helper(left, path + '0')
                helper(right, path + '1')
    helper(h_tree, '')
    return encoder

# Creates a string from of values from 'encoder' based on the chars in 's'
def encode_string_one(s : str, encoder : list[str]) -> str:
    result = []
    for char in s:
        result.append(encoder[ord(char)])
    return ''.join(result)

# Converts a 'bits' into a bytearray
def bits_to_bytes(bits : str) -> bytearray:
    n_bits = len(bits)
    padding = (8 - n_bits % 8) % 8
    bits_padded = bits + '0' * padding
    n_bytes = len(bits_padded) // 8
    b_array = bytearray(n_bytes)
    for i in range(n_bytes):
        byte_str = bits_padded[i * 8 : (i + 1) * 8]
        b_array[i] = int(byte_str, 2)
    return b_array

# Reads the input file using 'source', constructs and HTree, converts
# the tree into an encoder array, then converts text to a Huffman-encoded bytearray,
# and writes th array to the 'target'
def huffman_code_file(source : str, target : str) -> None:
    with open(source, 'r', encoding = 'utf-8') as file:
        text = file.read()
    if not text:
        with open(target, 'wb') as file:
            file.write(bytearray())
        return
    freq : List[int] = cnt_freq(text)
    base_list : HTList = base_tree_list(freq)
    sorted_list = initial_tree_sort(base_list)
    h_tree : HTree = coalesce_all(sorted_list)
    encoder : list[str] = build_encoder_array(h_tree)
    bits : str = encode_string_one(text, encoder)
    b_array : bytearray = bits_to_bytes(bits)
    with open(target, 'wb') as file:
        file.write(b_array)
    



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
    tree_a : HTree = HLeaf(5, 'a')
    leaf_b2 : HLeaf = HLeaf(5, 'a')
    leaf_b : HLeaf = HLeaf(7, 'b')
    tree_b : HTree = HLeaf(7, 'b')
    leaf_c : HLeaf = HLeaf(10, 'c')
    tree_c : HTree = HLeaf(10, 'c')
    leaf_d : HLeaf = HLeaf(11, 'd')
    tree_d2 : HTree = HLeaf(11, 'd')
    leaf_e : HLeaf = HLeaf(3, 'e')
    tree_e2 : HTree = HLeaf(3, 'e')
    tree_d : HTree = HLeaf(12, 'd')
    tree_e : HTree = HLeaf(4, 'e')

    tree_lst1 : HTList = HTLNode(leaf_a, HTLNode(leaf_b, None))
    tree_lst2 : HTList = HTLNode(leaf_a, HTLNode(leaf_b, HTLNode(leaf_d, None)))
    tree_lst3 : HTList = HTLNode(leaf_e, HTLNode(leaf_a, HTLNode(leaf_b, 
                                 HTLNode(leaf_c, None))))
    tree_lst4 : HTList = HTLNode(leaf_a, None)

    tree1 : HTree = HNode(22, 'a', leaf_c, HNode( 12, 'a', leaf_a, leaf_b))
    tree2 : HTree = HNode(12, 'a', leaf_a, leaf_b)
    tree3 : HTree = HNode(36, 'a', HNode(15, 'a', leaf_b, 
                                        HNode(8, 'a', leaf_e, leaf_a)),
                                            HNode(21, 'c', leaf_c, leaf_d))
    


    unsorted1 : HTList = HTLNode(leaf_b, HTLNode(leaf_c, HTLNode(leaf_a, None)))
    unsorted2 : HTList = HTLNode(leaf_d, HTLNode(leaf_a, HTLNode(leaf_e, None)))
    unsorted3 : HTList = HTLNode(leaf_b, HTLNode(leaf_e, HTLNode(leaf_c, None)))
    unsorted4 : HTList = HTLNode(leaf_d, None)

    def test_tree_lt(self):
        self.assertTrue(tree_lt(self.leaf_e, self.leaf_a))
        self.assertFalse(tree_lt(self.leaf_c, self.leaf_b))
        self.assertFalse(tree_lt(self.leaf_a, self.leaf_b2))
        self.assertFalse(tree_lt(self.leaf_b, self.leaf_b))

    def test_list_len(self):
        self.assertEqual(list_len(self.tree_lst1), 2)
        self.assertEqual(list_len(self.tree_lst2), 3)
        self.assertEqual(list_len(self.tree_lst3), 4)
        self.assertEqual(list_len(self.tree_lst4), 1)

    def test_base_tree_list(self):
       self.assertEqual(list_ref(base_tree_list(cnt_freq(self.text1)), 97), HLeaf(3, 'a'))
       self.assertEqual(list_ref(base_tree_list(cnt_freq(self.text2)), 98), HLeaf(4, 'b'))
       self.assertEqual(list_ref(base_tree_list(cnt_freq(self.text3)), 65), HLeaf(1, 'A'))
       self.assertEqual(list_ref(base_tree_list(cnt_freq(self.text4)), 97), HLeaf(0, 'a'))

    def test_tree_list_insert(self):
        self.assertEqual(tree_list_insert(self.tree_lst1, self.leaf_c),
                         HTLNode(self.leaf_a, 
                                 HTLNode(self.leaf_b, 
                                         HTLNode(self.leaf_c, None))))
        self.assertEqual(tree_list_insert(self.tree_lst2, self.leaf_e),
                         HTLNode(self.leaf_e, 
                                 HTLNode(self.leaf_a,
                                          HTLNode(self.leaf_b,
                                                   HTLNode(self.leaf_d, None)))))
        self.assertEqual(tree_list_insert(self.tree_lst3, self.leaf_d),
                         HTLNode(self.leaf_e, 
                                 HTLNode(self.leaf_a, 
                                         HTLNode(self.leaf_b, 
                                                 HTLNode(self.leaf_c, 
                                                         HTLNode(self.leaf_d, None))))))
        
    def test_initial_tree_sort(self):
        self.assertEqual(initial_tree_sort(self.unsorted1),
                             HTLNode(self.leaf_a, 
                                    HTLNode(self.leaf_b, 
                                         HTLNode(self.leaf_c, None))))
        self.assertEqual(initial_tree_sort(self.unsorted2),
                             HTLNode(self.leaf_e, 
                                    HTLNode(self.leaf_a, 
                                         HTLNode(self.leaf_d, None))))
        self.assertEqual(initial_tree_sort(self.unsorted3),
                             HTLNode(self.leaf_e, 
                                    HTLNode(self.leaf_b, 
                                         HTLNode(self.leaf_c, None))))
        self.assertEqual(initial_tree_sort(self.unsorted4),
                             HTLNode(self.leaf_d, None))
        
    def test_coalesce_once(self):
        self.assertEqual(coalesce_once(self.tree_lst1), HTLNode(HNode(12,'a', self.leaf_a, self.leaf_b), None))
        self.assertEqual(coalesce_once(self.tree_lst2), HTLNode(self.leaf_d, 
                                                                HTLNode(
                                                                    HNode(12,'a', self.leaf_a, self.leaf_b), None)))
        self.assertEqual(coalesce_once(self.tree_lst3), HTLNode(self.leaf_b, 
                                                                HTLNode(
                                                                    HNode(8,'a', self.leaf_e, self.leaf_a),
                                                                      HTLNode(self.leaf_c, None))))
        self.assertRaises(ValueError, coalesce_once, self.tree_lst4)

    def test_coalesce_all(self):
        self.assertEqual(coalesce_all(self.tree_lst1), HNode(12,'a', HLeaf(5,'a'), HLeaf(7,'b')))
        self.assertEqual(coalesce_all(self.tree_lst2), HNode(23,'a', HLeaf(11,'d'), HNode(12,'a',
                                                                                          HLeaf(5,'a'),
                                                                                          HLeaf(7,'b'))))
        self.assertEqual(coalesce_all(self.tree_lst3), HNode(25,'a', HLeaf(10,'c'), 
                                                              HNode(15,'a', HLeaf(7,'b'),
                                                                    HNode(8,'a', HLeaf(3,'e'), HLeaf(5,'a')))))
        self.assertEqual(coalesce_all(self.tree_lst4), HLeaf(5,'a'))

    def test_build_encoder_array(self):
       self.assertEqual(build_encoder_array(self.tree1)[97:100],['10','11','0'])
       self.assertEqual(build_encoder_array(self.tree2)[97:99],['0','1'])
       self.assertEqual(build_encoder_array(self.tree3)[97:102],['011','00','10','11','010'])

    def test_encode_string_one(self):
       self.assertEqual(encode_string_one('ab', build_encoder_array(self.tree2)), '01')
       self.assertEqual(encode_string_one('abc', build_encoder_array(self.tree1)), '10110')
       self.assertEqual(encode_string_one('abcde', build_encoder_array(self.tree3)), '011001011010')

    def test_bits_to_bytes(self):
       self.assertEqual(bits_to_bytes('01'), bytearray([64]))
       self.assertEqual(bits_to_bytes('10110'), bytearray([176]))
       self.assertEqual(bits_to_bytes('011001011010'), bytearray([101, 160]))

    def test_huffman_code_file(self):
       with open("test_source.txt", "w", encoding = "utf-8") as file:
           file.write("abcde")
       huffman_code_file("test_source.txt", "test_target.bin")
       with open("test_target.bin", "rb") as f:
           data = f.read()
       self.assertTrue(len(data) > 0)

    


if (__name__ == '__main__'):
    unittest.main()
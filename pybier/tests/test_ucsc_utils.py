from unittest import TestCase

from pybier import ucsc_utils

class TestUCSC(TestCase):
    def test_gets_hg19_seq(self):
        seq = ucsc_utils.get_DNA_seq('chr11',61731757,61731806,ref='hg19')
        ans = 'ttcagcctttaatgccttttattcataaaaactgtgaaagctagactgaa'
        self.assertEqual(seq,ans)


# Import classes from your brand new package
from ucsc_utils import get_DNA_seq

FTH1_seq = get_DNA_seq('chr11',61731757,61735132,ref='hg19')

print(FTH1_seq)

from xml.dom import minidom
import urllib2

#Function to get hg19 sequence at given location
def get_DNA_seq(chrom,start,stop,ref='hg19'):
    das_prefix = 'http://genome.ucsc.edu/cgi-bin/das/'+ref+'/dna?segment='
    query = das_prefix+chrom+':'+str(start)+','+str(stop)
    response = urllib2.urlopen(query)
    xmldoc = minidom.parse(response)
    seq = xmldoc.getElementsByTagName('DNA')[0].firstChild.nodeValue.strip()
    return seq


def get_don_flank(chrom,pos,strand,flank=20):
    don_start = pos-(flank-1) if strand == '+' else pos
    don_stop = pos if strand == '+' else pos+(flank-1)

    don_seq = get_seq(chrom,don_start,don_stop)
    don_seq = don_seq if strand == '+' else rev_comp(don_seq)

    return don_seq


def get_acc_flank(chrom,pos,strand,flank=20):
    acc_start = pos if strand == '+' else pos-(flank-1)
    acc_stop = pos+(flank-1) if strand == '+' else pos

    acc_seq = get_seq(chrom,acc_start,acc_stop)
    acc_seq = acc_seq if strand == '+' else rev_comp(acc_seq)

    return acc_seq

def rev_comp(seq):
    comp = {'A':'T','T':'A','a':'t','t':'a',
            'G':'C','C':'G','g':'c','c':'g'}
    rev_comp = ''.join([comp[base] for base in seq][::-1])
    return rev_comp

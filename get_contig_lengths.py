import sys
import re
import gzip

#usage: python get_contig_lengths.py in_vcf.gz out_lengths.txt

in_file = sys.argv[1]
out_file = sys.argv[2]

f = gzip.open(in_file, 'r')
o = open(out_file, 'w')

for i in f:
	if re.search('##contig=<ID=flattened_line_', i):
		split = re.split('=', i)
		c = split[2]
		l = split[3]
		contig,non = c.split(',')
		length = l[:-2]
		o.write(contig+'\t'+length+'\n')
	
f.close()
o.close()

#creates a tab-separated file with contig names and lengths from a vcf file

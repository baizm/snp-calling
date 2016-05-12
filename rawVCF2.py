import subprocess
import argparse
import sys
import glob
import re

seq = '/scratch/lsa_flux/baizm/reference_genome/AloPal_combined.a.lines.fasta'
dir = '/scratch/lsa_flux/baizm/alignments/'
out_dir = '/scratch/lsa_flux/baizm/snpCalling/'

bamfiles = sorted(glob.glob(dir + '*all.rg.bam'))
#create a list of *all.rg.bam files in dir
bamfiles = ' '.join(bamfiles)
	
out1 = '%sraw.vcf' % (out_dir)
out2 = '%sfiltered_indel.vcf' % (out_dir)
out3 = '%sfiltered_final.vcf' % (out_dir)
	
#pipe output of mpileup to bcftools to get raw VCF file
subprocess.call("samtools mpileup -ugf %s -t DP,DPR %s | bcftools call -vmO v -o %s" % (seq, bamfiles, out1), shell=True)

#filter VCF to remove SNPs within 5 bp of indel
subprocess.call("vcfutils.pl varFilter -w 5 %s > %s" % (out1, out2), shell=True)

#filter VCF to remove SNPs with quality score less than 20, this step only takes a few minutes
f=open(out2, 'r')
o=open(out3, 'w')

for i in f:
	if re.search('^#', i):
		o.write(i)
	else:
		split=re.split('\t', i)
		q=float(split[5])
		if q>20:
			o.write(i)
 
f.close()
o.close()


#usage: python rawVCF2.py
#note: took ~33 hours for library 1

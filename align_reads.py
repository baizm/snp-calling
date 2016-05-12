import argparse
import os
import subprocess
import pandas as pd

parser = argparse.ArgumentParser(description='reads')
parser.add_argument('--ind', help="ind to run this on")
args = parser.parse_args()
ind = args.ind


seq = '/scratch/lsa_flux/baizm/reference_genome/AloPal_combined.a.lines.fasta'
read_dir = '/scratch/lsa_flux/baizm/Lane_1/cortes/flash_out/'
out_dir = '/scratch/lsa_flux/baizm/alignments/'


def align_seq_pe(ind, out_dir, read_dir, seq):
	r1 = '%s%s.notCombined_1.fastq.gz' % (read_dir, ind)
	r2 = '%s%s.notCombined_2.fastq.gz' % (read_dir, ind)
	
	out1 = '%s%s_pe.sam' % (out_dir, ind)
	out2 = '%s%s_pe.mateFixed.bam' % (out_dir, ind)
	out3 = '%s%s_pe.mateFixed.sorted' % (out_dir, ind)

	# align
	subprocess.call("bwa mem -t 20 %s %s %s > %s" % (seq, r1, r2, out1), shell=True)
	# fixmate
	subprocess.call("samtools fixmate %s %s" % (out1, out2), shell=True)
	# sorted
	subprocess.call("samtools sort %s %s" % (out2, out3), shell=True)
	
	
def align_seq_ext(ind, out_dir, read_dir, seq):
	ex = '%s%s.extendedFrags.fastq.gz' % (read_dir, ind)

	out1 = '%s%s_ext.sam' % (out_dir, ind)
	out2 = '%s%s_ext.bam' % (out_dir, ind)
	out3 = '%s%s_ext.sorted' % (out_dir, ind)
	
	# align
	subprocess.call("bwa mem -t 20 %s %s > %s" % (seq, ex, out1), shell=True)
	# bam
	subprocess.call("samtools view -uS %s > %s" % (out1, out2), shell=True)
	# sorted
	subprocess.call("samtools sort %s %s" % (out2, out3), shell=True)


def merge_and_rg(ind, out_dir, read_dir, seq):

	out1 = '%s%s_pe.mateFixed.sorted.bam' % (out_dir, ind)
	out2 = '%s%s_ext.sorted.bam' % (out_dir, ind)
	out3 = '%s%s_all.bam' % (out_dir, ind)
	out4 = '%s%s_all.rg.bam' % (out_dir, ind)
	intervals = '%s%s_all.intervals' % (out_dir, ind)
	out5 = '%s%s_all.realigned.bam' % (out_dir, ind)
	out6 = '%s%s_all.bwamem.unique.bam' % (out_dir, ind)


	# merge bam files for alignments of paired extended reads  
	subprocess.call("samtools merge %s %s %s" % (out3, out1, out2), shell=True) 
	# readgroup
	subprocess.call("java -jar ./picard.jar AddOrReplaceReadGroups INPUT=%s OUTPUT=%s RGLB=%s RGPL=Illumina RGPU=%s RGSM=%s" % (out3, out4, ind, ind, ind), shell=True)
	subprocess.call("samtools index %s" % out4, shell=True)
	


# align all the way until time to call SNPs
align_seq_pe(ind, out_dir, read_dir, seq)
align_seq_ext(ind, out_dir, read_dir, seq)
merge_and_rg(ind, out_dir, read_dir, seq)

'''
Simple tool for post processing ATLAS-SNP2 or ATLAS-INDEL VCFs.

It can do several things:
  1. Append the string 'chr' to all contig IDs in a vcf file.
  2. Strip .snp.vcf (SNP2) or  from all sample names.
'''

import optparse
import os
import gzip

## pulls the SM tag from the header of a BAM
def extract_sm(bam, direc):
  bamReader = gzip.open(direc + '/' + bam, 'r')
  for line in bamReader:
    if 'SM' in line:
      fields = line.split()
      sm = [f for f in fields if f.startswith('SM')][0].lstrip('SM:')
      break
  bamReader.close()
  return sm  

## builds a sample ID by the same logic used in the swift script
def construct_id(bam):
  iid = bam.strip(bam + '.snp.vcf')
  return iid

def strip_id(sample, stripStr):
  '''
  Strips a string off of a sample ID.
  '''
  return sample.strip(stripStr)


def main():

  ## parse command line arguments
  parser = optparse.OptionParser()
  parser.add_option('-v', dest = 'oldvcf', help = 'Filepath for input vcf file.')
  parser.add_option('-o', dest = 'newvcf', help = 'Filepath for output vcf file.')
  parser.add_option('-d', dest = 'bamdir', help = 'Directory containing source BAM files.')
  parser.add_option('-s', dest = 'stripStr', help = 'String to strip from sample names.')
  parser.add_option('-c', action = 'store_true', dest = 'addChr', help = 'Switch for prepending chr to contig IDs.')
  (opts, args) = parser.parse_args()

  ## open file connections
  oldvcf = open(opts.oldvcf)
  newvcf = open(opts.newvcf, 'w')
  
  ## copy over vcf header
  head = oldvcf.next()
  newvcf.write(head)
  while head.startswith('##'):
      head = oldvcf.next()
      if head.startswith('#CHROM'):
        break
      newvcf.write(head)

  if opts.bamdir:
    ## match SM tags to file names
    sampleIds = dict()
    for (path, dirs, files) in os.walk(opts.bamdir):
      for bam in files:
        if bam.endswith('.bam'):
          sm = extract_sm(bam, opts.bamdir)
          oldId = construct_id(bam)
          sampleIds[oldId] = sm
    ## recode the sample Ids
    line = [ sampleIds[f] if sampleIds.get(f) else f for f in head.split() ]
  else:
    line = head.split()

  ## strip nonsense off of sample IDs if neccessary
  if opts.stripStr:
    line = [ x.strip(opts.stripStr) for x in head.split() ]
  else:
    line = head.split()  

  print >> newvcf, '	'.join(line)

  ## recode the chromosome IDs in the file
  for line in oldvcf:
      if opts.addChr: line = 'chr' + line
      newvcf.write(line)

  ## close file connections
  oldvcf.close()
  newvcf.close()

if __name__ == '__main__':
  main()


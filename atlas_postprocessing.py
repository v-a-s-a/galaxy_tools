'''
Simple tool to append the string 'chr' to all contig IDs in a vcf file
'''

import optparse
import os
import gzip

## pulls the SM tag from the header of a BAM
def extract_sm(bam):
  bamReader = gzip.open(bam, 'r')
  for line in bamReader:
    if 'SM' in line:
      fields = line.split()
      sm = [f for f in fields if f.startswith('SM')][0]
      break
  bamReader.close()
  return sm  

## builds a sample ID by the same logic used in the swift script
def construct_id(bam):
  iid = bam.strip('.bam') + '.snp.vcf'
  return iid



def main():

  ## parse command line arguments
  parser = optparse.OptionParser()
  parser.add_option('-v', dest = 'oldvcf', help = 'Filepath for input vcf file.')
  parser.add_option('-o', dest = 'newvcf', help = 'Filepath for output vcf file.')
  parser.add_option('-d', dest = 'bamdir', help = 'Directory containing source BAM files')
  (opts, args) = parser.parse_args()

  ## open file connections
  oldvcf = open(opts.oldvcf)
  newvcf = open(opts.newvcf, 'w')

  ## match SM tags to file names
  sampleIds = dict()
  for (path, dirs, files) in os.walk(bamdir):
    for bam in files:
      if bam.endswith('.bam'):
        sm = extract_sm(bam)
        oldId = construct_id(bam)
        sampleIds[oldId] = sm

  ## copy over vcf header
  head = oldvcf.next()
  newvcf.write(head)
  while head.startswith('##'):
      if head.startswith('#CHROM'):
        break
      else:
        head = oldvcf.next()
        newvcf.write(head)

  ## recode the sample Ids
  line = [ f for f in head.split('') ]
  line = [ sampleIDs[f] for f in if sampleIDs.get(f) ]
  newvcf.write(head)

  ## recode the chromosome IDs in the file
  for line in oldvcf:
      line = 'chr' + line
      newvcf.write(line)

  ## close file connections
  oldvcf.close()
  newvcf.close()

if __name__ == '__main__':
  main()


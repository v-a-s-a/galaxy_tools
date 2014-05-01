import argparse as arg
import os
import subprocess as sp

class region:
  """
  Single line of a BED file. A region defined by:
    {chromosome:start:end}
  """
  def __init__(self, chrom, start, end):
    self.chrom = chrom
    self.start = int(start)
    self.end = int(end)

class variant:
  """
  A variant defined by {chromosome:position}
  """
  def __init__(self, chrom, pos):
    self.chrom = chrom
    self.pos = int(pos)
    self.ID = chrom + ':' + str(pos)

  def __hash__(self):
    return hash(self.ID)

  def __eq__(self, other):
    if self.chrom == other.chrom and self.pos == other.pos: return True
    else: return False
  
  def __str__(self):
    return self.chrom + ':' + str(self.pos)
  
class bed:
  """
  Representation of a BED file. Essentially a list of region objects.
  """
  def __init__(self, bedFile):
    self.bedFile = bedFile
    self.regions = list()
    with open(self.bedFile) as f:
      for line in f:
        line = line.strip().split()
        if len(line) != 3: continue
        self.regions.append(region(chrom=line[0], start=line[1], end=line[2]))

  def is_present(self, var):
    """
    Check if variant falls within a region described by a BED file.

    ** regions can be ordered -- this needs to be a binary search 
  
    input: object of class 'var'
    return: True if BED contains var, False otherwise.
    """
    relevantRegions = ( x for x in self.regions if x.chrom == var.chrom )
    for region in relevantRegions:
      if region.start <= var.pos and region.end >= var.pos: return True
      else: return False


def __main__():
  """
  Generate a list of observed sites from a directory of VCF files. Allow this list to be filtered against a bed file.
  """
  ## parse command line args
  parser = arg.ArgumentParser()
  parser.add_argument('--bed', dest='bedFile')
  parser.add_argument('--min-qual', dest='minQual', nargs='?', const=0)
  parser.add_argument('--file-dir', dest='fileDir')
  parser.add_argument('--mode', choices=['vcf', 'indel'], dest='mode')
  parser.add_argument('--out', dest='out')
  args = parser.parse_args()

  ## GLOBALS
  minQual = int(args.minQual)

  ## pull the directory of files, and the location of the BED file.
  if args.mode == 'vcf': fileext = 'vcf'
  elif args.mode == 'indel': fileext = 'indel'
  for root, dirs, files in os.walk(args.fileDir):
    vcfs = [root+x for x in files if x.endswith(fileext)]

  ## make a BED object to check variant memebership
  bedChecker = bed(args.bedFile)

  ## walk VCF files
  uniqVariants = set()
  for vcfFile in vcfs:
    print vcfFile
    ## use ekg's bed filter
    p = sp.Popen(['vcfintersect', '--bed', args.bedFile, vcfFile], stdout=sp.PIPE)
    vcf = p.stdout
    while vcf.next().strip().startswith('##'): pass
    for line in vcf:
      line = line.split('	', 8)
      var = variant(line[0], line[1])
      ## include only variants that: PASS, are in BED, and have minimum QUAL
      if not var in uniqVariants:
        if line[6]=='PASS':
          if int(line[5])>=minQual:  
            uniqVariants.add(var)
    vcf.close()

  ## write our variants of interest out to file
  outfile=open(args.out, 'w')
  for var in uniqVariants:
    print >> outfile, var.chrom + '\t' + str(var.pos)
  outfile.close() 


if __name__ == '__main__':
  __main__()

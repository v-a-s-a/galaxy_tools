import argparse as arg
import os

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
    if self.chrom == other.chrom and self.pos = other.pos: return True
    else: return False

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
        regions.append(region(chrom=line[0], start=line[1], end=line[2]))

  def is_present(self, var):
    """
    Check if variant falls within a region described by a BED file.
 
    ** We can save this for later -- this is a more complicated idea.
    ** I wanted to hash region starts and ends
    To check membership for a given variant:
      pull tuple of regions associated with chromosome
      find regions with variant position > start
      find regions with variant position < end
    Variant is described in BED if the intersection of the above is non-empty
  
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
  parse.add_argument('--min-qual', dest='minQual', const=0)
  parser.add_argument('--vcf-dir', dest='vcfDir')
  parser.add_argument('--out', dest='out')
  args = parser.parse_args()

  ## GLOBALS
  minQual = int(args.minQual)

  ## pull the directory of VCF files, and the location of the BED file.
  for root, files, dirs in os.walk(args.vcfDir):
    vcfs = [root+x for x in files if x.endswith('vcf')]

  ## make a BED object to check against
  bedChecker = bed(args.bedFile)

  ## walk VCF files
  uniqVariants = set()
  for vcfFile in vcfs:
    vcf = open(vcfFile)
    while vcf.next().startswith('##'): pass
    for line in vcf:
      line = line.split(' ', 8)
      var = variant(line[0], line[1])
      ## include only variants that: PASS, are in BED, and have minimum QUAL
      if line[6]=='PASS' and bedChecker.is_present(var) and int(line[5])>=minQual:
        uniqVariants.add(var)
     vcf.close()

  ## write our variants of interest out to file
  outfile=open(args.out, 'w')
  for var in uniqVar:
    print >> outfile, var.chrom + '\t' + str(var.pos)
  outfile.close() 


if __name__ == '__main__':
  __main__()

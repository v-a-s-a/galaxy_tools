#!/usr/bin/python
"""
Simple script to pull variant sites from all VCF files in a directory.

Shell script provided by the Atlas team:
  for file in *.vcf
    do grep -v '^#' $file | cut -f1,2 >>tmp
  done
  sort -n -k1 -k2 tmp | uniq >master-site-list
  rm tmp

"""

import os
import optparse
import time

def __main__():
  
  ## parse command line arguments
  parser = optparse.OptionParser()
  parser.add_option('--vcf-directory',
    dest='vcf_dir',
    type="string",
    help="Directory of VCF files to aggregate variants from.")
  parser.add_option('--output-file',
    dest='out_file',
    type="string",
    help="Location of file to write master site list to.")
  (opts, args) = parser.parse_args()

  master_variants = set()
  out_file = open(opts.out_file, 'w')

  ## walk the directory
  for (path, dirs, files) in os.walk(opts.vcf_dir):
    for vcf in files:
      vcf = open(path+vcf)
      ## skip header
      while vcf.next().startswith('##'): None
      
      ## add first two fields of each line to master variant set
      for line in vcf:
        ## prematurely optimized
        #start_time = time.time()
        var = line[:line.index('\t') + line[1+line.index('\t'):].index('\t') + 2]
        #end_time = time.time()
        #print("1: Elapsed time was %g seconds" % (end_time - start_time))

        ### slower
        #start_time = time.time()
        #var = '\t'.join(line.split()[:2])
        #end_time = time.time()
        #print("2: Elapsed time was %g seconds" % (end_time - start_time))
  
        if var not in master_variants:
          master_variants.add(var)
          print >> out_file, var


if __name__ == "__main__":
  __main__()


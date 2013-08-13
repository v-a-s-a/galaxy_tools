'''
List all observed variants in a directory of vcf files.
'''

import os
import optparse as opt

def main():

  parser = opt.OptionParser()
  parser.add_option('--vcf-dir', dest="vcfDir")
  parser.add_option('--out', dest="outfile")
  (opts, args) = parser.parse_args()

  intersect = set()
  for path, dirs, files in os.walk(opts.vcfDir):
    vcfs = [ f for f in files if f.endswith('snp.recode.vcf')]
    for vcf in vcfs:
      print vcf
      vcf = open(opts.vcfDir + vcf)
      while vcf.next().startswith('##'): pass
      for line in vcf:
        line = line.split('	', 8)
        if line[6] == 'PASS':
          var = '	'.join( [line[0], line[1]] )
          intersect.add(var)
      vcf.close()

  print '%i total variants found.' % len(intersect)

  outfile=open(opts.outfile, 'w')
  for var in intersect:
    print >> outfile, var
  outfile.close()

if __name__ == '__main__':
  main()


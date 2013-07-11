'''
Simple tool to append the string 'chr' to all contig IDs in a vcf file
'''

import optparse

def main():

  ## parse command line arguments
  parser = optparse.OptionParser()
  parser.add_option('-v', dest = 'oldvcf', help = 'Filepath for input vcf file.')
  parser.add_option('-o', dest = 'newvcf', help = 'Filepath for output vcf file.')
  (opts, args) = parser.parse_args()

  ## open file connections
  oldvcf = open(opts.oldvcf)
  newvcf = open(opts.newvcf, 'w')

  ## copy over vcf header
  head = oldvcf.next()
  newvcf.write(head)
  while head.startswith('##'):
      head = oldvcf.next()
      newvcf.write(head)
      
  ## recode the rest of the file
  for line in oldvcf:
      line = 'chr' + line
      newvcf.write(line)

  ## close file connections
  oldvcf.close()
  newvcf.close()

if __name__ == '__main__':
  main()


#!/bin/bash

## parse command line args
config_file=$1
vcf_dir=$(grep VCF $config | awk '{print $2}')

output_file=$2

## pull ALL variant sites from experiment
for file in $(ls ${vcf_dir}*.vcf); do
  echo $file
  grep -v '^#' $file | cut -f1,2 >> tmp
done

## subset to unique sites
sort -n -k1 -k2 /tmp/atlas_tmp | uniq > $output_file
rm /tmp/atlas_tmp

#!/bin/sh

python depPath/extractRelevantDepPaths.py \
  --wikideppaths new_wikipedia_deppaths.txt \
  --trfile bless2011/data_lex_train.tsv \
  --outputfile output/relevantPaths.txt

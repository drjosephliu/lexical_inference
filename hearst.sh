#!/bin/sh
python hearst/extractHearstHyponyms.py \
  --inputwikifile wikipedia_sentences.txt \
  --outputfile output/hearst.txt

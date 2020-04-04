#!/bin/sh
python hearst/extractHearstHyponyms.py \
  --inputwikifile wikipedia_sentences.txt \
  --oututfile output/hearst.txt

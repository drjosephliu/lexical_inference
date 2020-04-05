#! /bin/sh

python depPath/extractDepPathHyponyms.py \
  --wikideppaths new_wikipedia_deppaths.txt \
  --relevantdeppaths output/relevantPaths.txt \
  --outputfile output/deppaths.txt



python extractDatasetPredictions.py \
  --extractionsfile output/deppaths.txt \
  --trdata bless2011/data_lex_train.tsv \
  --valdata bless2011/data_lex_val.tsv \
  --testdata bless2011/data_lex_test.tsv \
  --trpredfile output/train_pred_deppaths.txt \
  --valpredfile output/val_pred_deppaths.txt \
  --testpredfile output/test_pred_deppaths.txt

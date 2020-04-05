#!/bin/sh
python extractDatasetPredictions.py  \
 --extractionsfile output/hearst.txt \
 --trdata bless2011/data_lex_train.tsv \
 --valdata bless2011/data_lex_val.tsv \
 --testdata bless2011/data_lex_test.tsv \
 --trpredfile output/train_pred_hearst.txt \
 --valpredfile output/val_pred_hearst.txt \
 --testpredfile output/test_pred_hearst.txt

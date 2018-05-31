python3 main.py -f "title_rel_assigned_Haley - title_rel_assigned.csv" -l 3 -d 4

bin/fasttext supervised -input pdata.train -output classifiername -lr 1.0 -epoch 25 -wordNgrams 2 -verbose 2 

bin/fasttext test classifiername.bin pdata.valid


# bin/fasttext predict classifiername.bin -
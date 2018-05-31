python3 main.py -f "filename with space possible.csv" -l 3 -d 4

bin/fasttext supervised -input exo.train -output classifiername -lr 1.0 -epoch 25 -wordNgrams 2 -verbose 2


bin/fasttext test classifiername.bin exo.valid 


bin/fasttext predict classifiername.bin -
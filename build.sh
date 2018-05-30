python3 main.py -f "filename with space possible.csv" -l 3 -d 4

./fasttext supervised -input exo.train -output classifiername -lr 1.0 -epoch 25 -wordNgrams 2 -verbose 2


./fasttext test classifiername.bin exo.valid 


./fasttext predict classifiername.bin -
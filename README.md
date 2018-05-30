# text-classifier

A NLP project for classifying texts as relevant / irrelevant by training a fasttext model using labeled data from csv file.

### Process, build, test and interactive predict:
- `source build.sh`

### Notes
- *.train, *.valid, ftdataset.txt are auto-generated
- the model is *.bin and its corresponding embedding is *.vec
- The label and Data columns is set in the `process()` function of `main.py`
- In the `build.sh`, `-f` is name of csv file, `-l` is the label column and `-d` is the column
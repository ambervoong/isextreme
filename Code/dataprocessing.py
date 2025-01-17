# -*- coding: utf-8 -*-
"""DataProcessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jYsv5mMHchpL0Kf23Z8ekYgBeolYQ1Fj
"""

import pandas as pd

"""# Preprocessing

TSV FORMAT:
BERT wants data to be in a tsv file with a specific format, (Four columns, and no header row).
Column 0: An ID for the row
Column 1: The label for the row (should be an int)
Column 2: A column of the same letter for all rows. 
Column 3: The text for the row

BERT comes with data loading classes that expects **train and dev files ** in the above format. 

We can use the train data to train our model, and the dev data as the validation set.

BERT’s data loading classes can also use a test file but it expects the test file to be unlabelled. Therefore, I will be using the train and dev files instead.
"""

def change_to_tsv(filepath, folder):
    dev = pd.read_csv(filepath)

    dev_tsv = pd.DataFrame({
        'id':range(len(dev)),
        'label':1,  #"test sets" don't have labels
        'alpha':['a']*dev.shape[0],
        'text': dev["cleaned"].replace(r'\n', ' ', regex=True)# Replaces newline chars
                                                                  # with spaces.
    })


    dev_tsv.to_csv(folder + '/dev.tsv', sep='\t', index=False, header=False)


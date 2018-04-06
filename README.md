# POS-tagger

1. A Hidden Markov Model part-of-speech tagger for any language (tested for English, Chinese and Hindi).

2. The training data are provided tokenized and tagged; the test data will be provided tokenized, and the tagger will add the tags.

3. hmmlearn3.py will learn a hidden Markov model from the training data, and hmmdecode3.py will use the model to tag new data.

4. The learning program will be invoked in the following way:
   python hmmlearn3.py /path/to/input (refer to en_train_tagged.txt or zh_train_tagged.txt)

5. The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt.

6. The tagging program will be invoked in the following way:
   python hmmdecode3.py /path/to/input (refer to en_dev_raw.txt or zh_dev_raw.txt)
   
7. The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.


   


# TFIDF for a directory of txt files
This single script takes a directory as a param and reads the txt files generating an html file with the output results.
Libraries used:
glob
shutil
textblob
nltk

On Ubuntu: Python 3.5.4 :: Anaconda custom (64-bit)

1) Check your installs:
   Everyone is set up on different operating systems and python enviorments.
   You potentially need/do not need some of these libraries.
2) tfidf_processor.py:
   REads the directory for each text file and then runs the term frequency/ inverse document frequency functionality across them. Upon completion it generates an html output file with the results.

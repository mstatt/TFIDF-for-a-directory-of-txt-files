# -*- coding: utf-8 -*-
def tfidf_calc(outdir):
    import os
    import glob
    import shutil
    import math
    import nltk
    #nltk.download('stopwords')
    from textblob import TextBlob as tb
    from nltk.corpus import stopwords

    cachedStopWords = stopwords.words("english")
    #Below is the input directory of the files to be analyzed
    compdir = 'forprocessing/'
    #Adjustable word count for the output
    numofwords = 20

    def tf(word, blob):
        return blob.words.count(word) / len(blob.words)

    def n_containing(word, bloblist):
        return sum(1 for blob in bloblist if word in blob.words)

    def idf(word, bloblist):
        return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

    def tfidf(word, blob, bloblist):
        return tf(word, blob) * idf(word, bloblist)

    number_of_files = str(len([item for item in os.listdir(compdir) if os.path.isfile(os.path.join(compdir, item))]))
    print("Processing ("+ number_of_files + ") files for TFIDF.....")
    bloblist = []
    filename_listtf = []
    print("Building list and stream for TFIDF calculation......")
    for filename2tf in sorted(glob.glob(compdir+"*.txt")):
        with open(filename2tf, 'r') as myfile2tf:
            initstream = "".join(line.rstrip() for line in myfile2tf).upper()
            txtstreamtf =tb(" ".join([word for word in initstream.split() if word not in cachedStopWords]))
            filename_listtf.append(os.path.basename(filename2tf))
            bloblist.append(txtstreamtf)
            myfile2tf.close()


    print("Writing web page for TFIDF calculation......")
    with open (outdir+"tfidf.html","a",encoding="utf-8")as fp1tfidf:
        fp1tfidf.write("<!DOCTYPE html><html><!DOCTYPE html><html lang='en'><head><title>TF/IDF Calculation</title></head><body>")
        fp1tfidf.write("<h1><u>TF/IDF:</u></h1>")
        fp1tfidf.write('<p>Typically, the tf-idf weight is composed by two terms: the first computes the normalized Term Frequency (TF), aka. the number of times a word appears in a document, divided by the total number of words in that document; the second term is the Inverse Document Frequency (IDF), computed as the logarithm of the number of the documents in the corpus divided by the number of documents where the specific term appears.</p>')
        fp1tfidf.write('<ul><li><p>TF: Term Frequency, which measures how frequently a term occurs in a document. Since every document is different in length, it is possible that a term would appear much more times in long documents than shorter ones. Thus, the term frequency is often divided by the document length (aka. the total number of terms in the document) as a way of normalization:</p>')
        fp1tfidf.write('<p>TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).</p></li>')
        fp1tfidf.write('<li><p>IDF: Inverse Document Frequency, which measures how important a term is. While computing TF, all terms are considered equally important. However it is known that certain terms, such as "is", "of", and "that", may appear a lot of times but have little importance. Thus we need to weigh down the frequent terms while scale up the rare ones, by computing the following:</p>')
        fp1tfidf.write('<p>IDF(t) = log_e(Total number of documents / Number of documents with term t in it).</p></li><br/>')
        fp1tfidf.write("<table border=1>")
        for i, blob in enumerate(bloblist):
            fp1tfidf.write("<tr><td colspan=2>")
            fp1tfidf.write("Top words "+ str(numofwords) +" in document {}".format(filename_listtf[i]))
            fp1tfidf.write("</td></tr>")
            scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for word, score in sorted_words[:numofwords]:
                fp1tfidf.write("<tr><td>")
                fp1tfidf.write("\tWord: {}</td><td> TF-IDF: {} </td></tr>".format(word, round(score, 5)))
            fp1tfidf.write("</tr>")

        fp1tfidf.write("</table></body></html>")
    fp1tfidf.close()
    print("TF/IDF calculation completed on ("+ number_of_files + ") files******************************")
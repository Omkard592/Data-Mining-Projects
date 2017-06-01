#AUTHOR: OMKAR KETAN DESHMUKH
#UNIVERSITY OF TEXAS AT ARLINGTON
#UTA ID: 1001275806
#DATA MINING: PROGRAMMING ASSIGNMENT 1
#PROGRAM: IMPLEMENT TOY SEARCH ENGINE

import os
import sys
import math
import operator                                     #to convert dict to list
from nltk.tokenize import RegexpTokenizer           #for tokenizing
from nltk.corpus import stopwords                   #for removing stopwords
from nltk.stem.porter import PorterStemmer          #for stemming the tokens



##########################################################################################
def transform(doc):
    ############################## TOKENIZE THE FILE ##############################
    doc = doc.lower()                               #convert to lowercase
    tokens = tokenizer.tokenize(doc)                #tokenize the document, tokenizing into pure english alphabet words
    tokens = sorted(tokenizer.tokenize(doc))        #sort the tokens for optimized processing in the future
    ############################## TOKENIZE THE FILE ##############################


    ############################## REMOVE STOP WORDS ##############################
    english_stopwords = sorted(stopwords.words('english'))
    s = set(english_stopwords)                              #fastest solution to find difference between lists: credit goes to
    non_stopwords = [x for x in tokens if x not in s]       #http://stackoverflow.com/questions/3462143/get-difference-between-two-lists
    ############################## REMOVE STOP WORDS ##############################


    ############################## STEM THE NON STOPWORDS ##############################
    stemmer = PorterStemmer()                       #create stemmer object
    stemmed_tokens = []

    for word in non_stopwords:
        stemmed_tokens.append(stemmer.stem(word))   #store stemmed non-stopwords in a separate list

    return stemmed_tokens
    ############################## STEM THE NON STOPWORDS ##############################
##########################################################################################


##########################################################################################
def getidf(token):                                  #get inverse document frequency
    if isinstance(token, str):
        try:
            get_dft = doc_freq[token]
            return math.log10(doc_count / get_dft)
        except KeyError:
            return -1   #Token not found
    else:
        return -1   #Invalid parameters
##########################################################################################


##########################################################################################
def getweight(filename, token):                     #get TF-IDF weight
    if isinstance(filename, str) and isinstance(token, str):
        try:
            term_weight_dict = term_weight[token]
        except KeyError:
            return 0    #Token not found

        try:
            doc_no = inv_doc_names[filename]
            tw = term_weight_dict[doc_no]
            return tw
        except KeyError:
            return 0    #Document not found
    else:
        return 0    #Invalid parameters
##########################################################################################


##########################################################################################
def query(qstring):
    ############################## NORMALIZE THE QUERY JUST LIKE THE CONTENT OF THE DOCUMENTS ##############################
    if isinstance(qstring, str):                   #sanity check for query string
        query_term_freq = {}
        query_term_weight = {}
        query_stemmed_tokens = transform(qstring)
        query_unique_stemmed_tokens = list(set(query_stemmed_tokens))

        for ust in query_unique_stemmed_tokens:
            try:
                x = query_term_freq[ust]
                print('Oops I shouldnt have printed this:', x)
            except KeyError:
                query_term_freq[ust] = 0

            try:
                x = query_term_weight[ust]
                print('Oops I shouldnt have printed this:', x)
            except KeyError:
                query_term_weight[ust] = 0

        for st in query_stemmed_tokens:
            query_term_freq[st] = query_term_freq[st] + 1

        total = 0
        for ust in query_unique_stemmed_tokens:
            query_term_weight[ust] = 1 + math.log10(query_term_freq[ust])
            total = total + (query_term_weight[ust] * query_term_weight[ust])   #normalize using L2 norm

        for ust in query_unique_stemmed_tokens:
            query_term_weight[ust] = query_term_weight[ust] / math.sqrt(total)    #normalize using L2 norm
        ############################## NORMALIZE THE QUERY JUST LIKE THE CONTENT OF THE DOCUMENTS ##############################


        ############################## PROCESS THE QUERY TOKENS ##############################
        top_ten_list = []
        unq_docs_ttl = {}
        useful_qt_count = 0
        proceed = False          #for the case where none of the tokens in query are in corpus
        upper_limit = []
        useful_terms = []

        for k in query_term_freq.keys():
            try:
                tt = postings_list[k][:10]
                useful_qt_count = useful_qt_count + 1
                proceed = True
                useful_terms.append(k)
            except KeyError:
                continue

            upper_limit.append(tt[len(tt)-1][1])
            top_ten_list.append(tt)

            for t in tt:
                try:
                    ct = unq_docs_ttl[t[0]]
                    ct[0] = ct[0] + 1
                    unq_docs_ttl[t[0]] = ct

                except KeyError:
                    ct = []
                    ct.append(1)
                    unq_docs_ttl[t[0]] = ct

        if not proceed:                         #avoid any more computation and end query processing
            return('None', 0)

        fetch_more = True

        for u in unq_docs_ttl.keys():
            tct = unq_docs_ttl[u]

            if tct[0] == useful_qt_count:
                qd_weight = 0
                fetch_more = False

                for qust in useful_terms:
                    temp_d = term_weight[qust]
                    qd_weight = qd_weight + (query_term_weight[qust] * temp_d[u])

                temp_ct = unq_docs_ttl[u]
                temp_ct.append(qd_weight)
                unq_docs_ttl[u] = temp_ct

            else:
                qd_weight = 0
                indx = 0

                for indx in range(0, len(useful_terms)):
                    found_doc = False
                    ttl = top_ten_list[indx]

                    for j in ttl:
                        if j[0] == u:
                            temp_d = term_weight[useful_terms[indx]]
                            qd_weight = qd_weight + (query_term_weight[useful_terms[indx]] * temp_d[u])
                            found_doc = True
                            break

                    if not found_doc:
                        qd_weight = qd_weight + (query_term_weight[useful_terms[indx]] * upper_limit[indx])
                    indx = indx + 1

                temp_ct = unq_docs_ttl[u]
                temp_ct.append(qd_weight)
                unq_docs_ttl[u] = temp_ct

        if fetch_more:
            return('fetch more', 0)

        semi_final_res = {}
        final_res = {}
        for key, value in unq_docs_ttl.items():
            semi_final_res[key] = value[1]

        final_res = sorted(semi_final_res.items(), key=operator.itemgetter(1), reverse=True)
        top_doc_details = unq_docs_ttl[final_res[0][0]]
        top_doc_count = top_doc_details[0]

        if top_doc_count == useful_qt_count:
            final_doc_name = doc_names[final_res[0][0]]
            score = final_res[0][1]
            return(final_doc_name, score)
        else:
            return('fetch more', 0)

    else:
        return('Invalid parameters', 0)
    ############################## PROCESS THE QUERY TOKENS ##############################
##########################################################################################


##########################################################################################
corpusroot = './presidential_debates'               #root directory of all the docs
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')           #our custom regular expression

doc_names = {}
inv_doc_names = {}
doc_count = 0
term_freq = {}
doc_freq = {}
term_weight = {}
docwise_length = {}
postings_list = {}

for filename in os.listdir(corpusroot):             #main loop to scan all text files
    ############################## READ THE FILE ##############################
    file = open(os.path.join(corpusroot, filename), "r", encoding='UTF-8')
    doc = file.read()                               #store file in doc String
    doc_count = doc_count + 1
    doc_names[doc_count] = filename
    inv_doc_names[filename] = doc_count
    file.close()
    ############################## READ THE FILE ##############################


    ############################## TRANSFORM THE FILE ##############################
    stemmed_tokens = transform(doc)
    unique_stemmed_tokens = list(set(stemmed_tokens))    #make a unique list of tokens
    ############################## TRANSFORM THE FILE ##############################


    ############################## INIT DICTIONARIES & CALCULATE TF VECTOR ##############################
    for ust in unique_stemmed_tokens:
        try:                                    #create dictionary for term frequency
            x = term_freq[ust]
            tfd = term_freq[ust]
            tfd[doc_count] = 0
            term_freq[ust] = tfd
        except KeyError:
            tfd = {}
            tfd[doc_count] = 0
            term_freq[ust] = tfd

        try:                                    #create dictionary for document frequency
            x = doc_freq[ust]
        except KeyError:
            doc_freq[ust] = 0

        try:                                    #create dictionary for term weight
            x = term_weight[ust]
            twd = term_weight[ust]
            twd[doc_count] = 0
            term_weight[ust] = twd
        except KeyError:
            twd = {}
            twd[doc_count] = 0
            term_weight[ust] = twd

    for ust in unique_stemmed_tokens:           #update document frequency for all terms of that document
        doc_freq[ust] = doc_freq[ust] + 1

    for st in stemmed_tokens:                   #update term frequency for all terms of that document
        temp_tfd = term_freq[st]
        x = temp_tfd[doc_count]
        temp_tfd[doc_count] = x + 1
        term_freq[st] = temp_tfd
    ############################## INIT DICTIONARIES & CALCULATE TF VECTOR ##############################


############################## CALCULATE TF-IDF VECTOR ##############################
for i in range(1, doc_count + 1):
    total_len = 0

    for k in term_freq.keys():
        temp_twd = term_weight[k]
        temp_tfd = term_freq[k]

        try:
            tf = temp_tfd[i]
        except KeyError:
            tf = 0

        if tf > 0:
            temp_twd[i] = (1.0 + math.log10(tf)) * (math.log10(doc_count/doc_freq[k]))
        else:
            temp_twd[i] = 0

        total_len = total_len + (temp_twd[i] * temp_twd[i])         #normalize using L2 norm
        docwise_length[i] = total_len
        term_weight[k] = temp_twd

for i in range(1, doc_count + 1):
    for k in term_weight.keys():
        temp_twd = term_weight[k]
        try:
            temp_twd[i] = temp_twd[i] / math.sqrt(docwise_length[i])    #normalize using L2 norm
        except ZeroDivisionError:
            print('Divide by zero error! Exiting the program')
            sys.exit()

for k in term_weight.keys():                                        #create postings list from term weight dictionary
    x = term_weight[k]
    sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    postings_list[k] = sorted_x
############################## CALCULATE TF-IDF VECTOR ##############################


############################## PLACE YOUR QUERIES AND TEST CASES INSIDE THIS BLOCK ##############################


############################## PLACE YOUR QUERIES AND TEST CASES INSIDE THIS BLOCK ##############################

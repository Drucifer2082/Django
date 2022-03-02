from collections import defaultdict
from gensim import corpora, models, similarities

article = ""
article_corpus = []

# Creates a set of frequent words
stoplist = set('for a of the and to in'.split(' '))
# Lowercase each document, split it by white space and filter out stopwords
texts = [[word for word in article.lower().split() if word not in stoplist]
         for article in article_corpus]

# Counts word frequencies
frequency = collections.Counter(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# Only keep words that appear more than once
processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
pprint.pprint(processed_corpus)

"""corpora associates each word in the corpus with a unique integer ID. 
This dictionary defines the vocabulary of all words that our processing knows about."""

article_identifiers = corpora.Dictionary(processed_corpus)
print(article_identifiers.token2id)

dictionary = corpora.Dictionary(processed_corpus)
print(dictionary.token2id)


new_search = ""
new_vec = dictionary.doc2bow(new_search.lower().split())
print(new_vec)

bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
print(bow_corpus)


# train the model
tfidf = models.TfidfModel(bow_corpus)

# transform the "system minors" string
words = "system minors".lower().split()
print(tfidf[dictionary.doc2bow(words)])


"""Transforms the entire corpus with TFIDF"""
index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=12)


"""Queries the simiarities between documents in the corpus;  returns a percent"""

query = ''.split()
query_bow = dictionary.doc2bow(query)
sims = index[tfidf[query_bow]]
print(list(enumerate(sims)))

for article_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True):
    print(article_number, score)


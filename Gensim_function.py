from collections import defaltdict
from gensim import corpora

article = ""
article_corpus = []

# Creates a set of frequent words
stoplist = set('for a of the and to in'.split(' '))
# Lowercase each document, split it by white space and filter out stopwords
texts = [[word for word in article.lower().split() if word not in stoplist]
         for article in article_corpus]

# Counts word frequencies
frequency = defaultdict(int)
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

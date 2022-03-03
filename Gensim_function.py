import collections
from gensim import corpora, models, similarities

from .scraper import get_theguardian_articles, parse_theguardian_article

article = "Russia has pledged to stand its ground against what it calls “hostile actions” but has accepted that its economy will take a significant hit from the extensive sanctions imposed by the west in response to its invasion of Ukraine."

article_corpus = [ "Economists expect the sanctions to push Russia into a deep recession while driving inflation even higher this year, but do not think the economy will fail to function as long as the political will in the Kremlin exists to soften the impact of the measures.",
    "Once the initial crisis period of adjustment is over, the sanctions are expected to have a chronic impact on Russia, by limiting growth, imports and the opportunity to spend oil and gas revenues. Russia’s economy will become much more insular but energy exports will still generate a trade surplus.",
    "“Ninety-nine percent of the Russian people have no influence on Kremlin policy. I’m not keen on making life more miserable for ordinary Russians, which these sanctions will do,” said Gary Hufbauer of the Peterson Institute for International Economics."]

# Creates a set of frequent words
stoplist = set('for a of the and to in'.split(' '))
# Lowercase each document, split it by white space and filter out stopwords
# TODO: gensim.parsing.preprocessing.remove_stopword_tokens
texts = [[word for word in article.lower().split() if word not in stoplist]
         for article in article_corpus]

# Counts word frequencies
frequency = collections.Counter()
for text in texts:
    for token in text:
        frequency[token] += 1

# Only keep words that appear more than once
processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
print(processed_corpus)

"""corpora associates each word in the corpus with a unique integer ID.
This dictionary defines the vocabulary of all words that our processing knows about."""

article_identifiers = corpora.Dictionary(processed_corpus)
print(article_identifiers.token2id)

dictionary = corpora.Dictionary(processed_corpus)
print(dictionary.token2id)


new_search = "Russia military sanctions"
new_vec = dictionary.doc2bow(new_search.lower().split())
print(new_vec)

bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
print(bow_corpus)


# train the model
tfidf = models.TfidfModel(bow_corpus)

# transform the "system minors" string
words = "russian economy".lower().split()
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


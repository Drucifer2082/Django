import collections

from gensim import corpora, models, similarities


STOPLIST = set('for a of the and to in but'.split())
DEFAULT_QUERY = 'russian economy'.split()


def article_analysis(related_articles):
    """The Natural Language Processing analysis on the
    articles, returns a dictionary bag-of-words vector"""
    """Creates an additional set of stop words, final
    check to make sure some words do not get through"""
    # Lowercase each document, split it by white
    # space and filter out stopwords
    texts = [
        [word for word in article.lower().split()
         if word not in STOPLIST]
        for article in related_articles
    ]

    # Counts word frequencies
    frequency = collections.Counter()
    for text in texts:
        for token in text:
            frequency[token] += 1

    # Only keeps words that appear more than once
    processed_article = [
        [token for token in text if frequency[token] > 1]
        for text in texts
    ]
    return processed_article


def process_article(article, related_articles):
    processed_article = article_analysis(article)
    bow_corpus = keywords_into_vectors(processed_article)
    sims = training_the_model(bow_corpus)
    return sims


def keywords_into_vectors(processed_article):
    dictionary = corpora.Dictionary(processed_article)
    bow_corpus = [dictionary.doc2bow(text) for text in processed_article]
    return bow_corpus


def training_the_model(article, bow_corpus, dictionary):
    lsi = models.LsiModel(bow_corpus, id2word=dictionary, num_topics=2)
    vec_bow = dictionary.doc2bow(article.lower().split())
    vec_lsi = lsi[vec_bow]
    
    index = similarities.SparseMatrixSimilarity(lsi[bow_corpus],
            num_best=5, num_features=len(dictionary))
    sims = index[vec_lsi]  # perform a similarity query against the corpus

    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    return sims

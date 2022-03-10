import collections

from gensim import corpora, models, similarities
from gensim import utils
from gensim.parsing.preprocessing import remove_stopwords, preprocess_documents

STOPLIST = set('for a of the and to in but'.split())
DEFAULT_QUERY = 'russian economy'.split()

def telegraphic_text_single_article(article):
    """removes stopwords, predefined by Gensim, across the text."""
    filtered_article = remove_stopwords(article)
    return filtered_article


def telegraphic_text_multiple_articles(article_corpus):
    """removes stopwords across multiple texts."""
    post_processed_articles = preprocess_documents(article_corpus)
    return post_processed_articles


def article_analysis(filtered_article, related_articles):
    """The Natural Language Processing analysis on the
    articles, returns a dictionary bag-of-words vector"""
    """Creates an additional set of stop words, final
    check to make sure some words do not get through"""
    # Lowercase each document, split it by white
    # space and filter out stopwords
    texts = [
        [word for word in filtered_article.lower().split()
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
    processed_article = article_analysis(article, related_articles)
    article_kw_dict = selected_article_topical_keywords(processed_article)
    bow_corpus = keywords_into_vectors(processed_article)
    index, tfidf = training_the_model(bow_corpus)
    ret = searching_the_articles(index, tfidf, processed_article)
    return ret


def selected_article_topical_keywords(processed_article):
    dictionary = corpora.Dictionary(processed_article)

    # remove stop words and words that appear only once
    stop_ids = [
        dictionary.token2id[stopword]
        for stopword in STOPLIST
        if stopword in dictionary.token2id
        ]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids)
    dictionary.compactify()
    article_keyword_dictionary = dictionary
    ret = article_keyword_dictionary
    return ret


def keywords_into_vectors(processed_article):
    dictionary = corpora.Dictionary(processed_article)
    bow_corpus = [dictionary.doc2bow(text) for text in processed_article]
    return bow_corpus


def training_the_model(bow_corpus):
    """TF-IDF is a statistical measure that evaluates
    how relevant a word is to a document in a
    collection of documents."""
    tfidf = models.TfidfModel(bow_corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=12)
    return index, tfidf


def searching_the_articles(index, tfidf, processed_article,
                          query=DEFAULT_QUERY):
    dictionary = corpora.Dictionary(processed_article)
    query_bow = dictionary.doc2bow(query)
    sims = index[tfidf[query_bow]]
    print(f"{sims=}")
    for article_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True):
        return article_number, score

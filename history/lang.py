import collections
from gensim import corpora, models, similarities
from gensim import utils
from gensim.parsing.preprocessing import remove_stopwords, preprocess_documents, preprocess_string

from .scraper import get_theguardian_articles, parse_theguardian_article

article = """the original article or one selected from ???  not quite sure yet """
article_corpus = ["""my thought is this is where the selected texts will end up to be processed"""]

def telegraphic_text_single_article(article):
    """removes stopwords, predefined by Gensim, across the text."""
    filtered_article = remove_stopwords(article)
    return filtered_article

def telegraphic_text_multiple_articles(article_corpus):
    """removes stopwords across multiple texts.... returns dictionaries"""
    post_processed_articles = preprocess_documents(article_corpus)
    return post_processed_articles

def article_analysis(filtered_article):
    """The Natural Language Processing analysis on the articles....
    and returns a dictionary bag-of-words  of each article's keywords"""
    # Creates an additional set of stop words, final check to make sure some words do not get through
    stoplist = set('for a of the and to in but'.split(' '))
    # Lowercase each document, split it by white space and filter out stopwords
    texts = [[word for word in filtered_article.lower().split() if word not in stoplist]
             for article in article_corpus]

    # Counts word frequencies
    frequency = collections.Counter()
    for text in texts:
        for token in text:
            frequency[token] += 1

    # Only keeps words that appear more than once
    processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
    return processed_corpus
    
def selected_article_topical_keywords(processed_corpus):
    stoplist = set('for a of the and to in but'.split(' '))
    dictionary = corpora.Dictionary(processed_corpus)
    # remove stop words and words that appear only once
    stop_ids = [
        dictionary.token2id[stopword]
        for stopword in stoplist
        if stopword in dictionary.token2id
        ]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids)  
    dictionary.compactify()  
    article_keyword_dictionary = dictionary
    return article_keyword_dictionary

def keywords_into_vectors(processed_corpus):
    dictionary = corpora.Dictionary(processed_corpus)
    bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
    return bow_corpus, dictionary

def training_the_model(bow_corpus):
    """TF-IDF is a statistical measure that evaluates how relevant a word is to a document in a collection of documents."""
    tfidf = models.TfidfModel(bow_corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=12)
    return index, tfidf

def searching_the_articles(index, tfidf, processed_corpus):
    dictionary = corpora.Dictionary(processed_corpus)
    query = 'russian economy'.split()
    query_bow = dictionary.doc2bow(query)
    sims = index[tfidf[query_bow]]
    for article_number, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True):
        return article_number, score

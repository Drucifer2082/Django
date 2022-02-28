import sqlite3



def populate_db(db='db.sqlite3'):
    connection = sqlite3.connect(db)
    return connection

   
def isolate_articles(connection):
    with connection:
        cursor = connection.cursor()
        filename = query
        with open(filename, 'r') as f:
            contents = f.read()
 
def articles(request):
    articles = {}
  
    for i in articles:
        article_data = Article(
            name = i['webTitle'],
            category = i['sectionName'],
            slug = i[''],
            link = i['webUrl']
        )
        article_data.save()
        all_articles = Article.objects.all().order_by('-webTitle')

    return render (request, 'news/home.html', { "all_articles": 
    all_articles} )

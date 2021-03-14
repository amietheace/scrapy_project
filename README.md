# target
Using scrapy how to scrape target

There are two spiders in this project. One is using scrapy and other is using requests along with scrapy.
Both of them are able to do the same task but the request one is faster.
One is named as target(the scrapy one) and the other is named as target_new(requests along with scrapy).
steps to run this project
1. Pull the codes from master branch
2. go to the dirctory.
3. for running this the commands are:

    scrapy crawl target -a url=product_url -o "output.json" (for running the first spider)
    
    scrapy crawl target_new -a url=product_url -o "output.json" (for running the second spider)

# Job Spider
### Web crawling &amp; scraping with scrapy: a job finder with MongoDB backend

In this project, I am simply demonstrating how to use scrapy spiders to crawl and scrape web pages.

The use case I chose was a job finder bot which goes and gathers those jobs that match a candidate's criteria.
Prsently, only a single spider is implemented which goes through StackOverflow's job board.   Adding more 
spiders would be a trivial matter.  Just follow the model I show.

The results are stored into a MongoDB, so that is a prerequisite the way it is implemented.  But of course,
changing to a different DB is pretty straightforward

To run the bot as is:

`python run.py`

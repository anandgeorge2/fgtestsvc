# fgtestsvc
Part 1: Stock Ticker
Write a web service that looks up a fixed number of closing prices of a specific stock. 
Guidance:
● In response to a GET request, the service should return the last NDAYS days of data along with the
average closing price over those days. The structure of the response is up to you.
● The stock SYMBOL (the symbol to look up) and NDAYS (the number of days) are environment
variables provided to your program.
● Use this free quote service:
○ Sample query:
https://www.alphavantage.co/query?apikey=C227WD9W3LUVKVV9&function=TIME_SERIES_DAILY&symbol=MSFT
○ Note: You should be able to use the apikey="C227WD9W3LUVKVV9", but you may need to
create your own API key if that one has expired.
○ The API has a quota per key, so you will need to bear this in mind.
● Create a docker image that runs your web service.
● Publish your docker image, your code, and provide instructions on how to build the image and run it.
● Code should exhibit good hygiene. If you are running short of time you can demonstrate intent
without being exhaustive.
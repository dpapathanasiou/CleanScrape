# CleanScrape

## About

This is a no-nonsense [web scraping](https://en.wikipedia.org/wiki/Web_scraping) tool which uses [pycurl](https://pypi.python.org/pypi/pycurl/) to fetch public web page content, [readability-lxml](https://pypi.python.org/pypi/readability-lxml) to clean it of ads, navigation bars, sidebars, and other irrelevant boilerplate, and [wkhtmltopdf](http://wkhtmltopdf.org/) to preserve the output in [PDF](https://en.wikipedia.org/wiki/PDF) document format.

## Motivation

I was getting tired of stale bookmarked links: a lot of useful blog articles disappear and neither [web.archive.org](http://archive.org/web/) nor [Google's cache](http://websearch.about.com/od/focusongoogle/qt/google-cache.htm) are very helpful.

Additionally, too many otherwise-useful pages are cluttered with ads, sidebars, and other crap, so the focus is on preserving text, using the [readability algorithm](http://stackoverflow.com/a/4240037) built into [readability-lxml](https://pypi.python.org/pypi/readability-lxml).

## Installation

You need [python](http://python.org/), [pip](http://www.pip-installer.org/en/latest/installing.html), and [wkhtmltopdf](http://wkhtmltopdf.org/) installed and running on your computer.

Clone this repo to your compter and load the other requirements using the [requirements.txt](requirements.txt) file like so:

```
$ pip install -r requirements.txt
```

Edit the [settings.py](settings.py) file as necessary, to match your computer's environment.

## Usage

Run CleanScrape from a command line prompt, defining the url to fetch and clean, and the pdf file name to use for the final output.

```
$ ./CleanScraper.py "http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/" "strace.pdf"
```

The same, but from inside a python shell:

```
>>> from CleanScraper import scrape
>>> scrape("http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/", "strace.pdf")                                          
```

If successful, the output looks like this, with the final result being saved to <tt>/tmp/strace.pdf</tt> (change the output folder in the [settings.py](settings.py) file in this repo):

```
/usr/local/bin/wkhtmltopdf --page-size Letter /tmp/strace.html /tmp/strace.pdf
Loading pages (1/6)
Counting pages (2/6)                                               
Resolving links (4/6)                                                       
Loading headers and footers (5/6)                                           
Printing pages (6/6)
Done                                                                      
```

Cleaning it with readability is optional; if you want to keep the html retrieved as-is, use the <tt>--noclean</tt> option:

```
$ ./CleanScraper.py "http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/" "strace.pdf" --noclean
```

Or inside the python shell like this:

```
>>> from CleanScraper import scrape
>>> scrape("http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/", "strace.pdf", clean_it=False)                                          
```



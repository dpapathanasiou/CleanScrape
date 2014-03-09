# CleanScrape

## About

This is a no-nonsense [web scraping](https://en.wikipedia.org/wiki/Web_scraping) tool which uses [pycurl](https://pypi.python.org/pypi/pycurl/) to fetch public web page content, [readability-lxml](https://pypi.python.org/pypi/readability-lxml) to clean it of ads, navigation bars, sidebars, and other irrelevant boilerplate, and [wkhtmltopdf](http://wkhtmltopdf.org/) to preserve the output in [PDF](https://en.wikipedia.org/wiki/PDF) and [EPUB](http://en.wikipedia.org/wiki/EPUB) document formats.

## Motivation

I was getting tired of stale bookmarked links: a lot of useful blog articles disappear and neither [web.archive.org](http://archive.org/web/) nor [Google's cache](http://websearch.about.com/od/focusongoogle/qt/google-cache.htm) are very helpful.

Additionally, too many otherwise-useful pages are cluttered with ads, sidebars, and other crap, so the focus is on preserving text, using the [readability algorithm](http://stackoverflow.com/a/4240037) built into [readability-lxml](https://pypi.python.org/pypi/readability-lxml).

## Installation

You need [python](http://python.org/), [pip](http://www.pip-installer.org/en/latest/installing.html), [wkhtmltopdf](http://wkhtmltopdf.org/), and [pandoc](http://johnmacfarlane.net/pandoc/) installed and running on your computer.

Clone this repo to your compter and load the other requirements using the [requirements.txt](requirements.txt) file like so:

```
$ pip install -r requirements.txt
```

Edit the [settings.py](settings.py) file as necessary, to match your computer's environment.

You can also create a <tt>local_settings.py</tt> file which will override anything in [settings.py](settings.py), without affected the code checked in here.

For epub, there is a default [cover image](epub_cover.jpg) and [css file](epub.css) provided in this repo, but you can provide your own by editing the the [settings.py](settings.py) file, or overriding those definitions in a <tt>local_settings.py</tt> file.

## Usage

Run CleanScrape from a command line prompt, defining the url to fetch and clean, and the file name to use for the final output (both the pdf and epub files will have this filename, but with '.pdf' and '.epub' extensions, respectively).

```
$ ./CleanScraper.py "http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/" "strace"
```

The same, but from inside a python shell:

```
>>> from CleanScraper import scrape
>>> scrape("http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/", "strace")                                          
```

If successful, the output looks like this, with the final results being saved to <tt>/tmp/strace.epub</tt> and <tt>/tmp/strace.pdf</tt> for the epub and pdf files respectively:

```
/usr/bin/pandoc -f html -t epub --epub-metadata="/tmp/metadata.xml" -o /tmp/strace.epub --epub-cover-image="epub_cover.jpg" -s --smart --parse-raw /tmp/strace_epub.html 

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
$ ./CleanScraper.py "http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/" "strace" --noclean
```

Or inside the python shell like this:

```
>>> from CleanScraper import scrape
>>> scrape("http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/", "strace", clean_it=False)                                          
```



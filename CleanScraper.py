#!/usr/bin/env python

"""
CleanScraper.py

This module defines a series of functions to fetch html content from
from any publically-available URL, optionally clean it of any ads,
navigation bars, and other irrelevant boilerplate, and convert it 
into a pdf document framed with wide margins, in an easy-to-read 
format.

Edit the associated settings.py file to match your environment.

"""

from readability.readability import Document

import pycurl
from cStringIO import StringIO
from string import Template
import subprocess
import codecs
import sys
import os

from settings import ENCODING, UA, OUTPUT_FOLDER, WKHTMLTOX_PATH, PDF_PAGE_SIZE, HTML_FRAME

PDF_CONVERT_CMD = Template("$wkhtmltox_path/wkhtmltopdf --page-size $page_size $folder/$article_id.html $folder/$article_id.pdf")

def get_url (url, user_agent=UA, referrer=None):
    """Make a GET request of the url using pycurl and return the data
    (which is None if unsuccessful)"""

    data = None
    databuffer = StringIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.CONNECTTIMEOUT, 5)
    curl.setopt(pycurl.TIMEOUT, 8)
    curl.setopt(pycurl.WRITEFUNCTION, databuffer.write)
    curl.setopt(pycurl.COOKIEFILE, '')
    if user_agent:
        curl.setopt(pycurl.USERAGENT, user_agent)
    if referrer is not None:
        curl.setopt(pycurl.REFERER, referrer)
    try:
        curl.perform()
        data = databuffer.getvalue()
    except Exception:
        pass
    curl.close()

    return data

def to_unicode (s, enc=ENCODING):
    """Convert the given string to unicode, using the requested encoding, 
    (unless it's already in unicode), then return it"""

    if isinstance(s, basestring):
        if not isinstance(s, unicode):
            s = unicode(s, enc)
    return s

def generate_pdf (tmp_folder, filename, pdf_page_size):
    """Use wkhtmltopdf to convert the html file at tmp_folder/filename
    into a pdf file, and return the stdout and stderr results"""

    shell_cmd = PDF_CONVERT_CMD.substitute(wkhtmltox_path=WKHTMLTOX_PATH, folder=tmp_folder, article_id=filename, page_size=pdf_page_size)
    proc = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value, stderr_value = proc.communicate()

    print u'\n'.join(filter(None, [shell_cmd, stdout_value, stderr_value]))

def write_html_file (folder, filename, contents):
    """Attempt to write the contents to the filename in the tmp_folder
    as a utf-8 file, and return a boolean on success/fail"""

    result = False

    try:
        f = codecs.open(os.path.join(folder, filename), 'w', ENCODING)
        f.write(contents)
        f.close()
        result = True
    except (OSError, IOError):
        print "Sorry, could not save contents in", os.path.join(folder, filename)

    return result

def scrape (url, pdf_filename, pdf_page_size=PDF_PAGE_SIZE, folder=OUTPUT_FOLDER, clean_it=True):
    """Fetch the html content at url and convert it to a pdf file,
    cleaned by readability and framed in an easy-to-read format if
    clean_it is True"""

    raw_html = get_url(url)
    if raw_html is None:
        print "Sorry, could not read ", url
    else:
        filename_prefix, file_ext = os.path.splitext(pdf_filename)
        if clean_it:
            title   = Document(raw_html).short_title()
            content = Document(raw_html).summary(html_partial=True)
            frame   = HTML_FRAME.substitute(content=to_unicode(content),
                                            url=url,
                                            title=title)
            source  = write_html_file(folder, os.extsep.join([filename_prefix, 'html']), frame)
        else:
            source  = write_html_file(folder, os.extsep.join([filename_prefix, 'html']), raw_html)

        if source:
            generate_pdf (folder, filename_prefix, pdf_page_size)


if __name__ == "__main__":
    """Create a command-line main() entry point"""

    if len(sys.argv) < 3:
        # Define the usage 
        print sys.argv[0], '[URL]', '[PDF filename]', '--noclean (optional: leave the source html found at the URL as-is)'
    else:
        # Do the deed
        clean_html = True
        try:
            if sys.argv[3] == '--noclean':
                clean_html = False
        except IndexError:
            pass

        scrape(sys.argv[1], sys.argv[2], clean_it=clean_html)


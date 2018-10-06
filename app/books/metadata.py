# app/books/metadata.py

import epub_meta
import filetype
import re

from datetime import datetime
from langdetect import detect, DetectorFactory
from PyPDF2 import PdfFileReader


def detect_language(to_detect):
    DetectorFactory.seed = 0
    return detect(to_detect)


def format_publish_date(date, format):
    return datetime.strptime(date, format).strftime('%Y-%m-%d')


def get_pdf_meta_data(path):
    pdf = PdfFileReader(open(path, 'rb'))
    meta = pdf.getDocumentInfo()

    if '/CreationDate' in meta.keys():
        publish_date = format_publish_date(meta['/CreationDate'][2:10],
                                           '%Y%m%d')
    else:
        publish_date = None

    if '/Title' in meta.keys():
        title = meta['/Title']
        language = detect_language(meta['/Title'])
    else:
        title = None
        language = None

    if '/Author' in meta.keys():
        author = meta['/Author']
    else:
        author = None

    return {'authors': author, 'title': title, 'file_type': 'pdf',
            'language': language, 'description': None,
            'publish_date': publish_date}


def get_epub_meta_data(path):
    meta = epub_meta.get_epub_metadata(path)

    # Format authors
    if 'authors' in meta.keys():
        authors = ""
        for i, author in enumerate(meta['authors']):
            if i:
                authors += '; ' + author
            else:
                authors += author
    else:
        authors = None

    # Format Publish Date
    if 'publication_date' in meta.keys():
        try:
            publish_date = format_publish_date(meta['publication_date'][:10],
                                               '%Y-%m-%d')
        except ValueError or AttributeError or TypeError:
            publish_date = None
    else:
        publish_date = None

    # Format description
    if meta['description']:
        cleanr = re.compile('<.*?>')
        description = re.sub(cleanr, '', meta['description'])
        description = description.replace('\n', ' ').replace('\t', ' '). \
            replace('\r', ' ')
        cleanr2 = re.compile(' +')
        description = re.sub(cleanr2, ' ', description)
    else:
        description = None

    # Format language
    if 'language' in meta.keys():
        language = meta['language']
    else:
        if description:
            language = detect_language(description)
        else:
            language = detect_language(meta['title'])

    return {'authors': authors, 'title': meta['title'], 'file_type': 'epub',
            'publish_date': publish_date, 'language': language,
            'description': description}


def get_meta_data(path):
    type = filetype.guess(path).extension

    if type == 'pdf':
        return get_pdf_meta_data(path)
    elif type == 'epub':
        return get_epub_meta_data(path)
    else:
        return None

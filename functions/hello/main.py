# coding: utf-8
from os import path
from logging import getLogger
from jinja2 import Environment, FileSystemLoader
import feedparser
import boto3
import logging

COUNTER_HASH_SIZE = 10

TECH_BLOG_URL = 'https://chroju.github.io/atom.xml'
HOBBY_BLOG_URL = 'http://chroju.hatenablog.jp/feed'
QIITA_URL = 'http://qiita.com/chroju/feed'

BUCKET = 'chroju-profile'
s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
env = Environment(loader=FileSystemLoader(path.join(path.dirname(__file__), 'templates'), encoding='utf8'))

def upload_s3(r):
    key = 'index.html'
    template = env.get_template('index.html.j2')
    body = template.render(techblog=techblog, hobbyblog=hobbyblog, qiita=qiita)
    s3.put_object(Bucket=BUCKET, Key=key, Body=body, ContentType='text/html')

def pick_up_entries(url):
    response = feedparser.parse(url)
    result = []
    for i in range(3):
        logger.info(response.entries[i].title)
        result.append(
            { "url" : response.entries[i].link,
              "title" : response.entries[i].title})
    return result

techblog = pick_up_entries(TECH_BLOG_URL)
hobbyblog = pick_up_entries(HOBBY_BLOG_URL)
qiita = pick_up_entries(QIITA_URL)

def handle(event, context):
    logger.info(event)
    upload_s3(event)


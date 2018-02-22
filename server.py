#!/bin/python

__author__ = "Stefan Safranek"
__copyright__ = "Copyright 2016, The Real Dikshunary"
__credits__ = ["Stefan Safranek"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Stefan Safranek"
__email__ = "https://github.com/sjsafranek"
__status__ = "Development"

import os
import json
import time
import builtins
import Conf
import random
import requests
import tornado.web
import tornado.ioloop
from tornado.log import logging
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

logger = logging.getLogger("tornado.application")

define("p", default=5000, help="server port", type=int)


WORDS = []
with open("words.json", 'r') as f:
	data = json.load(f)
	WORDS = data['words']


class Database(object):

	def __init__(self, db_path):
		self.db_path = db_path
		self.data = {}
		self._get_data()

	def save(self):
		with open(self.db_path, 'w') as f:
			json.dump(self.data, f)

	def _get_data(self):
		try:
			with open(self.db_path, 'r') as f:
				self.data = json.load(f)
		except FileNotFoundError:
			pass

DB = Database(builtins.DATABASE_PATH)


WEBSTERS_FAILURE_MESSAGES = [
	"The word you've entered was not found",
	"The word you've entered isn't in the dictionary",
	"The word you've entered isn't in the thesaurus",
	"Aren’t you smart – you've found a word that is only available in the Merriam-Webster Unabridged Dictionary"
]


# class BaseHandler(tornado.web.RequestHandler):
# 	@tornado.web.asynchronous
#

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.write(
				"The Real Dikshunary <br>" +
				"noun | the·real·dik·shun·ary"
			)

def create_new_word(page, old_word):
	""" create_new_word
		Chooses random word from list and checks Webster for validity
		Args:
			page (str): `dictionary` or `thesaurus`
			old_word (str): user supplied word
	"""
	new_word = random.choice(WORDS)
	res = requests.get(builtins.WEBSTER_URL + "%s/%s" % (page, new_word))
	logger.info(builtins.WEBSTER_URL + "%s/%s" % (page, new_word))
	content = res.text
	for message in WEBSTERS_FAILURE_MESSAGES:
		if message in content:
			content = create_new_word(page, old_word)
	else:
		DB.data[old_word] = new_word
		DB.save()
	return content

def forge_page(word, url):
	""" forge_page
		Requests html source from webster dictionary.
		Replaces instances of random word with user supplied word
		Args:
			word (str): users `word`
			url (str): webster dictionary url
	"""
	res = requests.get(url)
	logger.info(url)
	logger.info({word: DB.data[word]})
	content = res.text
	content = content.replace(DB.data[word], word)
	content = content.replace(DB.data[word].lower(), word.lower())
	content = content.replace(DB.data[word].upper(), word.upper())
	content = content.replace(DB.data[word].title(), word.title())
	return content

class MapHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, word):
		self.set_header("Content-Type", "application/json")
		if word in DB.data:
			self.write({word: DB.data[word]})
		else:
			self.write({word: None})
		self.finish()

class SetHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, new_word, old_word):
		self.set_header("Content-Type", "application/json")
		old_word = old_word.upper()
		if old_word in WORDS:
			DB.data[new_word] = old_word
			DB.save()
			self.write({"status": "ok"})
		else:
			self.write({"error": "{0} does not exist".format(old_word)})
		self.finish()

class DatabaseHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.set_header("Content-Type", "application/json")
		self.write(DB.data)
		self.finish()

class WordsHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.set_header("Content-Type", "application/json")
		self.write({"words": WORDS})
		self.finish()

class DictionaryHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, word):
		if word in DB.data:
			content = forge_page(word, builtins.WEBSTER_URL + "dictionary/%s" % DB.data[word])
			self.write(content)
		else:
			res = requests.get(builtins.WEBSTER_URL + "dictionary/%s" % word)
			content = res.text
			failure_messages = [
				"The word you've entered was not found",
				"The word you've entered isn't in the dictionary."
			]
			for message in failure_messages:
				if message in content:
					content = create_new_word("dictionary", word)
					break
			else:
				DB.data[word] = word
			DB.save()
			content = content.replace(DB.data[word], word)
			logger.info({word: DB.data[word]})
			content = content.replace(DB.data[word], word)
			content = content.replace(DB.data[word].lower(), word.lower())
			content = content.replace(DB.data[word].upper(), word.upper())
			content = content.replace(DB.data[word].title(), word.title())
			self.write(content)
		self.finish()

class ThesaurusHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, word):
		if word in DB.data:
			content = forge_page(word, builtins.WEBSTER_URL + "thesaurus/%s" % DB.data[word])
			self.write(content)
		else:
			res = requests.get(builtins.WEBSTER_URL + "thesaurus/%s" % word)
			content = res.text
			for message in WEBSTERS_FAILURE_MESSAGES:
				if message in content:
					content = create_new_word("thesaurus", word)
					break
			else:
				DB.data[word] = word
			DB.save()
			content = content.replace(DB.data[word], word)
			logger.info(word, DB.data[word])
			content = content.replace(DB.data[word], word)
			content = content.replace(DB.data[word].lower(), word.lower())
			content = content.replace(DB.data[word].upper(), word.upper())
			content = content.replace(DB.data[word].title(), word.title())
			self.write(content)
		self.finish()



# Tornado settings
settings = {
	'static_path': os.path.join(os.getcwd(), 'static'),
	# 'template_path': os.path.join(os.getcwd(), 'templates'),
	'debug': True
}

if __name__ == "__main__":
	parse_command_line()
	application = tornado.web.Application([
		(r"/", MainHandler),
		(r"/db", DatabaseHandler),
		(r"/words", WordsHandler),
		(r"/map/([a-zA-Z]+)", MapHandler),
		(r"/set/([a-zA-Z]+)/([a-zA-Z]+)", SetHandler),
		(r"/dictionary/([a-zA-Z]+)",DictionaryHandler),
		(r"/thesaurus/([a-zA-Z]+)", ThesaurusHandler),
	], **settings)
	application.listen(options.p)
	logger.info("Running on http://localhost:" + str(options.p))
	tornado.ioloop.IOLoop.current().start()

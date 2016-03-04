#!/bin/python
import os
import json
import time
import random
import requests
import tornado.web
import tornado.ioloop
from tornado.log import logging
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

app_log = logging.getLogger("tornado.application")

define("p", default=5000, help="server port", type=int)

WORDS = []
db = {}
db_file = 'db.json'

WEBSTER_URL = "http://www.merriam-webster.com/"

def save_database():
	with open(db_file, 'w') as f:
		json.dump(db, f)

def get_database():
	try:
		with open(db_file, 'r') as f:
			data = json.load(f)
		return data
	except FileNotFoundError:
		return {}

def getWords():
	data = {}
	with open("words.json", 'r') as f:
		data = json.load(f)
	return data['words']



class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")


def create_new_word(page, old_word):
	# new_word = words[random.randint(0,len(words))].lower()
	new_word = random.choice(WORDS)
	# while "ly" == new_word[len(new_word)-2: len(new_word)-1]:
		# new_word = words[random.randint(0,len(words))].lower()
	res = requests.get(WEBSTER_URL + "%s/%s" % (page, new_word))
	app_log.info(WEBSTER_URL + "%s/%s" % (page, new_word))
	content = res.text
	failure_messages = [
			"The word you've entered was not found",
			"The word you've entered isn't in the dictionary",
			"The word you've entered isn't in the thesaurus",
			"Aren’t you smart – you've found a word that is only available in the Merriam-Webster Unabridged Dictionary."
	]
	for message in failure_messages:
		if message in content:
			content = create_new_word(page, old_word)
	else:
		db[old_word] = new_word
		save_database()
	return content

# def rewrite_page():

class MapHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, word):
		self.set_header("Content-Type", "application/json")
		if word in db:
			self.write({word: db[word]})
		else:
			self.write({word: None})
		self.finish()

class DictionaryHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, word):
		# self.set_header("Content-Type", "application/json")
		if word in db:
			res = requests.get(WEBSTER_URL + "dictionary/%s" % db[word])
			app_log.info(WEBSTER_URL + "dictionary/%s" % db[word])
			content = res.text
			app_log.info({word: db[word]})
			content = content.replace(db[word], word)
			content = content.replace(db[word].lower(), word.lower())
			content = content.replace(db[word].upper(), word.upper())
			content = content.replace(db[word].title(), word.title())
			self.write(content)
		else:
			res = requests.get(WEBSTER_URL + "dictionary/%s" % word)
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
				db[word] = word
			save_database()
			content = content.replace(db[word], word)
			app_log.info({word: db[word]})
			content = content.replace(db[word], word)
			content = content.replace(db[word].lower(), word.lower())
			content = content.replace(db[word].upper(), word.upper())
			content = content.replace(db[word].title(), word.title())
			self.write(content)
		self.finish()


class ThesaurusHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, word):
		# self.set_header("Content-Type", "application/json")
		if word in db:
			res = requests.get(WEBSTER_URL + "thesaurus/%s" % db[word])
			app_log.info(WEBSTER_URL + "thesaurus/%s" % db[word])
			content = res.text
			app_log.info(word, db[word])
			content = content.replace(db[word], word)
			content = content.replace(db[word].lower(), word.lower())
			content = content.replace(db[word].upper(), word.upper())
			content = content.replace(db[word].title(), word.title())
			self.write(content)
		else:
			res = requests.get(WEBSTER_URL + "thesaurus/%s" % word)
			content = res.text
			failure_messages = [
				"The word you've entered was not found",
				"The word you've entered isn't in the thesaurus."
			]
			for message in failure_messages:
				if message in content:
					content = create_new_word("thesaurus", word)
					break
			else:
				db[word] = word
			save_database()
			content = content.replace(db[word], word)
			app_log.info(word, db[word])
			content = content.replace(db[word], word)
			content = content.replace(db[word].lower(), word.lower())
			content = content.replace(db[word].upper(), word.upper())
			content = content.replace(db[word].title(), word.title())
			self.write(content)
		self.finish()


# Tornado settings
settings = {
	'static_path': os.path.join(os.getcwd(), 'static'),
	'template_path': os.path.join(os.getcwd(), 'templates'),
	'debug': True
}

if __name__ == "__main__":
	parse_command_line() 
	WORDS = getWords()
	db = get_database()
	application = tornado.web.Application([
		(r"/", MainHandler),
		(r"/map/([a-zA-Z]+)", MapHandler),
		(r"/dictionary/([a-zA-Z]+)",DictionaryHandler),
		(r"/thesaurus/([a-zA-Z]+)", ThesaurusHandler),
	], **settings)
	application.listen(options.p)
	app_log.info("Running on http://localhost:" + str(options.p))
	# print("Magic happens on port %s..." % options.p)
	tornado.ioloop.IOLoop.current().start()


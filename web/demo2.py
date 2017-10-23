#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import pymongo

define("port", default=8083, help="run on the given port", type=int)
blogs = []

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/edit/([0-9Xx\-]+)", EditHandler),
			(r"/add", EditHandler),
			(r"/delete/([0-9Xx\-]+)", DelHandler),
			(r"/blog/([0-9Xx\-]+)", BlogHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			)
		#conn = pymongo.MongoClient("localhost", 27017)
		#self.db = conn["demo2"]
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		import time
		#coll = self.application.db.blog
		#blogs = coll.find().sort("id",pymongo.DESCENDING)
		self.render(
			"index.html",
			#blogs = blogs,
			time = time,
		)

class EditHandler(tornado.web.RequestHandler):
	def get(self, id=None):
		blog = dict()
		#if id:
			#coll = self.application.db.blog
			#blog = coll.find_one({"id": int(id)})
		self.render("edit.html",
			blog = blog
			)

	def post(self, id=None):
		import time
		#coll = self.application.db.blog
		blog = dict()
		#if id:
			#blog = coll.find_one({"id": int(id)})
		blog['deviceId'] = self.get_argument("deviceId", None)
		#blog['action'] = self.get_argument("action", None)
		blog['message'] = self.get_argument("message", None)
		blogs.append(blog)	
		self.redirect("/")

class DelHandler(tornado.web.RequestHandler):
	def get(self, id=None):
		self.render("/")
        

class BlogHandler(tornado.web.RequestHandler):
	def get(self, id=None):
		import time
		#coll = self.application.db.blog
		if id:
			#blog = coll.find_one({"id": int(id)})
			self.render("blog.html",
				page_title = "我的博客",
				#blog = blog,
				time = time,
				)
		else:
			self.redirect("/",)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    try:        
        #http_server = tornado.httpserver.HTTPServer()
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        http_server.stop()
    


if __name__ == "__main__":
	main()

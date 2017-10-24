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

import sys
import os
import inspect

cmd_subfolder = os.path.realpath(
    os.path.abspath(
        os.path.join(
            os.path.split(
                inspect.getfile(inspect.currentframe())
            )[0],
            "..",
            "tests"
        )
    )
)
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import test_iot as mqtt


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
			blogs = blogs,
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
		blog['testTimes'] = self.get_argument("testTimes", None)
		mqtt.connet_mqtt_server('192.168.202.172')
		mqtt.publish_topic(3, ['66-55-44-33-22-13'], 'config_info', 1, blog['message'])
		blogs.append(blog)
		print blogs
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
				#time = time,
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

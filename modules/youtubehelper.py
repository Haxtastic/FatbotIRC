# encoding: UTF-8

import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import gdata.youtube
import gdata.youtube.service
import re
import ConfigParser
from urlparse import urlparse, parse_qs
import urllib2 as urllib
from bs4 import BeautifulSoup
from weakboundmethod import WeakBoundMethod as Wbm

class youtubehelper():
	def __init__(self, ed):
		self.ed = ed
		self.read_config()
		self.client = gdata.youtube.service.YouTubeService()
		self.client.ssl = True
		self.started = False
		self._connections = [
			self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg)),
			self.ed.add(ReloadconfigEvent, Wbm(self.reload_config))
		]
		
	def reload_config(self, event):
		if event.module == "youtubehelper" or event.module == "all":
			self.read_config()
		
	def parse_privmsg(self, event):
		if self.started == False:
			return
		message = event.message
		urls = re.findall(r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""", message)
		#urls = match_urls.match(message)#re.findall('(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
		if not urls:
			return
		for urlT in urls:
			if urlT[0].startswith("http") == False:
				url = "http://" + urlT[0]
			else:
				url = urlT[0]
			print url
			videoid = self.video_id(url)
			if videoid is None:
				#get title of site
				try:
					soup = BeautifulSoup(urllib.urlopen(url))
					if hasattr(soup.title, "title"):
						title = self.title % (soup.title.string.encode("utf-8").strip())
					else:
						title = self.title % (url)
				except urllib.URLError:
					title = "Title Error: Invalid url or request timeout."
			else:
				try:
					#get stats of video
					video = self.client.GetYouTubeVideoEntry(video_id=videoid)
					title =  self.youtubetitle % (video.media.title.text, video.statistics.view_count, video.rating.average)
				except gdata.service.RequestError:
					title = "YouTube Error: Invalid video id"
			self.ed.post(SendPrivmsgEvent(event.channel, title))
		"""
			if url.find("youtube.com/watch") != -1:
				url_data = urlparse.urlparse(url)
				query = urlparse.parse_qs(url_data.query)
				videoid = query["v"][0]
				try:
					video = self.client.GetYouTubeVideoEntry(video_id=videoid)
					title =  self.title % (video.media.title.text, video.statistics.view_count, video.rating.average)
				except gdata.service.RequestError:
					title = "YouTube Error: Invalid video_id"
				self.evManager.post(SendPrivmsgEvent(event.channel, title))
		"""
		
	def video_id(self, value):
		"""
		Examples:
		- http://youtu.be/SA2iWivDJiE
		- http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
		- http://www.youtube.com/embed/SA2iWivDJiE
		- http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
		"""
		query = urlparse(value)
		if query.hostname == 'youtu.be':
			return query.path[1:]
		if query.hostname in ('www.youtube.com', 'youtube.com'):
			if query.path == '/watch':
				p = parse_qs(query.query)
				return p['v'][0]
			if query.path[:7] == '/embed/':
				return query.path.split('/')[2]
			if query.path[:3] == '/v/':
				return query.path.split('/')[2]
		# fail?
		return None
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.title 			= self.config.get("youtubehelper", "titlemessage").decode("string_escape").encode("utf-8")
		#self.title 			= self.title.replace("\\x02", "\x02").replace("\\x03", "\x03").replace("\\x17", "\x17")
		self.youtubetitle 	= self.config.get("youtubehelper", "youtubemessage").decode("string_escape").encode("utf-8")
		#self.youtubetitle 	= self.youtubetitle.replace("\\x02", "\x02").replace("\\x03", "\x03").replace("\\x17", "\x17")
			
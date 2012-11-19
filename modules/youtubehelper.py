import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import gdata.youtube
import gdata.youtube.service
import urlparse
import re
import ConfigParser

class youtubeHelper():
	def __init__(self, evManager):
		self.evManager = evManager
		self.read_config()
		self.client = gdata.youtube.service.YouTubeService()
		self.client.ssl = True
		self.started = False
		self.evManager.register_listener(self)
		
	def parse_privmsg(self, event):
		if self.started == False:
			return
		message = event.message
		urls = re.findall('(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
		for url in urls:
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
				
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.parse_privmsg(event)
		elif isinstance(event, ReloadconfigEvent):
			if event.module == "youtubehelper" or event.module == "all":
				self.read_config()
		elif isinstance(event, WelcomeEvent):
			self.started = True
			
	def read_config(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'modules.cfg'))
		self.title = self.config.get("youtubehelper", "titlemessage")
		self.title = self.title.replace("\\x02", "\x02").replace("\\x03", "\x03").replace("\\x17", "\x17")
			
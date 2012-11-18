import os, sys
lib_path = os.path.abspath(os.path.join("..", "core"))
sys.path.append(lib_path)
from events import *
import gdata.youtube
import gdata.youtube.service
import urlparse
import re

class youtubeHelper():
	def __init__(self, evManager):
		self.evManager = evManager
		self.evManager.register_listener(self)
		self.client = gdata.youtube.service.YouTubeService()
		self.client.ssl = True
		
	def parse_privmsg(self, event):
		message = event.message
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
		for url in urls:
			if url.find("youtube.com/watch") != -1:
				url_data = urlparse.urlparse(url)
				query = urlparse.parse_qs(url_data.query)
				videoid = query["v"][0]
				video = self.client.GetYouTubeVideoEntry(video_id=videoid)
				title = "YouTube Title: %s | Viewed: %s times | Rating: %s" % (video.media.title.text, video.statistics.view_count, video.rating.average)
				self.evManager.post(SendPrivmsgEvent(event.channel, title))
				
	def notify(self, event):
		if isinstance(event, PrivmsgEvent):
			self.parse_privmsg(event)
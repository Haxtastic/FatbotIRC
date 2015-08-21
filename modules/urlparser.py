"""
Copyright 2014 Magnus Briden

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# encoding: UTF-8
import os, sys, gdata.youtube, gdata.youtube.service, datetime, re, urllib2 as urllib
from core.events import *
from urlparse import urlparse, parse_qs
from bs4 import BeautifulSoup
from core.weakboundmethod import WeakBoundMethod as Wbm
import os, sys
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)
from botinfo import bot_info

class urlparser():
    def __init__(self, ed):
        self.ed = ed
        self.read_config()
        self.regex = re.compile(self.pattern)
        self.client = gdata.youtube.service.YouTubeService()
        self.client.ssl = True
        self._connections = [
            self.ed.add(PrivmsgEvent, Wbm(self.parse_privmsg)),
            self.ed.add(ReloadconfigEvent, Wbm(self.reload_config))
        ]
        
    def reload_config(self, event):
        if event.module == "urlparser" or event.module == "all":
            self.read_config()
        
    def parse_privmsg(self, event):
        message = event.data
        urls = self.regex.findall(message)
        for url in urls:
            if url[0].startswith("http") == False:
                url = "http://" + url[0]
            else:
                url = url[0]
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
                    title =  self.youtube % (video.media.title.text, video.statistics.view_count, video.rating.average, str(datetime.timedelta(seconds=int(video.media.duration.seconds))))
                except gdata.service.RequestError:
                    title = "YouTube Error: Invalid video id"
            if event.dest[0] != '#' and "!" in event.source:
                event.dest = event.source.split("!")[0]
            RequestSendPrivmsgEvent(event.dest, title).post(self.ed)
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
        config              = bot_info["urlparser"];
        self.title          = config["title"].decode("string_escape").encode("utf-8")
        self.youtube        = config["youtube"].decode("string_escape").encode("utf-8")
        self.pattern        = config["regex"]
            
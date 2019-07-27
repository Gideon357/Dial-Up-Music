import os
import shutil
import pafy
import asyncio

class Song:
    def __init__(self, author, channel, song):
        self.requester = author
        self.channel = channel
        self.song = song

class MusicPlayer:
    def __init__(self):
        self.songFileUrls = []

    async def addSongs(self, url, name):
        try:
            self.get_song_file_urls(url, name)
        except:
            print('Failed to preload songs: ' + str(name), file=sys.stderr)

    def get_song_file_urls(self, url, name):
        video = pafy.get_playlist(url)
        for v in video:
            self.songFileUrls.append(v.audiostreams[0].url_https)
# coding:utf-8
from pytube import YouTube
from pytube import Playlist
pl = Playlist("https://www.youtube.com/watch?v=H2WYnKGE0Us&list=PLGNVlSJ5fH_Uy53mmPc7wyxgAthLnMNrZ")
lists = pl.parse_links()
for list in lists[119:]:
    YouTube('http://youtube.com'+list).streams.first().download()
#pl.download_all()
# or if you want to download in a specific directory
#pl.download_all('/mp4/')

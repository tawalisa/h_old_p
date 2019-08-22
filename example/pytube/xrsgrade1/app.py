from pytube import Playlist
from pytube import YouTube
pl = Playlist("https://www.youtube.com/watch?v=cOTNpC_QdQI&list=PL0aO77tKg1k51iInSO3PFzLqQg2-0FdFT&index=2")
#pl.download_all()
lists = pl.parse_links()
print(len(lists))
for list in lists[164:]:
    YouTube('http://youtube.com'+list).streams.first().download()



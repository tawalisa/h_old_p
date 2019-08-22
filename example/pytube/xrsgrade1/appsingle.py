from pytube import YouTube

url = 'https://www.youtube.com/watch?v=2TaSU4Q3Fag&list=PL0aO77tKg1k51iInSO3PFzLqQg2-0FdFT&index=120'
#YouTube(url).streams.download()
yt = YouTube(url)
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

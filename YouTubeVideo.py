# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 13:32:22 2022

@author: Tori
"""
from __future__ import unicode_literals
import youtube_dl

files = [r"https://www.youtube.com/watch?v=JrBdYmStZJ4"]

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    #'format': 'bestvideo/best,bestaudio',
    # 'quiet': 'True',
    'keepvideo': 'True',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for file in files:
        ydl.download([file])
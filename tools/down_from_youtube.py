

# from pytube import YouTube
# yt = YouTube('https://www.youtube.com/watch?v=4t_kCOFozrA')
# yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()

import pytube
link = "https://www.youtube.com/watch?v=4t_kCOFozrA"
SAVE_PATH = "E:/"
yt = pytube.YouTube(link)
stream = yt.streams.first()
stream.download(SAVE_PATH)

# from pytube import YouTube
#
# # where to save
# SAVE_PATH = "E:/"  # to_do
#
# # link of the video to be downloaded
# link = ["https://www.youtube.com/watch?v=4t_kCOFozrA",
#         ]
#
# for i in link:
#     try:
#
#         # object creation using YouTube
#         # which was imported in the beginning
#         yt = YouTube(i)
#     except:
#
#         # to handle exception
#         print("Connection Error")
#
#         # filters out all the files with "mp4" extension
#     mp4files = yt.filter('mp4')
#
#     # get the video with the extension and
#     # resolution passed in the get() function
#     d_video = yt.get(mp4files[-1].extension, mp4files[-1].resolution)
#     try:
#         # downloading the video
#         d_video.download(SAVE_PATH)
#     except:
#         print("Some Error!")
print('Task Completed!')
import feedparser
import requests
import cv2
import numpy as np
import math 
import matplotlib.pyplot as plt
import argparse
import io
import urllib.request
from PIL import Image
import tempfile

cat_cascade = cv2.CascadeClassifier("haarcascade_frontalcatface_extended.xml")

rdf_url = "https://www.youtube.com/feeds/videos.xml?channel_id=取得したいチャンネルのID"
document = feedparser.parse(rdf_url)

def imread_web(url):
    res = requests.get(url)
    img = None
    with tempfile.NamedTemporaryFile(dir='./') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img

def lineNotify(message, *args):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    line_notify_token = '自分のlineトークン'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    if len(args) == 0:
        requests.post(line_notify_api, data=payload, headers=headers)
    else:
        files = {"imageFile": open(args[0], "rb")}
        requests.post(line_notify_api, data=payload, headers=headers, files=files)

send_list = []

for entry in document.entries:
  img = imread_web(entry["media_thumbnail"][0]["url"])

  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  cat_list = cat_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

  for (x, y, w, h) in cat_list:
    color = (0, 0, 225) #BGR
    pen_w = 2
    cv2.rectangle(img, (x, y), (x+w, y+h), color, thickness = pen_w)

  if len(cat_list) != 0:
    cv2.imwrite("cat_out.jpg", img)
    send_img = "cat_out.jpg"
    send_list.append(send_img)
  
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show("send_img")

    image_url = send_img
    text = "pythonからのメッセージ"
    lineNotify(text, image_url)

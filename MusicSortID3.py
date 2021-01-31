"""
Usage
argv[1] = sorce(fullpath)
*optional
*argv[2] = newFolder(fullpath)
"""

import os
import subprocess
import sys
import shutil
from time import time
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from PIL import Image

args = sys.argv
sorce = args[1]
if len(args) == 3:
    newFolder = args[2]
else:
    newFolder = f"{sorce}_edited"
newFolder = newFolder.replace("/", "\\")
musicExp = [".mp3", ".MP3", ".mp4", ".MP4", ".wave", ".wav", ".m4a", ".flac", ".aif", ".aiff", ".aac", ".wma"]
escSequences = {"\"": "\'", ":": "-", "/": "_", "<": "_", ">": "_", "*": "_", "\\": "_", "?": "", "|": "-"}
is_cover = False
dst = ""

timeStart = time()


def escSequencesFix(artist, album, title):
    for befor, after in escSequences.items():
        if befor in (list(title) + list(artist) + list(album)):
            artist = artist.replace(f'{befor}', f'{after}')
            album = album.replace(f'{befor}', f'{after}')
            title = title.replace(f'{befor}', f'{after}')
    return artist, album, title


os.chdir(sorce)
for root, dirs, files in os.walk(os.getcwd()):
    # print(files, "\n")
    for fname in files:
        ftitle, exp = os.path.splitext(fname)
        src = os.path.join(root, fname)
        src = src.replace("/", "\\")

        if fname == "cover.jpg" or fname =="cover.png":
            if fname == "cover.png":
                dir, _ = os.path.split(src)
                pil_img = Image.open(src, 'r')
                pil_img.save(os.path.join(dir, "cover.jpg"), 'JPEG')
            if dst:
                dir, _ = os.path.split(src)
                shutil.copy(os.path.join(dir, "cover.jpg"), dst)
                print("cover.jpgをコピーしました。")
            else:
                is_cover = True


        if exp in musicExp:
            try:
                if exp == ".m4a":
                    raise Exception("m4aは使えません。MP3に変換して下さい。")
                if exp == ".flac":
                    tags = FLAC(src)
                    artist = tags["artist"][0]
                    album = tags["album"][0]
                    title = tags["title"][0]
                else:
                    tags = EasyID3(src)
                    artist = tags["artist"][0]
                    album = tags["album"][0]
                    title = tags["title"][0]
                if ftitle != f"{artist} - {album} - {title}":
                    artist, album, title = escSequencesFix(artist, album, title)
                    dir, _ = os.path.split(src)
                    ftitle = f"{artist} - {album} - {title}"
                    os.rename(src, os.path.join(dir, f"{ftitle}{exp}"))
                    src = os.path.join(dir, f"{ftitle}{exp}")

                dst = os.path.join(newFolder, artist, album)
                os.makedirs(dst, exist_ok=True)

                if os.path.exists(os.path.join(dst, f"{ftitle}{exp}")):
                    print(f"{title}は既に存在しています。")
                else:
                    shutil.copy(src, dst)
                    print(f"{title}をコピーしました。")

                if is_cover:
                    dir, _ = os.path.split(src)
                    shutil.copy(os.path.join(dir, "cover.jpg"), dst)
                    print("cover.jpgをコピーしました。")
                    is_cover = False

            except (IndexError, FileNotFoundError) as e:
                print(f"{src}でエラーが発生しました")
                print("フォルダ名が長すぎるとエラーが発生します")
                print(f"{e}")
                print("Continue? y/n")
                while True:
                    inp = input()
                    if inp == "y":
                        break
                    elif inp == "n":
                        quit()

print(time() - timeStart)

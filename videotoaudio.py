import speech_recognition as sr
import moviepy.editor as mp
from pytube import YouTube
import os
import subprocess
from multiprocessing import Process




def video_to_audio(vid_path,dest_path):
    video = mp.VideoFileClip(vid_path)
    video.audio.write_audiofile(dest_path)
    video.close()

def you_to_video(url):
    YouTube(url).streams.get_by_resolution("720p").download()
    
def you_to_audio(url):
    os.chdir(r"/home/soumyachatterjee/Desktop/INFRAMIND/PROJECT/uploads/")
    for i in os.listdir():
        os.remove(i)
    
    mp4 = YouTube(url).streams.get_highest_resolution().download()
    mp3 = mp4.split(".mp4",1)[0] +".mp3"
    video_to_audio(mp4,mp3)
    os.remove(mp4)
    return os.path.join("/home/soumyachatterjee/Desktop/INFRAMIND/PROJECT/uploads/",mp3)    
    
def spliter_audio_text(path,fname):
    os.chdir(r"/home/soumyachatterjee/Desktop/INFRAMIND/PROJECT/uploads/")
    for i in os.listdir():
        if i == fname:
            continue
        else:
            os.remove(i)
    
    command = "ffmpeg -i "+path+" -f segment -segment_time 30 -c copy %03d.wav"
    subprocess.call(command,shell=True)
    files = []
    for filename in os.listdir('.'):
        if len(filename)==7:
            files.append(filename)
    files.sort()
    print(files)
    count = 0
    txt = [] 
    for filename in files:
        with open(filename,'rb') as fp:
            r = sr.Recognizer()
            audio = sr.AudioFile(fp)
            with audio as source:
                audio_file = r.record(source)
        try:
            result = r.recognize_google(audio_file)
            txt.append(result)
            count += 1
            print(count)
            os.remove(filename)

        except:
            count += 1
            print("error ")
            os.remove(filename)
            continue

    res = path[:-3]+"txt"
    with open(res,"a") as fp:
        fp.writelines(txt)
    
    return os.path.join("/home/soumyachatterjee/Desktop/INFRAMIND/PROJECT/uploads/",res)
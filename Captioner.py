# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 15:16:44 2022

@author: Tori
"""
import cv2
import speech_recognition as sr
from pydub import AudioSegment
import ffmpeg


# Opens video file and sets variables for video 
file_folder = r"C:\Users\Tori\Documents\InstaCaption"
video_file = file_folder + r"\Agent Smith Interrogation-JrBdYmStZJ4.mp4"
wav_file = file_folder + r"\Agent Smith Interrogation-JrBdYmStZJ4.wav"
captioned_video = file_folder + r"\output.avi"
final_combined_video = file_folder + r"\final.avi"
cap = cv2.VideoCapture(video_file)
frames_per_second = cap.get(cv2.CAP_PROP_FPS)
frame_count = 0

print(frames_per_second)

if (cap.isOpened()== False): 
    print("Error opening video stream or file")
    
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
output_file = cv2.VideoWriter(captioned_video,cv2.VideoWriter_fourcc('M','J','P','G'), frames_per_second, (frame_width,frame_height))

# Opens wav file and sets variables for audio
r = sr.Recognizer()

audio = sr.AudioFile(wav_file)  #the audio component of the wav file
file = AudioSegment.from_file(wav_file)  #used only to calculate file length 
file_duration = (len(file) / 1000.0)  #finds the length of the audio in seconds
clip_size = 10  #the length in seconds of the sub-clip to sample
transcript = []
previous_line = ""
print("\nStarting...")
print("file length: {}s\n".format(file_duration))

# Sticks overlapping sentence parts together
def speech_glue(first_line, second_line, start, stop): 
    array_one = first_line.split(" ")
    print("array one: {}".format(array_one))
    array_two = second_line.split(" ")
    print("array two: {}".format(array_two))
    matched = False
    offset = 0
    while matched == False:
        for i in range(offset, len(array_two)-1):
            for j in range(len(array_one)-1, offset, -1):
                if array_one[j] == array_two[i]:
                    matched = True
                    print(array_one[j])
                    print("i: {}, j: {}".format(i,j))
                    crop_one = j
                    crop_two = i
                    combined = " ".join(array_one[0:crop_one] + array_two[crop_two:len(array_two)])
                    print("\ncombined: {}".format(combined))
                    return combined
        matched = True
        print("no overlap")
        combined = " ".join(array_one + array_two)
    #moved to loop - combined = " ".join(array_one[0:crop_one] + array_two[crop_two:len(array_two)])
    #moved to loop - print(combined)
    return combined

def screen_text(text, frame):
    # sets parameters for text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_black = (0,0,0)
    font_white = (255,255,255)
    font_thickness = 2

    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
    screen_width, screen_height = frame.shape[1], frame.shape[0]
    
    if text_width < (screen_width * 0.9):   
        # writes the text to the screen twice, first to add shadow
        position = ((int) ((screen_width/2) - (text_width/2)), (int) (screen_height - text_height))
        cv2.putText(frame, text, position, font, font_scale, font_black, font_thickness+4)
        cv2.putText(frame, text, position, font, font_scale, font_white, font_thickness)
    elif text_width < (screen_width*2):
        # splits the text in half by character count
        first_half = text[0:int(len(text)/2)]
        second_half = text[int(len(text)/2):]
        split_text = second_half.split(" ", 1)
        
        # splits based on space, but only from the middle of text
        line_one = first_half + split_text[0]
        line_two = split_text[1] 
        
        # writes the first line of text
        (text_width, text_height), baseline = cv2.getTextSize(line_one, font, font_scale, font_thickness)
        position = ((int) ((screen_width/2) - (text_width/2)), (int) (screen_height - (10+text_height*2)))
        cv2.putText(frame, line_one, position, font, font_scale, font_black, font_thickness+4)
        cv2.putText(frame, line_one, position, font, font_scale, font_white, font_thickness)
        # writes the second line
        (text_width, text_height), baseline = cv2.getTextSize(line_two, font, font_scale, font_thickness)
        position = ((int) ((screen_width/2) - (text_width/2)), (int) (screen_height - text_height))
        cv2.putText(frame, line_two, position, font, font_scale, font_black, font_thickness+4)
        cv2.putText(frame, line_two, position, font, font_scale, font_white, font_thickness)
    else:
        print("caption too long for screen: reduce clip size")
        
    return frame


# Main

# makes a transcript from speech-to-text information in the wav file
for i in range(0, int(file_duration), clip_size):
    # does the speech-to-text work
    with audio as source:
        audio_file = r.record(source,duration=clip_size+4,offset=i)
    try:
        result = r.recognize_google(audio_file)
    except:
        result = ""  #necessary in cases of silence
    
    # takes care of segments with silence
    if previous_line == "":
        print("\nprevious line: {}".format(previous_line))
        previous_line = result
    else: 
        previous_line = speech_glue(previous_line, result, i, i+clip_size) #start and stop useless for now
    
    transcript.append(result)
    
    #print("{}: {}".format(i, result))
    print("\ntranscript: {}".format(transcript))
    
#adds one more item to the transcript in case there's a second or two of no talking at the end
transcript.append(" ")

while(cap.isOpened()):
      
    # capture frames in the video and breaks if no more frames
    ret, frame = cap.read()
    if not ret:
        break  
    frame_count += 1
    seconds = frame_count/frames_per_second
    transcript_counter = int(seconds / clip_size)
    print(transcript_counter)
    print("seconds: {}".format(seconds))
    print("transcript: {}".format(transcript_counter))
    frame = screen_text((transcript[transcript_counter]), frame)

        
    # Display the resulting frame
    output_file.write(frame)
    #cv2.imshow('video', frame)
  

print("done!")
# release the cap object
cap.release()
# close all windows
cv2.destroyAllWindows()

try:
    input_video = ffmpeg.input(captioned_video)
    input_audio = ffmpeg.input(wav_file)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(final_combined_video).run()
    print("combined video and audio successfully!")
except Exception:
    print("failed to convert")
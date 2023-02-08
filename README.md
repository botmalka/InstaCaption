# InstaCaption

This project was originally written with captioning YouTube videos in mind, but it’s likely small businesses would likely find it useful to be able to easily caption recorded meetings. I started by writing a script that downloads YouTube videos and splits them into mp4 video and wav audio. 

Speech recognition easily turns the entire wav file into a transcript, except it’s designed to stop transcribing when it encounters a long pause. Since we also had to figure out the timing of the words to align with the proper frames for captioning, the two major issues to overcome here were queueing for the captions to start at the right time in the video, as well as the caption overlay process itself. I loaded the audio in overlapping segments to account for words that may be cut off and misheard. A total of 14 seconds of audio at a time, the first 4 seconds being overlap then a 10 second unique segment. 

Future updates will include modifying the text clipping, as well as making it function better for videos with multiple speakers and automatic punctuation

<sub>Images from video, captioned with InstaCaption, original video taken from https://www.youtube.com/watch?v=JrBdYmStZJ4 which was taken from The Matrix, owned by Warner Bros.</sub>

![Caption example 1](https://raw.githubusercontent.com/botmalka/InstaCaption/main/Billions.JPG)

![Caption example 2](https://raw.githubusercontent.com/botmalka/InstaCaption/main/Primitive.JPG)

![Caption example 3](https://raw.githubusercontent.com/botmalka/InstaCaption/main/Dinosaur.JPG)

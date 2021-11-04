# AWS Audio Converter

This audio converter can be used in conjunction with AWS Lamba to convert wav files to mp3 by using ffmpeg

## Usage and modifications

Simply zip the content of this repository and add it to your lambda function. Afterwards you can 
add an S3 action as trigger to the lambda. The lambda will be executed upon the S3 action, convert the wav file to mp3 and upload it to another S3 Bucket.
It is important to give lambda the right permissions for S3.

You can add the output bucket by setting the variable "outputbucket" at the top of the code.

My client wanted to give the uploaded file a specific path and name, something you might don't need and can simply remove from the code.

Additionally, the client wanted to store the wav file next to the mp3 file and remove it from the input S3 bucket. It is up to you if you want the same behaviour.

## library_location.py

This file will allocate the lib folder within this project and use it to convert the audio files with ffmpeg. 
Unfortunately, I couldn't find an other solution to enable lambda to make use of ffmpeg.

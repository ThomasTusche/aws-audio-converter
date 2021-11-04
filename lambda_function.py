import os
import urllib
import boto3
from subprocess import Popen, PIPE
import library_location
# used to find and import the ffmpeg binary file, since ffmpeg can't be used directly with lambda and needs to be imported
library_location.set_path_if_library_not_available('ffmpeg','lib','ffmpeg is required for this library, but was not found')

# set the output bucket
outputbucket = 'audioconverteroutput'

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # read bucketname and key from event data, to determine the file which needs to be converted
    record = event['Records'][0]['s3']
    bucket = record['bucket']['name']
    key = urllib.parse.unquote_plus(record['object']['key'])

    print("Output of the lambda trigger context")
    print(context)
    print("S3 Bucketname:")
    print(bucket)
    print("Wav Filename:")
    print(key)

    # Manipulates the name of the audio file to create an s3 path of it
    splitkey = key.split('_')
    mp3filename = splitkey[0] + '_' + splitkey[1] + '_' + splitkey[2] + '/' + splitkey[3] + '/' + key.replace('.wav','.mp3')
    wavfilename = splitkey[0] + '_' + splitkey[1] + '_' + splitkey[2] + '/' + splitkey[3] + '/' + key

    # read the wav file and stores as bytes
    wav_audio = s3.get_object(Bucket=bucket, Key=key)['Body'].read()

    try:
        mp3_audio = audio_bytes_to_mp3_bytes(wav_audio)
    except Exception as e:
        print("EXCEPTION ---->")
        print(e)
        quit()

    # save new mp3 audio to s3
    s3.put_object(
        Body=mp3_audio,
        Key=mp3filename,
        Bucket=outputbucket,
    )

    # move the wav file next to the new mp3 and deletes it from the old folder
    s3_file = boto3.resource('s3')
    copy_source = {
        'Bucket': bucket,
        'Key': key
    }
    dstbucket = s3_file.Bucket(outputbucket)
    dstbucket.copy(copy_source, wavfilename)

    s3_file.Object(bucket, key).delete()

# function to convert from wav to mp3
def audio_bytes_to_mp3_bytes(audio_bytes):
    ''' convert the wav audio bytes to mp3 audio bytes '''
    process = Popen('ffmpeg -i pipe:0 -ar 32000 -ac 2 -q:a 5 -f mp3 pipe:1'.split(), stdout=PIPE, stdin=PIPE)
    stdout, stderr = process.communicate(input = audio_bytes)
    return stdout
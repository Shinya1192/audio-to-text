import boto3
import datetime
import json
import re
import os
from urllib.parse import unquote_plus


def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))
    
    transcribe = boto3.client('transcribe')
    s3 = boto3.client('s3')
    
    # Input and output bucket names
    input_bucket = os.environ['INPUT_BUCKET']
    output_bucket = os.environ['OUTPUT_BUCKET']
    
    # Get the input audio file from S3
    encoded_key = event['Records'][0]['s3']['object']['key']
    key = unquote_plus(encoded_key)
    audio_file_uri = f's3://{input_bucket}/{key}'
    
    print(f"Audio file URI: {audio_file_uri}")  # Add this line to log the audio file URI
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    transcription_job_name = f'Transcription-{os.path.splitext(key)[0]}-{timestamp}'
    transcription_job_name = re.sub(r'[^0-9a-zA-Z._-]', '_', transcription_job_name)


    # Job configuration
    job_name = transcription_job_name
    language_code = 'ja-JP' # Change this to the language code of your audio file

    # Start the transcription job
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat='mp3',
        Media={
            'MediaFileUri': audio_file_uri
        },
        OutputBucketName=output_bucket
    )

    return {
        'statusCode': 200,
        'body': 'Transcription job started'
    }

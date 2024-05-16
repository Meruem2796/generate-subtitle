import re
import time
import math
import ffmpeg
from faster_whisper import WhisperModel
from googletrans import Translator

input_video = "input.mp4"
input_video_name = input_video.replace(".mp4", "")

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio

def transcribe(audio):
    model = WhisperModel("small")
    segments, info = model.transcribe(audio)
    language = info[0]
    print("Transcription language", info[0])
    segments = list(segments)
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    return language, segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    return formatted_time

def generate_subtitle_file(language, segments):
    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"
        
    with open(subtitle_file, "w", encoding="utf-8") as f:
        f.write(text)

    return subtitle_file

def translate_subtitles(subtitle_file, src_lang='en', dest_lang='yo'):
    translator = Translator()
    with open(subtitle_file, 'r', encoding='utf-8') as file:
        subtitles = file.readlines()

    translated_subtitles = []
    for line in subtitles:
        if re.match(r'^\d{2}:\d{2}:\d{2},\d{3}', line) or line.strip() == '' or line.strip().isdigit():
            translated_subtitles.append(line)
        else:
            translated_line = translator.translate(line, src=src_lang, dest=dest_lang).text
            translated_subtitles.append(translated_line + '\n')

    translated_subtitle_file = subtitle_file.replace(f".{src_lang}.srt", f".{dest_lang}.srt")
    with open(translated_subtitle_file, 'w', encoding='utf-8') as file:
        file.writelines(translated_subtitles)

    return translated_subtitle_file

def add_subtitle_to_video(soft_subtitle, subtitle_file, subtitle_language):
    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = f"output-{input_video_name}.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
               "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        stream = ffmpeg.output(video_input_stream, output_video,
                               vf=f"subtitles={subtitle_file}")
        ffmpeg.run(stream, overwrite_output=True)

def run():
    extracted_audio = extract_audio()
    language, segments = transcribe(audio=extracted_audio)
    subtitle_file = generate_subtitle_file(language=language, segments=segments)
    translated_subtitle_file = translate_subtitles(subtitle_file, src_lang=language, dest_lang='yo')
    add_subtitle_to_video(soft_subtitle=True, subtitle_file=translated_subtitle_file, subtitle_language='yo')

run()

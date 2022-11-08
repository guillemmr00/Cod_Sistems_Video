import os
import ffmpeg



def parse_video():
    probe = ffmpeg.probe('bbb.mp4')
    print('File name: ', probe['format']['filename'])
    print('Format: ', probe['format']['format_name'])
    print('Number of streams: ', probe['format']['nb_streams'])
    for i in range(len(probe['streams'])):
        print(f'\nStream #{i}')
        print(f'    Type of Stream #{i}: ', probe['streams'][i]['codec_type'])
        print(f'    Codec name of Stream #{i}: ', probe['streams'][i]['codec_name'])
        print(f'    Duration Stream #{i}: ', probe['streams'][i]['duration'], 'seconds')


def modify_video():
        os.system("ffmpeg -ss 0 -i bbb.mp4 -c copy -t 60 cut_bbb.mp4")
        os.system("ffmpeg -i cut_bbb.mp4 -q:a 0 -map a cut_bbb.mp3")
        os.system("ffmpeg -i cut_bbb.mp4 -q:a 0 -map a cut_bbb.aac")
        os.system("ffmpeg -i cut_bbb.mp4 -i cut_bbb.mp3 -i cut_bbb.aac -c copy -map 0:v -map 1:a -map 2:a bbb_cont.mp4")

def resize_video():
    input_v = input("Name of the video to resize (should be on the same folder as this script): ")
    width = input("New width of the video: ")
    height = input("New heigth of the video: ")
    os.system(f'ffmpeg -i {input_v} -vf scale={width}:{height} {input_v}_{width}x{height}.mp4')


def broadcasting_formats():
    b_s = {"DVB":["AAC", "AC-3", "MP3"], "ATSC":["AC-3"], "ISDB":["AAC"], "DTMB":["DRA", "AAC", "AC-3", "MP2", "MP3"]}
    input_v = input("Name of the video to get broadcasting options (should be on the same folder as this script): ")
    codecs = os.popen('ffprobe -v error -select_streams a -show_entries'
                       f' stream=codec_name -of default=noprint_wrappers=1:nokey=1 {input_v}').read()
    codecs = codecs.split()
    possible_broad = []
    for codec in codecs:
        for b in list(b_s.items()):
            if codec.upper() in b[1] and b[0] not in possible_broad:
                possible_broad.append(b[0])

    print(f"Input video has {', '.join(codecs)} codecs, "
          f"therefore can be broadcoasted with {', '.join(possible_broad)}.")

def main():
    print("Welcome to Guillem's P2!")
    options = {"Parse video (ex 1)": parse_video, "Modify video streams (ex 2)": modify_video,
               "Resize video (ex 3)": resize_video, "Possible broadcasting formats (ex 4)": broadcasting_formats}
    for idx, i in enumerate(options.keys()):
        print(idx + 1, ") ", i)
    try:
        option = int(input("Which action do you want to perform? (select number): "))
        if option <= len(options):
            list(options.values())[option - 1]()
        else:
            print("\nOption out of range! Try again!\n")
            main()
    except ValueError:
        cont = str(input("Options should be an integer option! Do you want to try again?[y/N]: "))
        if cont.capitalize() == ("Y" or "YES"):
            main()
        else:
            return


main()

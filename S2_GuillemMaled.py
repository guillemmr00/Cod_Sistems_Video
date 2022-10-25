import os


def cut_video():
    seconds_2_cut = input("How many seconds would you like to cut?: ")
    input_file = "bbb.mp4"
    os.system(f"ffmpeg -ss {seconds_2_cut} -i {input_file} -c copy -t 10000000 cut2_bbb.mp4")


def histogram_video():
    os.system('ffmpeg -i bbb.mp4 -filter_complex "split=2[a][b];'
              '[a]pad=width=in_w+100:height=in_h:x=0:y=0:color=black[a];'
              '[b]histogram=display_mode=stack,scale=100:240,format=yuva444p[c];'
              '[a][c]overlay=x=416:y=0" bbb_with_hist.mp4')


def resize_video():
    size_options = {"720p": "1280:720", "480p": "640:480", "360x240": "360:240", "160x120": "160:120"}
    for idx, i in enumerate(size_options):
        print(idx+1, ") ", i)
    try:
        size = int(input("Which resize option do you want?: "))
        if size <= len(size_options):
            os.system(f'ffmpeg -i bbb.mp4 -vf scale={list(size_options.values())[size-1]}'
                      f' bbb_resize_{list(size_options.keys())[size-1]}.avi')
        else:
            print("Option out of range! Try again!")
            resize_video()
    except ValueError:
        cont = str(input("Options should be an integer option! Do you want to resize again?[y/N]: "))
        if cont.capitalize() == ("Y" or "YES"):
            resize_video()
        else:
            return


def audio_channels():
    x = int(os.popen(' ffprobe -i bbb.mp4 -show_entries stream=channels'
                     ' -select_streams a:0 -of compact=p=0:nk=1 -v 0').read())
    if x == 2:
        print("Converting stereo file to mono!")
        os.system('ffmpeg -i bbb.mp4 -ac 1 bbb_mono.mp4')
    if x == 1:
        print("Converting mono file to stereo!")
        os.system('ffmpeg -i bbb_mono.mp4 -ac 2 bbb_stereo.mp4')
    else:
        print("Our program only supports files with 1 or 2 audio channels...")


def main():
    print("Welcome to Guillem's S2!")
    options = {"Cut video": cut_video, "Video with histogram": histogram_video,
               "Resize video": resize_video, "Convert audio": audio_channels}
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

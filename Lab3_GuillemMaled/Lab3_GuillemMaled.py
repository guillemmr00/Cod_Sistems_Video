import os
import random
from pathlib import Path
import string


def ex_1():
    input_v = "cut_bbb.mp4 "
    output_f = f"./{Path(input_v).stem}"
    os.system(
        f'ffmpeg -i {input_v} -filter_complex "[0:v]split=3[v1][v2][v3]; [v1]copy[v1out]; [v2]scale=w=1280:h=720[v2out]; [v3]scale=w=640:h=360[v3out]" '
        f'-map [v1out] -c:v:0 libx264 -x264-params "nal-hrd=cbr:force-cfr=1" -b:v:0 5M -maxrate:v:0 5M -minrate:v:0 5M -bufsize:v:0 10M -preset slow -g 48 -sc_threshold 0 -keyint_min 48 '
        f'-map [v2out] -c:v:1 libx264 -x264-params "nal-hrd=cbr:force-cfr=1" -b:v:1 3M -maxrate:v:1 3M -minrate:v:1 3M -bufsize:v:1 3M -preset slow -g 48 -sc_threshold 0 -keyint_min 48 '
        f'-map [v3out] -c:v:2 libx264 -x264-params "nal-hrd=cbr:force-cfr=1" -b:v:2 1M -maxrate:v:2 1M -minrate:v:2 1M -bufsize:v:2 1M -preset slow -g 48 -sc_threshold 0 -keyint_min 48 '
        f'-map a:0 -c:a:0 aac -b:a:0 96k -ac 2 '
        f'-map a:0 -c:a:1 aac -b:a:1 96k -ac 2 '
        f'-map a:0 -c:a:2 aac -b:a:2 48k -ac 2 '
        f'-f hls '
        f'-hls_time 2 '
        f'-hls_playlist_type vod '
        f'-hls_flags independent_segments '
        f'-hls_segment_type mpegts '
        f'-hls_segment_filename {output_f}/stream_%v/data%02d.ts '
        f'-master_pl_name master.m3u8 '
        f'-var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" {output_f}/stream_%v.m3u8')


def ex_2():
    input_v = "cut_bbb.mp4 "
    output_res = f"./{Path(input_v).stem}_res"
    output_frag = f"./{Path(input_v).stem}_frag"
    if not os.path.exists(output_res):
        os.makedirs(output_res)

    if not os.path.exists(output_frag):
        os.makedirs(output_frag)

    resized_v = resize_video(input_v, output_res)

    fragment_v = fragment_video(resized_v, output_frag)

    dash_video(fragment_v)

    decrypt_video('cut_bbb_resize_160x120_frag.mp4')


def ex_3():
    os.system('ffmpeg -i cut_bbb.mp4 -v 0 -vcodec mpeg4 -f mpegts udp://127.0.0.1:23000')
    os.system('ffplay udp://127.0.0.1:23000')   #Should be on different terminal in same computer


def resize_video(input_v, output_path):
    in_v_stem = Path(input_v).stem
    size_options = {"720p": "1280:720", "480p": "640:480", "360x240": "360:240", "160x120": "160:120"}
    output_v = []

    for size in range(0, len(size_options)):
        v_dir = os.path.join(output_path, f'{in_v_stem}_resize_{list(size_options.keys())[size - 1]}.mp4')
        v_dir = v_dir.replace(os.sep, '/')
        """os.system(f'ffmpeg -i {input_v} -vf scale={list(size_options.values())[size - 1]}'
                  f' {v_dir}')"""
        output_v.append(v_dir)

    return output_v


def fragment_video(input_v_array, output_path):
    frag_v = []
    for v in input_v_array:
        v_dir = os.path.join(output_path, f'{Path(v).stem}_frag.mp4')
        v_dir = v_dir.replace(os.sep, '/')
        os.system(f"mp4fragment --fragment-duration 5000 {v} {v_dir}")
        frag_v.append(v_dir)
    return frag_v


def dash_video(input_v_array):
    in_v = ""
    kid, key = random_encriptation()
    for v in input_v_array:
        in_v += v + " "
    res = os.system(f"mp4dash --no-split --use-segment-list --encryption-key={kid}:{key} {in_v}")
    if res == 0:
        with open('./output/encryptation.txt', 'w') as f:
            f.write(f'KID: {kid}\nKey: {key}')


def random_encriptation():
    character_set = string.ascii_lowercase
    nums = "".join(map(str, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    kid = ""
    key = ""
    for i in range(32):
        kid += random.choice(random.choice([character_set, nums]))
        key += random.choice(random.choice([character_set, nums]))
    return kid, key


def decrypt_video(input_v):
    in_v_stem = Path(input_v).stem
    with open('./output/encryptation.txt', 'r') as e:
        lines = e.readlines()
        kid = (lines[0][lines[0].find(': ') + 2:])
        key = (lines[1][lines[1].find(': ') + 2:])
        print(kid, key)
    os.system(f'mp4decrypt --key {kid}:{key} {input_v} {in_v_stem}_dec.mp4')

def main():
    print("Welcome to Guillem's P3!")
    options = {"Exercise 1": ex_1, "Exercise 2": ex_2,
               "Exercise 3": ex_3}
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
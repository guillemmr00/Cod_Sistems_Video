import sys

import os
from pathlib import Path
import tkinter as tk
import tk as tk
import numpy as np
from tkinter import filedialog as fd


def resize_video(window, input_v, output_path, array_sizes):
    in_v_stem = Path(input_v).stem
    size_options = {"720p": "1280:720", "480p": "640:480", "360x240": "360:240", "160x120": "160:120"}

    error_arr = []
    for size in range(0, len(size_options)):
        if array_sizes[size] == 1:
            v_dir = os.path.join(output_path, f'{in_v_stem}_resize_{list(size_options.keys())[size - 1]}.mp4')
            x = os.system(f'ffmpeg -i {input_v} -vf scale={list(size_options.values())[size - 1]}'
                      f' {v_dir}')
            if x != 0:
                error_arr.append(f"Unsuccessful operation for {list(size_options.keys())[size-1]} with error code {x}")

    if error_arr:
        result_win = tk.Toplevel(window)
        result_win.title("Error")
        for i in error_arr:
            error = tk.Label(result_win,text=i, padx= 5, pady=5)
            error.pack()
        exit_btn = tk.Button(result_win, text="Exit", width= 10, command=result_win.destroy)
        exit_btn.pack(padx=5, pady=5)
        result_win.mainloop()
    if array_sizes.any() != 0 and not error_arr:
        result_win = tk.Toplevel(window)
        result_win.title("Success")
        succ = tk.Label(result_win, text="Successful operation!", padx= 5, pady=5)
        succ.pack()
        exit_btn = tk.Button(result_win, text="Exit",
                             width=10, command=lambda: [result_win.destroy(),  window.destroy()])
        exit_btn.pack()
        result_win.mainloop()


def encode_video(window, input_v, output_path):
    in_v_stem = Path(input_v).stem
    encode_options = ['vp8', 'vp9', 'h264', 'av1']
    video_dirs=[]
    error_arr = []
    for enc in encode_options:
        if enc == "vp8":
            v_dir = os.path.join(output_path, f'{in_v_stem}_{enc}.webm')
            x = os.system(f'ffmpeg -i {input_v} -c:v {enc} {v_dir}')
            video_dirs.append(v_dir)
            if x != 0:
                error_arr.append(f"Unsuccessful operation for {enc} with error code {x}")

        else:
            v_dir = os.path.join(output_path, f'{in_v_stem}_{enc}.mp4')
            x = os.system(f'ffmpeg -i {input_v} -c:v {enc} {v_dir}')
            video_dirs.append(v_dir)
            if x != 0:
                error_arr.append(f"Unsuccessful operation for {enc} with error code {x}")
    x = os.system(f"ffmpeg -i {str(video_dirs[0])} -i {str(video_dirs[1])} -i {str(video_dirs[2])} -i {str(video_dirs[3])} "
              f"-filter_complex '[0:v] setpts=PTS-STARTPTS, scale=qvga [a0];[1:v] setpts=PTS-STARTPTS, "
              f"scale=qvga [a1]; [2:v] setpts=PTS-STARTPTS, scale=qvga [a2]; [3:v] setpts=PTS-STARTPTS, scale=qvga [a3];"
              f" [a0][a1][a2][a3]xstack=inputs=4:layout=0_0|0_h0|w0_0|w0_h0[out]'"
              f" -map '[out]' -c:v libx264 -t '30' -f matroska {os.path.join(output_path, f'{in_v_stem}_mosaic.mp4')}")
    if x != 0:
        error_arr.append(f"Unsuccessful operation for mosaic with error code {x}")

    if error_arr:
        result_win = tk.Toplevel(window)
        result_win.title("Error")
        for i in error_arr:
            error = tk.Label(result_win,text=i, padx= 5, pady=5)
            error.pack()
        exit_btn = tk.Button(result_win, text="Exit", width= 10, command=result_win.destroy)
        exit_btn.pack(padx=5, pady=5)
        result_win.mainloop()
    if input_v and output_path and not error_arr :
        result_win = tk.Toplevel(window)
        result_win.title("Success")
        succ = tk.Label(result_win, text="Successful operation!", padx= 5, pady=5)
        succ.pack()
        exit_btn = tk.Button(result_win, text="Exit",
                             width=10, command=lambda: [result_win.destroy(),  window.destroy()])
        exit_btn.pack()
        result_win.mainloop()


def select_file(entry):

    filename = fd.askopenfilename(
        title='Select input file',
        initialdir=os.getcwd())

    set_text(filename, entry)


def select_folder(entry):

    foldername = fd.askdirectory(
        title='Select output path',
        initialdir=os.getcwd(),)

    set_text(foldername, entry)


def set_text(text, entry):
    entry.delete(0,tk.END)
    entry.insert(0,text)
    return


def resize_win(main_win):
    resize_win = tk.Toplevel(main_win)
    resize_win.title('Resize video')

    tk.Label(resize_win, text="Input Video:").grid(row=0, column=0)
    tk.Label(resize_win, text="Output Folder:").grid(row=1, column=0)
    tk.Label(resize_win, text="Resize options:").grid(row=3, column=0)

    # Create the entry objects using master
    input_entry = tk.Entry(resize_win, width=50)
    output_entry = tk.Entry(resize_win, width=50)

    # Pack them using grid
    input_entry.grid(columnspan=4, row=0, column=1)
    output_entry.grid(columnspan=4, row=1, column=1)

    input_btn = tk.Button(resize_win, text="Input file", command=lambda: select_file(input_entry, ))
    input_btn.grid(columnspan=1, row=0, column=6, padx=10, pady=10)

    output_btn = tk.Button(resize_win, text="Output path", command=lambda: select_folder(output_entry))
    output_btn.grid(columnspan=1, row=1, column=6, padx=10, pady=10)

    var1 = tk.IntVar()
    var2 = tk.IntVar()
    var3 = tk.IntVar()
    var4 = tk.IntVar()

    c1 = tk.Checkbutton(resize_win, text='720p', variable=var1, onvalue=1, offvalue=0)
    c2 = tk.Checkbutton(resize_win, text='480p', variable=var2, onvalue=1, offvalue=0)
    c3 = tk.Checkbutton(resize_win, text='360x240', variable=var3, onvalue=1, offvalue=0)
    c4 = tk.Checkbutton(resize_win, text='160x120', variable=var4, onvalue=1, offvalue=0)

    c1.grid(columnspan=1, row=3, column=1)
    c2.grid(columnspan=1, row=3, column=2)
    c3.grid(columnspan=1, row=3, column=3)
    c4.grid(columnspan=1, row=3, column=4)

    empty_row= tk.Label(resize_win, text="")
    empty_row.grid(row=4)


    ok_btn = tk.Button(resize_win,
                       text="Apply",
                       width=8,
                       command=lambda : resize_video(resize_win,
                                                     input_entry.get(),
                                                     output_entry.get(),
                                                     np.array([var1.get(), var2.get(), var3.get(), var4.get()])))
    ok_btn.grid(columnspan=1, row=5, column=2)

    cancel_btn = tk.Button(resize_win, text="Cancel", width=8, command=resize_win.destroy)
    cancel_btn.grid(columnspan=1, row=5, column=3)

    empty_row = tk.Label(resize_win, text="")
    empty_row.grid(row=6)

    # The mainloop
    tk.mainloop()


def encode_win(main_win):
    resize_win = tk.Toplevel(main_win)
    resize_win.title('Encode video')

    tk.Label(resize_win, text="Input Video:").grid(row=0, column=0)
    tk.Label(resize_win, text="Output Folder:").grid(row=1, column=0)

    # Create the entry objects using master
    input_entry = tk.Entry(resize_win, width=50)
    output_entry = tk.Entry(resize_win, width=50)

    # Pack them using grid
    input_entry.grid(columnspan=4, row=0, column=1)
    output_entry.grid(columnspan=4, row=1, column=1)

    input_btn = tk.Button(resize_win, text="Input file", command=lambda: select_file(input_entry, ))
    input_btn.grid(columnspan=1, row=0, column=6, padx=10, pady=10)

    output_btn = tk.Button(resize_win, text="Output path", command=lambda: select_folder(output_entry))
    output_btn.grid(columnspan=1, row=1, column=6, padx=10, pady=10)

    empty_row= tk.Label(resize_win, text="")
    empty_row.grid(row=2)

    ok_btn = tk.Button(resize_win,
                       text="Apply",
                       width=8,
                       command=lambda : encode_video(resize_win,
                                                     input_entry.get(),
                                                     output_entry.get(),
                                                     ))
    ok_btn.grid(columnspan=1, row=3, column=2)

    cancel_btn = tk.Button(resize_win, text="Cancel", width=8, command=resize_win.destroy)
    cancel_btn.grid(columnspan=1, row=3, column=3)

    empty_row = tk.Label(resize_win, text="")
    empty_row.grid(row=6)

    comments1 = tk.Label(resize_win, text="The input video will be encoded to vp8, vp9, h264 and av1")
    comments1.grid(columnspan=4, row=7, column=1)
    comments2 = tk.Label(resize_win, text="The process may take some time... Please be patient!")
    comments2.grid(columnspan=4, row=8, column=1)

    # The mainloop
    tk.mainloop()

if __name__ == "__main__":


    win = tk.Tk()
    win.title("Welcome to Guillem's S3!")

    encode_btn = tk.Button(
        win,
        text="Encode Video!",
        width=25,
        height=5,
        bg="blue",
        fg="yellow",
        command=lambda: encode_win(win)
    )
    encode_btn.grid(row=1, column=0)

    resize_btn = tk.Button(
        win,
        text="Resize Video!",
        width=25,
        height=5,
        bg="blue",
        fg="yellow",
        command=lambda: resize_win(win)
    )
    resize_btn.grid(row=1, column=1)

    label = tk.Label(win, text="What would you like to do?")
    label.grid(columnspan=2, row=0, column=0)
    win.mainloop()
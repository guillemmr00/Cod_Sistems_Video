from rgb_yuv import *
from run_length import *
from dct import *

if __name__ == '__main__':
    # Task 1
    y, u, v = rgb_2_yuv(100, 46, 87)
    print("Task 1\n", y, u, v)

    r, g, b = yuv_2_rgb(y, u, v)
    print(r, g, b)

    # Task 4
    print("\nTask 4\n", run_length_encoder("aaaabceee"))

    # Task 5
    project_dir = os.path.dirname(os.path.abspath(__file__))
    dct, idct = encode_decode_dct_im(os.path.join(project_dir, "lenna.jpg"))

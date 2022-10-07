from scipy.fft import dct, idct
from matplotlib.image import *
import matplotlib.pyplot as plt


# implement 2D DCT
def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')


# implement 2D IDCT
def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.144])


def encode_decode_dct_im(path_to_img):
    """
    Encoding and decoding of an image with 2D dct and 2D IDCT from the scipy.fft library
    Args:
        path_to_img (str): path to the input image

    Returns:
        im_dct (array): DCT content of the input image
        im_inv_dct (array): IDCT of the input image (therefore recovered image)

    """
    im = rgb2gray(imread(path_to_img))
    im_dct = dct2(im)
    im_inv_dct = idct2(im_dct)

    # plot original and reconstructed images with matplotlib.pylab
    plt.gray()
    plt.subplot(211), plt.imshow(im), plt.axis('off'), plt.title('original image', size=20)
    plt.subplot(212), plt.imshow(im_inv_dct), plt.axis('off'), plt.title('reconstructed image (DCT+IDCT)', size=20)
    plt.show()

    return im_dct, im_inv_dct

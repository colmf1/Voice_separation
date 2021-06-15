import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav
from scipy import signal
from scipy.fftpack import fft2, ifft2
from matplotlib.colors import LogNorm

def read_wav(path):
    rate, audio_array = wav.read(path)
    audio_array = np.mean(audio_array, axis=1)
    return audio_array, rate

def stft(audio, freq_res, sample_rate=44100, window='hann'):
    nperseg = 2**(8+freq_res)
    f, t, spectrogram = signal.stft(audio, sample_rate, window=window, nperseg=nperseg, noverlap=.5*nperseg)
    return spectrogram

def ft2d(spectrogram):
    return fft2(abs(spectrogram))


def sep2d(img, k, winx=2, winy=1):
    padded = False
    pad = np.zeros((img.shape[0], 1)) + np.vstack(img[:, -1])
    if img.shape[1] % 2 != 0:
        img = np.append(img, pad, axis=1)
        padded = True
    img_h, img_w = img.shape
    tiled_array = img.reshape(img_h//winy, winy, img_w//winx, winx)
    tiled_array = tiled_array.swapaxes(1,2)
    filt = np.ptp(tiled_array, axis=3) < k * np.std(img)
    mask = np.stack((filt, filt), -1)
    A = mask*tiled_array
    bg = A.reshape((img_h, img_w))
    if padded == True:
        bg = np.delete(bg, -1, axis=1)
        img = np.delete(img, -1, axis=1)
    fg = img - bg
    return bg, fg


def i2dft(bg, fg):
  return ifft2(bg), ifft2(fg)


def sep_stft(img, background_mag, foreground_mag):
    filt = background_mag > foreground_mag
    bg = filt*img
    fg = img - bg
    return bg, fg


def inverse_short_time(background_dat, foreground_dat):
  N1, bg = signal.istft(background_dat)
  N2, fg = signal.istft(foreground_dat)
  time_bg = N1/44100
  time_fg = N2/44100
  return time_bg, bg, time_fg, fg


def write_wav(x, filename, sample_rate=44100):
    scaled = np.int16(x / np.max(np.abs(x)) * 32767)
    wav.write(filename, sample_rate, scaled)


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


def short_time_fourier_transform(audio, nperseg,
                                 sample_rate=44100, window='hann'):
    frequency, time, transformed_audio = signal.stft(audio, sample_rate,
                                                     window=window,
                                                     nperseg=nperseg,
                                                     noverlap=.5*nperseg)
    return frequency, time, transformed_audio



def fourier_transform_2d(short_time_fourier):
    transformed_2d = fft2(abs(short_time_fourier))
    return transformed_2d


def initial_separation(transformed_2d, window_size_r, k, window_size_s=1):
    background_component = np.empty_like(transformed_2d)
    for s in np.arange(0,
                       transformed_2d.shape[0],
                       window_size_s):
        gamma = np.std(transformed_2d[s])
        for r in np.arange(0,
                           transformed_2d.shape[1],
                           window_size_r):
            hood = abs(transformed_2d[s: s + window_size_s, r: r + window_size_r])
            win_range = np.max(hood) - np.min(hood)
            if win_range >= k*gamma:  # Peak present
                background_component[s:s + window_size_s, r:r + window_size_r] = transformed_2d[s:s + window_size_s,
                                                                               r:r + window_size_r]
            else:
                background_component[s:s + window_size_s, r:r + window_size_r] = 0
    foreground_component = transformed_2d - background_component

    return background_component, foreground_component


def inverse_2d_spectrograms(background_component, foreground_component):
  background_magnitude = ifft2(background_component)
  foreground_magnitude = ifft2(foreground_component)

  return background_magnitude, foreground_magnitude


def another_separation_function(transformed_audio, background_mag,
                                foreground_mag):
    background_dat = np.empty_like(transformed_audio)
    for f in range(transformed_audio.shape[0]):
        for t in range(transformed_audio.shape[1]):
            if background_mag[f][t] >= foreground_mag[f][t]:
                background_dat[f][t] = transformed_audio[f][t]
            else:
                background_dat[f][t] = 0
    foreground_dat = transformed_audio - background_dat

    return background_dat, foreground_dat


def inverse_short_time(background_dat, foreground_dat):
  N1, background_audio = signal.istft(background_dat)
  N2, foreground_audio = signal.istft(foreground_dat)
  time_1 = N1/44100
  time_2 = N2/44100

  return time_1, background_audio, time_2, foreground_audio


def plot_short_time_fourier_transform(frequency, time, transformed_audio):
  fig, ax = plt.subplots()
  ax.pcolormesh(time, frequency,
                abs(np.log10(transformed_audio)),
                shading = 'auto')
  ax.set_ylabel('Frequency [Hz]', fontsize=16)
  ax.set_xlabel('Time [sec]', fontsize=16);
  plt.title('Audio Spectrogram of "PatrickTalbot.wav"', fontsize=18)
  plt.show()


def plot_2d_fourier_transform(transformed_2d_fourier):
    fig, ax = plt.subplots()

    plt.imshow(np.abs(transformed_2d_fourier),
               norm=LogNorm(vmin=5))
    colour_bar = plt.colorbar(fraction=0.046, pad=0.04)
    colour_bar.set_label('Relative Intensity')

    plt.title("2D Fourier transform on Audio Spectrogram", fontsize=12)
    plt.xlabel("Rate [cyc/s]", fontsize=12)
    plt.ylabel("Scale [cyc/Hz]", fontsize=12)
    plt.show()


def plot_compare(transformed_2d, foreground_component, background_component,
                 f, t, transformed_audio, foreground_dat, background_dat, norm=LogNorm(vmin=5)):
    total_dat = background_dat + foreground_dat
    total_components = background_component + foreground_component
    try:
        Z1 = np.log10(background_dat)
    except ZeroDivisionError:
        Z1 = 0
    try:
        Z2 = np.log10(foreground_dat)
    except ZeroDivisionError:
        Z2 = 0
    try:
        Z3 = np.log10(total_dat)
    except ZeroDivisionError:
        Z3 = 0

    fig, ax = plt.subplots(4,2, figsize=(16,8))

    ax[0][0].imshow(abs(transformed_2d), norm=norm, label='Original')
    ax[0][0].title.set_text('2DFT')
    ax[0][0].set_xlabel("Rate [cyc/s]", fontsize=8)
    ax[0][0].set_ylabel("Scale [cyc/Hz]", fontsize=8)
    ax[0][1].pcolormesh(t, f, abs(np.log10(transformed_audio)), shading='auto')
    ax[0][1].title.set_text('Original')

    ax[1][0].imshow(abs(foreground_component), norm=norm, label='Original')
    ax[1][0].title.set_text('FG 2DFT')
    ax[1][0].set_xlabel("Rate [cyc/s]", fontsize=8)
    ax[1][0].set_ylabel("Scale [cyc/Hz]", fontsize=8)
    ax[1][1].pcolormesh(t, f, abs(Z2), shading='auto')
    ax[1][1].title.set_text('FG Spectrogram')

    ax[2][0].imshow(abs(background_component), norm=norm, label='Original')
    ax[2][0].title.set_text('BG')
    ax[2][0].set_xlabel("Rate [cyc/s]", fontsize=8)
    ax[2][0].set_ylabel("Scale [cyc/Hz]", fontsize=8)
    ax[2][1].pcolormesh(t, f, abs(Z1), shading='auto')
    ax[2][1].title.set_text('BG Spectrogram')

    ax[3][0].imshow(abs(total_components), norm=norm, label='Original')
    ax[3][0].title.set_text('TOT')
    ax[3][0].set_xlabel("Rate [cyc/s]", fontsize=8)
    ax[3][0].set_ylabel("Scale [cyc/Hz]", fontsize=8)
    ax[3][1].pcolormesh(t, f, abs(Z3), shading='auto')
    ax[3][1].title.set_text('BG+FG')
    fig.tight_layout(pad=3.0)
    plt.show()


def plot_audio(x1, x2, t1, t2):
    fig, ax = plt.subplots(1, 2)
    ax[0].plot(t1, x1)
    ax[0].set_xlabel('Time[s]')
    ax[0].set_ylabel('Amplitude')
    ax[1].plot(t2, x2)
    ax[1].set_xlabel('Time[s]')
    ax[1].set_ylabel('Amplitude')
    plt.show()


def write_wav(x, filename, sample_rate=44100):
    scaled = np.int16(x / np.max(np.abs(x)) * 32767)
    wav.write(filename, sample_rate, scaled)


def strip_voice(bg, fg, f):
    f_filt_bg = (f>5000)
    bg_extra = fg[f_filt_bg]
    fg[f_filt_bg] = 0 # Selected data from voice corresponding to music
    bg[f_filt_bg] += bg_extra
    return bg, fg

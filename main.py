from funcs import *
import time as t


def main(path, freq_res, k):
    '''

    :param freq_res: Frequency resolution, coupled to time resolution
                     number of frequency bins in STFT is 2^(8+freq_res)
                     Tradeoff between frequency and time resolution
    :param k:        Number of Standard Deviations within window to identify Peak
                     Increasing k increases the sensitivity to periodic components
                     High K means all data captured in vocal component
    :return:         Saves Separated files
    '''

    t0 = t.time()
    audio, sample_rate = read_wav(path)
    transformed_audio = stft(audio, freq_res, sample_rate)
    transformed_2d = ft2d(transformed_audio)
    background_2d, foreground_2d = sep2d(transformed_2d, k)
    background_mag, foreground_mag = i2dft(background_2d,foreground_2d)
    background_dat, foreground_dat = sep_stft(transformed_audio, background_mag, foreground_mag)
    time_1, background_audio, time_2, foreground_audio = inverse_short_time(background_dat, foreground_dat)

    path_bg = 'bg.wav'
    path_fg = 'fg.wav'
    write_wav(background_audio, path_bg)
    write_wav(foreground_audio, path_fg)
    t1 = t.time()
    t_tot = t1 - t0
    print('Time elapsed %s' % t_tot)
    print(path)

# TO RUN
# main('song.wav', 2, 8)


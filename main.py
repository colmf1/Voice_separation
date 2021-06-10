from funcs import *
import time as t
def main(path, nperseg, w, k):
    '''
    param nperseg: Number of Frequency bins in the STFT
    param w: Window size in image convolution of 2DFT spectrogram
    param k: Number of Standard Deviations within window to identify Peak
    return: Saves Separated files, and returns data to plot audio files
    '''
    t0 = t.time()
    audio, sample_rate = read_wav(path)
    frequency, time, transformed_audio = short_time_fourier_transform(audio, nperseg,
                                                                      sample_rate)
    transformed_2d = fourier_transform_2d(transformed_audio)

    background_2d, foreground_2d = initial_separation(transformed_2d, w, k)

    background_mag, foreground_mag = inverse_2d_spectrograms(background_2d,
                                                             foreground_2d)

    background_dat, foreground_dat = another_separation_function(transformed_audio,
                                                                 background_mag,
                                                                 foreground_mag)

    time_1, background_audio, time_2, foreground_audio = inverse_short_time(background_dat,
                                                                            foreground_dat)

    path_bg = 'bg%s_%s_%s.wav' %(nperseg, w, k)
    path_fg = 'fg%s_%s_%s.wav' %(nperseg, w, k)
    write_wav(background_audio, path_bg)
    write_wav(foreground_audio, path_fg)
    #play_audio(path_fg)
    #plot_compare(transformed_2d, foreground_2d, background_2d,
                 #frequency, time, transformed_audio, foreground_dat, background_dat)
    t1 = t.time()
    t_tot = t1-t0
    print('Time elapsed %s' %t_tot)
    print(path)

main('song.wav', 512)

'''
Loop to find best parameters
npersegs = [512, 1024, 2048, 4096, 8192]
wins = [2, 4, 8, 16, 32, 64]
ks = [1, 2, 4, 8, 16, 32]

for n in npersegs:
    for win in wins:
        for k in ks:
            time_1, background_audio, time_2, foreground_audio = main('Seventeen.wav', n, win, k)
'''
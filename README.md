# Voice_separation
Algorithm separating Vocal/Musical components of a song.

Based on MUSIC/VOICE SEPARATION USING THE 2D FOURIER TRANSFORM - by - Prem Seetharaman, Fatemeh Pishdadian, Bryan Pard.

Program takes .wav file as input. Outputs bg.wav and fg.wav.

### Tuneable Parameters 

Freq_res - Frequency resolution of STFT, coupled to time resolution:
           Number of frequency bins in STFT to produce spectrogram
           nperseg = 2^(8+freq_res)

k - Peak sensitivity; Number of standard deviations within window to determine peak

## Demonstration - https://colmf1.github.io/Voice_separation/demo.html

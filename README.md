# Voice_separation
Algorithm separating Vocal/Musical components of a song.

Based on MUSIC/VOICE SEPARATION USING THE 2D FOURIER TRANSFORM - by - Prem Seetharaman, Fatemeh Pishdadian, Bryan Pard.
Method detects temporal repititions in the audio spectrogram and relies on the assumption that background music is relativly periodic in comparison to vocals. Musical component will appear as peaks in 2D spectrogram.

Program takes .wav file as input. Outputs bg.wav and fg.wav.

### Tuneable Parameters 
nperseg - Number of frequency bins in STFT to produce spectrogram
w - window size for detecting peaks in 2DFT spectrogram
k - Peak sensitivity; Number of standard deviations within window to determine peak

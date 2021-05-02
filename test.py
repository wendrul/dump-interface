import pyaudio
import numpy as np
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style
import scipy
from scipy.signal import argrelextrema
import math
import asyncio
import playsound

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
MAX_TIME_BUFFERED = 5
VOL_TRESHOLD = 100000


pa = pyaudio.PyAudio()

callback_output = []


def callback(in_data, frame_count, time_info, flag):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    callback_output.append(audio_data)
    if (len(callback_output) > MAX_TIME_BUFFERED * (RATE / CHUNK)):
        callback_output.pop(0)
    return None, pyaudio.paContinue


def get_n_maxes(data, n):
    """
    Returns the n biggest maxima sorted from largest to smallest
    """
    maxes = scipy.signal.argrelmax(data, order=100)
    ret = []
    for _ in range(n):
        M = None
        for m in maxes[0]:
            if (M == None or (data[m] > data[M])) and (not m in ret):
                M = m
        ret.append(M)
    return ret

stream = pa.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 output=False,
                 input=True,
                 stream_callback=callback,
                 frames_per_buffer=CHUNK)

stream.start_stream()

time.sleep(2)

def JoinData(output, numberOfChunks):
    """
    Joins numberOfChunks before the current chunk and returns that as one element
    """
    i = 0
    ret = np.zeros(len(output[-1]) * numberOfChunks)
    j = 0
    while (i < numberOfChunks):
        k = 0
        while (k < len(output[-(numberOfChunks - i)])):
            ret[j] = output[-(numberOfChunks - i)][k]
            k += 1
            j += 1
        i += 1
    return ret


def isFreqInMaxes(freq, maxes, fft_data, fft_freq, freqRange=100):
    closest = 0
    for i in range(len(maxes)):
        if (abs(freq - fft_freq[maxes[i]]) < abs(freq - fft_freq[maxes[closest]])):
            closest = i
    if (abs(freq - fft_freq[maxes[closest]]) < freqRange):
        return 1 - (freq - fft_freq[maxes[closest]]) / freqRange
    return 0
    



async def AnalyzeSpike(data):
    fft_data = np.fft.rfft(data)
    fft_freq = np.fft.rfftfreq(len(data), d = 1/RATE)
    maxes1 = get_n_maxes(fft_data, 3)
    maxes = get_n_maxes(fft_data, 8)
    certainFactor = 0
    certainFactor += isFreqInMaxes(1731, maxes1, fft_data, fft_freq, freqRange=175) * 2
    if (certainFactor == 0):
        certainFactor += isFreqInMaxes(1731, maxes, fft_data, fft_freq, freqRange=175)
    certainFactor += isFreqInMaxes(3930, maxes, fft_data, fft_freq, freqRange=400) * 0.5 + 0.5
    certainFactor += isFreqInMaxes(568, maxes1, fft_data, fft_freq, freqRange=175) * 2
    
    certainFactor -= isFreqInMaxes(2780, maxes, fft_data, fft_freq, freqRange=100) * 0.5
    certainFactor -= isFreqInMaxes(280, maxes, fft_data, fft_freq, freqRange=100) * 0.5
    certainFactor += isFreqInMaxes(50, maxes1, fft_data, fft_freq, freqRange=20)
    print(certainFactor)

    if (certainFactor > 2.3):
        #print("success!")
        playsound.playsound("poop.mp3")
    # for x in maxes:
        # print (f"{abs(fft_data[x]):.1f}, {fft_freq[x]:.1f}")
    # print("        ")

detect = False
t_last = time.time()
t = 0
last_vol = 0
while stream.is_active():
    dt = time.time() - t_last
    t_last = time.time()
    vol = np.linalg.norm(callback_output[-5])
    if (abs(vol - last_vol) > 10**-2):   
        if (vol > VOL_TRESHOLD):
            detect = True
            t = 0
            asyncio.run(AnalyzeSpike(JoinData(callback_output, 5)))
    last_vol = vol
    if detect == True:
        t += dt
        if t >= 1.5:
            detect = False
            print("\n\n\n----------------------\nEND\n----------------------\n\n\n")    
    # fft_data = np.fft.rfft(callback_output[-1]) # rfft removes the mirrored part that fft generates
    # fft_freq = np.fft.rfftfreq(len(callback_output[-1]), d=1/44100) # rfftfreq needs the signal data, not the fft data
    # plt.plot(fft_freq, np.absolute(fft_data)) # fft_data is a complex number, so the magnitude is computed here
    # plt.xlim(np.amin(fft_freq), 5000)
    # plt.ylim(0, 6000000)
    # fig.canvas.draw()
    # plt.pause(0.05)
    # fig.canvas.flush_events()
    # fig.clear()


stream.close()
pa.terminate()
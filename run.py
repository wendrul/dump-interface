import numpy as np
import time
import scipy
from scipy.signal import argrelextrema
import math
import asyncio
import pyaudio
import sys
import random
import playsound
from PoopVoiceLines import PoopVoiceLines
from SerialInterface import PooperInterface
from FullScreenMSG import FullScreenMSG
import tkinter as tk

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
MAX_TIME_BUFFERED = 5
VOL_TRESHOLD = 50000#100000


pa = pyaudio.PyAudio()

callback_output = []


def callback(in_data, frame_count, time_info, flag):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    callback_output.append(audio_data)
    if (len(callback_output) > MAX_TIME_BUFFERED * (RATE / CHUNK)):
        callback_output.pop(0)
    return None, pyaudio.paContinue

stream = pa.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 output=False,
                 input=True,
                 stream_callback=callback,
                 frames_per_buffer=CHUNK)

stream.start_stream()


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

    if (certainFactor > 2.3):
        print("poop", file=sys.stderr)
        voices.playRandomLine()
    # for x in maxes:
        # print (f"{abs(fft_data[x]):.1f}, {fft_freq[x]:.1f}")
    # print("        ")

with open("messages/samples.txt") as msgs:
    lines = msgs.readlines()
    availableSamples = []
    busySamples = []
    turn = 0
    for l in lines:
        if len (l) < 3:
            continue
        if "AVAILABLE" in l:
            turn = 1
            continue
        elif "BUSY" in l:
            turn = 2
            continue
        if turn == 1:
            availableSamples.append(l)
        elif turn == 2:
            busySamples.append(l)

root = tk.Tk()
FS_Display = FullScreenMSG(root)

def OnSitUp():
    FS_Display.ChangeBackgroundColor("green")
    FS_Display.PrintMsg(random.choice(availableSamples))

def OnSitDown():
    FS_Display.ChangeBackgroundColor("red")
    FS_Display.PrintMsg(random.choice(busySamples))

OnSitUp()
root.update()

voices = PoopVoiceLines()
ser = PooperInterface(port='/dev/ttyUSB0')

detect = False
t_last = time.time()
t = 0
last_vol = 0
wasActive = False
while stream.is_active():
    try:
        root.update_idletasks()
        ser.UpdateStatus()
        dt = time.time() - t_last
        t_last = time.time()
        if (ser.IsSitting()):
            if (not wasActive):
                OnSitDown()
            wasActive = True
            vol = np.linalg.norm(callback_output[-5])
            if (abs(vol - last_vol) > 10**-2):   
                if (vol > VOL_TRESHOLD):
                    t = 0
                    asyncio.run(AnalyzeSpike(JoinData(callback_output, 5)))
            last_vol = vol
            t += dt
            if t >= 20:
                detect = False
                voices.playRandomLine(lineType="constipation")
                t = 0
        else:
            if (wasActive):
                OnSitUp()
            t = 0
            wasActive = False
    except KeyboardInterrupt:
        print("exit uwu", file=sys.stderr)
        break

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
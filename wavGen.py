import numpy as np
from scipy.io.wavfile import write
import sys
import math

def sine(frequency=440, length=60, rate=44100):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return np.sin(np.arange(length) * factor)

def wavGen(name,func):
    if (name != ""):
        if (func == "sine"):
            data = sine() # np.random.uniform(-1,1,44100) # 44100 random samples between -1 and 1
        else:
            data = np.random.uniform(-1,1,44100) # 44100 random samples between -1 and 1
    else:
    	print "Please provide a filename and a function name (sine or rand)"
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write(name, 44100, scaled)

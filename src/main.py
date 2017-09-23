import sys
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

def gen_collage(filename):
  # Read + the file data + rate
  rate, data = scipy.io.wavfile.read(filename)
  # Grab relevant data + times
  s1 = data[:, 1]
  n = len(s1)
  time_array = [float(ts) / rate for ts in range(0, n)]
  # Plot out the tone
  plt.plot(time_array, s1, color='k')
  plt.ylabel('Amplitude')
  plt.xlabel('Time (ms)')
  plt.show()

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print 'Improper arguments!'
  else:
    gen_collage(sys.argv[1])

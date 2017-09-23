import sys
import math
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

BASE = 10

def amps_per_s(s1, rate, seconds_array):
  result = []
  for sec in seconds_array:
    result.append(np.mean(s1[(sec - 1) * rate: sec * rate]))
  return result

def top_freq_db_per_s(s1, rate, hz, seconds_array):
  result = []
  for sec in seconds_array:
    freq_arr, pwr = \
      windowed_power_spectrum(s1[(sec - 1) * rate: sec * rate], hz)
    top_idx = np.argmax(pwr)
    result.append((freq_arr[top_idx], pwr[top_idx]))
  return result

def windowed_power_spectrum(window, hz):
  # size of the window
  n = len(window)
  # One-dimensional Fourier transform (outputs np array)
  p = np.fft.fft(window)
  # Cleans of complex #s, scale + compute power
  n_unique_pts = int(math.ceil((n + 1) / 2.0))
  p = abs(p[0:n_unique_pts])
  p = (p / float(n)) ** 2
  # Multiply by 2 to keep power since half points were dropped
  if n % 2 > 0:
    p[1:len(p)] = p[1:len(p)] * 2
  else:
    p[1:len(p) -1] = p[1:len(p) - 1] * 2
  # Most interesting metrics
  freq_array = [f * hz for f in range(0, n_unique_pts)] # in Hz
  power = 10 * np.log10(p) # in dB
  # Resultant
  return freq_array, power

def circle_tuples(amps, hzs, dbs):
  assert len(amps) == len(hzs) == len(dbs)
  # Length of all of them
  n = len(amps)
  # Scaling factors
  hz_max, hz_min = np.max(hzs), np.min(hzs)
  db_max, db_min = np.max(dbs), np.min(dbs)

  # Compute scaled values according to `base`
  result = []
  for i in xrange(0, n):
    amp = amps[i]
    hz = (BASE * (hzs[i] - hz_min)) / float(hz_max - hz_min)
    db = (BASE * (dbs[i] - db_min)) / float(db_max - db_min)
    result.append((amp, hz, db))
  return result

# NOTE - main function to run
def gen_collage(filename):
  # Read + the file data + rate
  rate, data = scipy.io.wavfile.read(filename)
  # Grab relevant data + times
  s1 = data[:, 0]
  n = len(s1)
  total_seconds = n / rate
  seconds_array = range(1, total_seconds + 1)
  hz = float(rate) / n # hertz

  # amp / s
  amps = amps_per_s(s1, rate, seconds_array)
  # Hz + dB / s
  hz_db = top_freq_db_per_s(s1, rate, hz, seconds_array)

  # Tuples for drawing
  circ_tups = circle_tuples(amps, [t[0] for t in hz_db], [t[1] for t in hz_db])

  # Collect those circles
  circs = []
  amps = [] # needed for the y-limits
  for i, tup in enumerate(circ_tups):
    # Position driven by time (x) and amplitude (y)
    # Circle radius driven by scaled Hz (radius)
    # Color driven by dB (darker == lower)
    x, y = i * BASE * 1.5, tup[0]
    rand_c = '#%02x%02x%02x' % tuple(np.floor(np.random.rand(3, 1) * 255))
    alpha = tup[2] / float(BASE)
    radius = tup[1]
    circs.append(plt.Circle((x, y), radius=radius, color=rand_c, alpha=alpha))
    amps.append(y)

  # Prepare plot
  fig, ax = plt.subplots(figsize=(50, 50))
  plt.xlim(0, len(circs) * BASE)
  plt.ylim(min(amps) - BASE, max(amps) + BASE) # for buffer
  plt.axis('off')
  for c in circs:
    ax.add_artist(c)

  # Save it to a file
  fig.savefig('collage.png', bbox_inches='tight')

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print 'Improper arguments!'
  else:
    gen_collage(sys.argv[1])

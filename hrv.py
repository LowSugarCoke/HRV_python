import numpy as np
from scipy.fftpack import fft  
import matplotlib.pyplot as plt
import pywt

# 小波
def denoise(data):
    coeffs = pywt.wavedec(data=data, wavelet='db5', level=9)
    cA9, cD9, cD8, cD7, cD6, cD5, cD4, cD3, cD2, cD1 = coeffs

    # 域值去噪
    threshold = (np.median(np.abs(cD1)) / 0.6745) * (np.sqrt(2 * np.log(len(cD1))))
    cD1.fill(0)
    cD2.fill(0)
    for i in range(1, len(coeffs) - 2):
        coeffs[i] = pywt.threshold(coeffs[i], threshold)

    # 小波reconstruction
    rdata = pywt.waverec(coeffs=coeffs, wavelet='db5')
    return rdata

def ImportData(path):
    np_data = np.loadtxt(path)
    return np_data

def Plot(data):
    # origin signal
    x = np.linspace(0,1,data.size)
    fig, ax = plt.subplots(1, figsize=(6, 4.5))
    ax.plot(x, data, "r")
    plt.show()
    
data = ImportData("180hz_10minute__15frequency_breath.txt")
# Plot(data)
d = denoise(data)
Plot(d)












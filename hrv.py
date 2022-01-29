import numpy as np
from scipy.fftpack import fft  
import matplotlib.pyplot as plt
import pywt
from scipy.signal import medfilt
from scipy.fftpack import fft
from scipy.interpolate import interp1d
from scipy.integrate import trapz
from scipy import signal


def Differential(data):
    i=4
    d=np.arange(data.size)
    for i in range(data.size):
       d[i]=1.3*abs(data[i]-data[i-2])+1.1*abs(data[i]-2*data[i-2]+data[i-4])+100
    return d

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

def BaseLine(data):
    filter = int(0.8*180)
    baseline = medfilt(data,filter+1)
    filter_data = data-baseline
    return filter_data

def MovingAverage(data):
    moving_line = np.arange(float(data.size+1));
    temp=0.0
    i=0
    for i in range(data.size):
       moving_line[i+1] = moving_line[i]+(10+data[i]-moving_line[i])/30
    return moving_line

    
def Plot(ori_data,diff_data,denoise_data,base_line,moving_line,r_pick,r_high):
    x = np.linspace(0,ori_data.size,ori_data.size)
    diff_x=np.linspace(0,diff_data.size,diff_data.size)
    x1 = np.linspace(0,denoise_data.size,denoise_data.size)
    x2 = np.linspace(0,base_line.size,base_line.size)
    x3 = np.linspace(0,moving_line.size,moving_line.size)
    

    fig,ax = plt.subplots()
    plt.plot(x, ori_data, "r")
    plt.plot(diff_x,diff_data,"g")
    plt.plot(x1,denoise_data-50,"b")
    # plt.plot(x2,base_line,"g")
    plt.plot(x3,moving_line-50,"r")

    i=1
    for i in np.arange(r_pick.size):
        circle1 = plt.Circle((r_pick[i],r_high[i]-50),radius=3,color="r",fill=False)
        ax.add_patch(circle1)
 
    
    plt.show()

def PickRPoint(data,moving_line):
    flag=0
    data_higher_moving=[]
    data_higher_position=[]
    r_position=[]
    r_high=[]
    for i in range(data.size):
        if (data[i]-moving_line[i])>0:
            flag=1
        else:
            if flag==1:
                max_data = max(data_higher_moving)
                # print(max_data)
                index = data_higher_moving.index(max_data)
                r_position.append(data_higher_position[index])
                r_high.append(max_data)
                data_higher_moving.clear()
                data_higher_position.clear()
                flag=0
        
        if flag==1:
            data_higher_moving.append(data[i])
            data_higher_position.append(i)
    
    return r_position,r_high

def CalHeartRate(r_position,sample_rate):
    rr_interval=[]
    for i in range(2,r_position.size):
        rr_interval.append(r_position[i]-r_position[i-1])
    for a in range(len(rr_interval)):
        rr_interval[a]=rr_interval[a]/sample_rate 
    
    
    return rr_interval    

def Interpolation(rr_interval):
    x = np.cumsum(rr_interval)
    f = interp1d(x,rr_interval,kind='cubic')
    
    fs=4.0
    steps = 1/fs
    
    xx=np.arange(1,np.max(x),steps)
    rr_interpolated = f(xx)
    # plt.figure(figsize=(20, 15))

    # plt.subplot(211)
    # plt.title("RR intervals")
    # plt.plot(x, rr_interval, color="k", markerfacecolor="#A651D8", markeredgewidth=0, marker="o", markersize=8)
    # plt.xlabel("Time (s)")
    # plt.ylabel("RR-interval (ms)")
    # plt.title("Interpolated")
    # plt.gca().set_xlim(0, 20)

    # plt.subplot(212)
    # plt.title("RR-Intervals (cubic interpolation)")
    # plt.plot(xx, rr_interpolated, color="k", markerfacecolor="#51A6D8", markeredgewidth=0, marker="o", markersize=8)
    # plt.gca().set_xlim(0, 20)
    # plt.xlabel("Time (s)")
    # plt.ylabel("RR-interval (ms)")
    # plt.show()
    
    return rr_interpolated
    


def frequency_domain(rr_interpolated, fs=4):
    # Estimate the spectral density using Welch's method
    fxx, pxx = signal.welch(x=rr_interpolated, fs=fs)
    
    '''
    Segement found frequencies in the bands 
     - Very Low Frequency (VLF): 0-0.04Hz 
     - Low Frequency (LF): 0.04-0.15Hz 
     - High Frequency (HF): 0.15-0.4Hz
    '''
    cond_vlf = (fxx >= 0) & (fxx < 0.04)
    cond_lf = (fxx >= 0.04) & (fxx < 0.15)
    cond_hf = (fxx >= 0.15) & (fxx < 0.4)
    
     # calculate power in each band by integrating the spectral density 
    vlf = trapz(pxx[cond_vlf], fxx[cond_vlf])
    lf = trapz(pxx[cond_lf], fxx[cond_lf])
    hf = trapz(pxx[cond_hf], fxx[cond_hf])
    
    # sum these up to get total power
    total_power = vlf + lf + hf

    # find which frequency has the most power in each band
    peak_vlf = fxx[cond_vlf][np.argmax(pxx[cond_vlf])]
    peak_lf = fxx[cond_lf][np.argmax(pxx[cond_lf])]
    peak_hf = fxx[cond_hf][np.argmax(pxx[cond_hf])]

    # fraction of lf and hf
    lf_nu = 100 * lf / (lf + hf)
    hf_nu = 100 * hf / (lf + hf)
    
    results = {}
    results['Power VLF (ms2)'] = vlf
    results['Power LF (ms2)'] = lf
    results['Power HF (ms2)'] = hf   
    results['Power Total (ms2)'] = total_power

    results['LF/HF'] = (lf/hf)
    results['Peak VLF (Hz)'] = peak_vlf
    results['Peak LF (Hz)'] = peak_lf
    results['Peak HF (Hz)'] = peak_hf

    results['Fraction LF (nu)'] = lf_nu
    results['Fraction HF (nu)'] = hf_nu
    return results, fxx, pxx
    

data = ImportData("180hz10minutejack9.5breath.txt")
diff_data = Differential(data)
denoise_data = denoise(diff_data)
baseline_data = BaseLine(denoise_data)
moving_line = MovingAverage(denoise_data)


r_pick,r_high = PickRPoint(denoise_data,moving_line)
r_pick = np.array(r_pick)
r_high = np.array(r_high)
# Plot(data,diff_data,denoise_data,baseline_data,moving_line,r_pick,r_high)
rr_interval = CalHeartRate(r_pick,180)
print(rr_interval)

rr_interpolated = Interpolation(rr_interval)
results, fxx, pxx = frequency_domain(rr_interpolated)
for k, v in results.items():
    print("- %s: %.2f" % (k, v))
    
plt.figure(figsize=(20, 7))
plt.plot(fxx, pxx, color="k", linewidth=0.3)
plt.title("FFT Spectrum (Welch's periodogram)")

# create interpolation function for plotting frequency bands
psd_f = interp1d(fxx, pxx)

# setup frequency bands for plotting
x_vlf = np.linspace(0, 0.04, 100)
x_lf = np.linspace(0.04, 0.15, 100)
x_hf = np.linspace(0.15, 0.4, 100)

plt.gca().fill_between(x_vlf, psd_f(x_vlf), alpha=0.2, color="#A651D8", label="VLF")
plt.gca().fill_between(x_lf, psd_f(x_lf), alpha=0.2, color="#51A6D8", label="LF")
plt.gca().fill_between(x_hf, psd_f(x_hf), alpha=0.2, color="#D8A651", label="HF")
plt.gca().set_xlim(0, 0.5)
plt.gca().set_ylim(0)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Density")
plt.legend()
plt.show()






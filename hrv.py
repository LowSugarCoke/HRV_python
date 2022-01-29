import numpy as np
from scipy.fftpack import fft  
import matplotlib.pyplot as plt
import pywt
from scipy.signal import medfilt

#  dt[i] = 1.3*abs(Cosine[i] - Cosine[i - 2]) + 1.1*abs(Cosine[i] - 2 * Cosine[i - 2] + Cosine[i - 4]);
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


    # print(r_x[1],r_pick[1])
    # circle1 = plt.Circle((r_x[1],r_pick[1]-50),radius=3,color="r",fill=False)
    # ax.add_patch(circle1)
    i=1
    for i in np.arange(r_pick.size):
        circle1 = plt.Circle((r_pick[i],r_high[i]-50),radius=3,color="r",fill=False)
        ax.add_patch(circle1)
    # circle = plt.Circle((r_x, r_pick), 0.3)
    # ax.add_patch(circle)
    # draw_circle = plt.Circle((0.5, 0.5), 0.3,fill=False)
    
    plt.show()

def PickRPoint(data,moving_line):
    i=200
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
        print(i)
        rr_interval.append(r_position[i]-r_position[i-1])
    

    for a in rr_interval:
        a=a/sample_rate 
        print(a)    
    

data = ImportData("180hz_10minute__15frequency_breath.txt")
diff_data = Differential(data)
denoise_data = denoise(diff_data)
baseline_data = BaseLine(denoise_data)
moving_line = MovingAverage(denoise_data)


r_pick,r_high = PickRPoint(denoise_data,moving_line)
r_pick = np.array(r_pick)
r_high = np.array(r_high)
# Plot(data,diff_data,denoise_data,baseline_data,moving_line,r_pick,r_high)
CalHeartRate(r_pick,180)









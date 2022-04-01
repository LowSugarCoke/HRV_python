<p align=center>
<img target = "banner" src="https://raw.githubusercontent.com/LowSugarCoke/HRV_python/main/img/frequency_domain.PNG">
</p>

<p align=center>
<a target="badge" href="https://github.com/LowSugarCoke/Pixiv-Downloader/blob/main/img/banner.png" title="python version"><img src="https://img.shields.io/badge/python-v3.9.7-brightgreen"></a>
<a target="badge" href="https://github.com/LowSugarCoke/RPG-Game" title="visual studio version" title="os:windows"><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" width=85/></a>  
</p>

>Heart rate variability (HRV) is the physiological phenomenon of variation in the time interval between heartbeats. It is measured by the variation in the beat-to-beat interval.



## Download source code
In order to analysis hrv, make sure that you have python 3.9.7 and python packages as below:
* numpy 1.21.4
* matplotlib 3.5.0
* PyWavelets 1.2.0
* scipy 1.7.3

```
$ git clone https://github.com/LowSugarCoke/HRV_python
```

## Usage
### Visual Studio Code
Download VSCode https://code.visualstudio.com/

Download python https://www.python.org/

After installing VScode and Python, download the extension in VSCode as follow:
* python
* python for vscode
* code runner

Done it and Run code


## Introduction
### Time-Domain Processing
```mermaid
    flowchart TD;
     A[Import ECG data]-->B[Differential];
     B[Differential]-->C[Denoise];
     C[Denoise]-->D[BaseLine];
     D[BaseLine]-->E[Pick R Point];
     E[Pick R Point]-->F[Plot time-domain signal]
```

![img](https://raw.githubusercontent.com/LowSugarCoke/HRV_python/main/img/time_domain.PNG)

### Frequency-Domain Processing
```mermaid
  flowchart TD;
   A[Import differential ecg and dynamic line]-->B[Calculate RR interval];
   B[Calculate RR interval]-->C[Interpolation];
   C[Interpolation]-->D[Transfer to frequency domain];
   D[Transfer to frequency domain]-->E[Plot frequency-domain signal]
```
![img](https://raw.githubusercontent.com/LowSugarCoke/HRV_python/main/img/interpolated.PNG)
![img](https://raw.githubusercontent.com/LowSugarCoke/HRV_python/main/img/frequency_domain.PNG)
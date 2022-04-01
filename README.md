<p align=center>
<img target = "banner" src="https://raw.githubusercontent.com/LowSugarCoke/HRV_python/main/img/frequency_domain.PNG">
</p>

<p align=center>
<a target="badge" href="https://github.com/LowSugarCoke/Pixiv-Downloader/blob/main/img/banner.png" title="python version"><img src="https://img.shields.io/badge/python-v3.9.7-brightgreen"></a>
<a target="badge" href="https://github.com/LowSugarCoke/RPG-Game" title="visual studio version" title="os:windows"><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" width=85/></a>  
</p>

>Heart rate variability (HRV) is the physiological phenomenon of variation in the time interval between heartbeats. It is measured by the variation in the beat-to-beat interval.

## Download source code
In order to use hrv analysis, make sure that you have python 3.9.7 and python packages as below:
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
```flow
  start=>start: Import ecg data
  differential=>operation: Differential
  denoise=>operation: Denoise
  baseline=>operation: BaseLine
  pickrpoint=>operation: Pick R Point
  end=>end: Plot time-domain signal
  start->differential->denoise->baseline->pickrpoint->end
```

![img](https://raw.githubusercontent.com/LowSugarCoke/HRV_python/main/img/time_domain.PNG)

### Frequency-Domain Processing
```flow
  start=>start: Import differential ecg and dynamic line
  rr_interval=>operation: Calculate RR interval
  interpolation=>operation: Interpolation
  frequency=>operation: Transfer to Frequency Domain 
  end=>end: Plot frequency-domain signal
  start->rr_interval->interpolation->frequency->end
```
![img](https://raw.githubusercontent.com/LowSugarCoke/HRV_python/main/img/interpolated.PNG)
![img](https://raw.githubusercontent.com/LowSugarCoke/HRV_python/main/img/frequency_domain.PNG)
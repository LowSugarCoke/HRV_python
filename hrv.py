import hrv_lib as hrv 
import numpy as np


if __name__ == '__main__':
    data = hrv.ImportData("180hz_10minute__15frequency_breath.txt")
    diff_data = hrv.Differential(data)
    denoise_data = hrv.denoise(diff_data)
    baseline_data = hrv.BaseLine(denoise_data)
    moving_line = hrv.MovingAverage(diff_data)


    r_pick,r_high = hrv.PickRPoint(diff_data,moving_line)
    r_pick = np.array(r_pick)
    r_high = np.array(r_high)
    hrv.Plot(data,diff_data,denoise_data,baseline_data,moving_line,r_pick,r_high)
    rr_interval = hrv.CalHeartRate(r_pick,180)
    print(rr_interval)

    rr_interpolated = hrv.Interpolation(rr_interval)
    results, fxx, pxx = hrv.frequency_domain(rr_interpolated)









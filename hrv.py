import hrv_lib as hrv
import numpy as np

# 讀取檔案


def ImportData(path):
    np_data = np.loadtxt(path)
    return np_data


if __name__ == '__main__':
    data = ImportData("180hz_10minute__15frequency_breath.txt")
    diff_data = hrv.Differential(data)
    denoise_data = hrv.Denoise(diff_data)
    baseline_data = hrv.BaseLine(denoise_data)
    dynamic_line = hrv.DynamicThreshold(diff_data)

    r_pick, r_high = hrv.PickRPoint(diff_data, dynamic_line)
    r_pick = np.array(r_pick)
    r_high = np.array(r_high)
    hrv.PlotTimeDomain(data, diff_data, denoise_data,
                       baseline_data, dynamic_line, r_pick, r_high)
    rr_interval = hrv.CalRRInterval(r_pick, 180)
    print(rr_interval)

    rr_interpolated = hrv.Interpolation(rr_interval)
    results, fxx, pxx = hrv.FrequencyDomain(rr_interpolated)

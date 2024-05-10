
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sys 
import json 
from scipy.signal import find_peaks


plt.close('all')

class Service_assessment():
    def __init__(self,acc_data,fs,_dir,activity_factor):
        self.data = acc_data 
        self.fs = fs
        self._dir = _dir 
        self.act_fact = activity_factor
        self.x_ticks = [1, 2, 3, 5, 6.3, 10, 16, 25, 40, 63, 80]
        self.ylimits = []
        self.xlimits = []
    
  
    def get_acc(self):
        with open('BS_6472_curves.json', 'r') as file:
            data = json.load(file)
        frequency = data[f"BS_6472_accelaration_{self._dir}"]["frequency"]
        accelerations = data[f"BS_6472_accelaration_{self._dir}"]["accelerations"]
        # Factoring the accelerations base on activities 
        accelerations = [value * self.act_fact for value in accelerations]
        self.ylimits = [accelerations[0], accelerations[-1]]
        self.xlimits = [frequency[0], frequency[-1]]
        return frequency,accelerations
    
    def BS_6472(self,color = 'k'):
        # suptitle = 'BS 6472 - Guide to Evaluation of human exposure \n to vibration in buildings'
        title = f'Acceleration (rms) values for the base curve ({self._dir} axis)\nbased on BS 6472'
        frequencies,accelerations = self.get_acc()
        
        fig, ax = plt.subplots()
        plt.plot(frequencies, accelerations, color='r', linewidth=1.2, label='Acceleration limits')  # Added label here
        self.plot_fft_rms(ax)
        
        plt.title(title)
        plt.grid(True, which='both', linestyle='--', color=[0.1, 0.1, 0.1], alpha=0.1)
        plt.xlabel('Frequency (Hz)', fontsize=11)
        plt.ylabel('Acceleration rms (m/s²)', fontsize=11)
        plt.legend(framealpha=0.0)

        ax.legend()  # Display the legend
        
        plt.show()
                
        

    
    def plot_fft_rms(self, ax, color='gray'):
        N = len(self.data)
        fft_output = np.fft.fft(self.data)
        freqs = np.fft.fftfreq(N, 1/self.fs)
        magnitude = 2 * np.abs(fft_output) / N
        rms_per_bin = magnitude / np.sqrt(2)
        
        ax.plot(freqs[:N//2], rms_per_bin[:N//2], color='green', label='Normalized FFT')  # Added label here
    
        # Detecting peaks
        peaks, _ = find_peaks(rms_per_bin[:N//2])
        
        # Find the maximum peak
        max_peak_index = peaks[np.argmax(rms_per_bin[peaks])]
        max_peak_freq = freqs[max_peak_index]
        max_peak_value = rms_per_bin[max_peak_index]
        
        # Define text position relative to peak
        text_x_offset = 0.5
        text_y_offset = 0.1
        
        # Check x boundaries and adjust
        if max_peak_freq + text_x_offset > ax.get_xlim()[1]:
            text_x_offset = -2
    
        # Check y boundaries and adjust
        if max_peak_value + text_y_offset > ax.get_ylim()[1]:
            text_y_offset = -0.5
    
        # Annotate the maximum peak
        ax.annotate(f'({max_peak_freq:.2f} Hz, {max_peak_value:.2f} m/s²)',
                    xy=(max_peak_freq, max_peak_value),
                    xytext=(max_peak_freq + text_x_offset, max_peak_value + text_y_offset),  
                    arrowprops=dict(facecolor='black', arrowstyle='->', shrinkA=0, shrinkB=5))
        
        if self.xlimits[1] < self.fs/2:
            ax.set_xlim(self.xlimits[0], self.xlimits[1])
        else: 
            ax.set_xlim(self.xlimits[0], int(self.fs/2))
        
        ax.grid(True, which='both', linestyle='--', color=[0.1, 0.1, 0.1], alpha=0.1) # Use ax.grid

Service_assessment()
import os
import numpy as np
import matplotlib.pyplot as plt 
# Base directory containing all the other directories
from pathlib import Path
from scipy import integrate,signal


def load_data():
    base_dir = Path.cwd() / 'data' / 'centrifuges'
    # Dictionary to store all the numpy arrays
    data_dict = {}
    # List of directories centri_md_3, centri_md_4, etc.
    centri_dirs = [dir for dir in os.listdir(base_dir) if dir.startswith('centri_md_')]
    print(centri_dirs)
    for centri_dir in centri_dirs:

        print(centri_dir)
        data_dict[centri_dir] = {}
        
        for sub_dir in ['Machine', 'Structure']:
            data_dict[centri_dir][sub_dir] = {}
            
            # List all the .txt files in the subdirectory
            txt_files = [file for file in os.listdir(os.path.join(base_dir, centri_dir, sub_dir)) if file.endswith('.txt')]
            
            for txt_file in txt_files:
                # Load the data from the text file into a numpy array
                data = np.loadtxt(os.path.join(base_dir, centri_dir, sub_dir, txt_file))
                
                # Store the numpy array in the dictionary
                data_dict[centri_dir][sub_dir][txt_file] = data
    return data_dict,centri_dirs




def slice_from_center(array, n=50000):
    # find the middle point of the array
    center_index = len(array) // 2
    
    # slice array from (center - n) to (center + n)
    sliced_array = array[center_index - n : center_index + n]
    
    return sliced_array

def set_array(centri_dirs):
    # New dictionary to hold the final data structure for each `centri_md_*`
    final_data_dict = {}
    
    for centri_dir in centri_dirs:
        # Stack the sliced arrays for Machine and Structure subdirs
        machine_data = np.column_stack([
            slice_from_center(data_dict[centri_dir]['Machine']['EAST-WEST.txt']),
            slice_from_center(data_dict[centri_dir]['Machine']['Z.txt']),
            slice_from_center(data_dict[centri_dir]['Machine']['NORTH-SOUTH.txt'])
        ])
        
        structure_data = np.column_stack([
            slice_from_center(data_dict[centri_dir]['Structure']['EAST-WEST.txt']),
            slice_from_center(data_dict[centri_dir]['Structure']['Z.txt']),
            slice_from_center(data_dict[centri_dir]['Structure']['NORTH-SOUTH.txt'])
        ])
        
        # Concatenate Machine and Structure data
        combined_data = np.column_stack([machine_data, structure_data])
        
        # Convert acceleration measurements (m/s^2) to mm/s^2
        # combined_data *= 1000
        
        # Integrate twice to convert acceleration to displacement
        # velocity = integrate.cumtrapz(combined_data, axis=0, initial=0)
        # displacement = integrate.cumtrapz(velocity, axis=0, initial=0)
        
        # Store the final displacement array in the final_data_dict
        final_data_dict[centri_dir] = combined_data #displacement
    return final_data_dict
    
        
def plot_comparison(final_data_dict, fs=4000, NFFT=2**17):
    # Iterate over each centri_md_*
    for i, centri_dir in enumerate(final_data_dict.keys()):
        # Create a figure for each centri_md_*
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))

        data = final_data_dict[centri_dir]

        # Compare corresponding directions between Machine and Structure
        for j in range(3):
            axs[j].psd(data[:, j], Fs=fs, NFFT=NFFT, label='Machine', color='blue')
            axs[j].psd(data[:, j+3], Fs=fs, NFFT=NFFT, label='Structure', color='red')
            axs[j].set_xlim([1, 100])
            axs[j].set_xlabel('Frequency [Hz]')
            axs[j].legend()
            axs[j].set_title(['EAST-WEST', 'Z', 'NORTH-SOUTH'][j], loc='left')

        fig.suptitle(centri_dir, fontsize=16, x=0.85)

        # Call tight_layout before setting y limits
        plt.tight_layout()

        # Now set y limits
        for ax in axs:
            ax.set_ylim([-150, 10])

        # Save the figure in SVG format
        # plt.savefig(f'{centri_dir}_comparison.svg', format='svg')

        plt.show()




def plot_psd(final_data_dict, fs=4000):
    # Create a figure
    fig, axs = plt.subplots(len(final_data_dict.keys()), 2, figsize=(10, 5 * len(final_data_dict.keys())))
    
    # Iterate over each centri_md_*
    for i, centri_dir in enumerate(final_data_dict.keys()):
        data = final_data_dict[centri_dir]
        
        # First 3 directions for Machine
        for j in range(3):
            axs[i, 0].psd(data[:, j], Fs=fs, label=['EAST-WEST', 'Z', 'NORTH-SOUTH'][j])
        
        # Last 3 directions for Structure
        for j in range(3, 6):
            axs[i, 1].psd(data[:, j], Fs=fs, label=['EAST-WEST', 'Z', 'NORTH-SOUTH'][j-3],color = 'r')
            
        axs[i, 0].set_title(f"{centri_dir} Machine")
        axs[i, 1].set_title(f"{centri_dir} Structure")
        axs[i, 0].legend()
        axs[i, 1].legend()
    
    # Show the plots
    plt.tight_layout()
    plt.show()



def find_peaks(final_data_dict, fs=4000, new_fs=150, nfft=2**17, n_peaks=3):
    # Dictionary to hold the peaks
    peaks_dict = {}

    # Iterate over each centri_md_*
    for centri_dir in final_data_dict.keys():
        data = final_data_dict[centri_dir]
        
        # Take 'NORTH-SOUTH' direction for Machine
        north_south_data = data[:, 2]
        
        # Resample to 100Hz
        num_samples = len(north_south_data) * new_fs // fs
        resampled_data = signal.resample(north_south_data, num_samples)
        
        # Get the PSD
        f, Pxx_den = signal.welch(resampled_data, new_fs, nperseg=nfft)
        
        # Find the peaks in the PSD
        peak_indices = signal.find_peaks(Pxx_den, distance=new_fs)[0]
        
        # Sort the peaks by their heights (energies)
        sorted_peak_indices = peak_indices[np.argsort(Pxx_den[peak_indices])][::-1]
        
        # Only keep the top n_peaks
        if len(sorted_peak_indices) > n_peaks:
            sorted_peak_indices = sorted_peak_indices[:n_peaks]
        
        # Store the peak frequencies and their energies in the peaks_dict
        peaks_dict[centri_dir] = (f[sorted_peak_indices], Pxx_den[sorted_peak_indices])
    
    return peaks_dict


def get_peaks(final_data_dict):
    peaks_dict = find_peaks(final_data_dict)
    for centri_dir, (peak_frequencies, peak_energies) in peaks_dict.items():
        print(f"{centri_dir}:")
        for freq, energy in zip(peak_frequencies, peak_energies):
            print(f"  Frequency: {freq:.2f} Hz, Energy: {energy}")
    return peaks_dict

def plot_comparison_peaks(final_data_dict, peaks_dict, fs=4000, NFFT=2**17):
    # Iterate over each centri_md_*
    for i, centri_dir in enumerate(final_data_dict.keys()):
        # Create a figure for each centri_md_*
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))

        data = final_data_dict[centri_dir]

        # Compare corresponding directions between Machine and Structure
        for j in range(3):
            axs[j].psd(data[:, j], Fs=fs, NFFT=NFFT, label='Machine', color='blue')
            axs[j].psd(data[:, j+3], Fs=fs, NFFT=NFFT, label='Structure', color='red')
            axs[j].set_xlim([1, 100])
            axs[j].set_xlabel('Frequency [Hz]')
            axs[j].legend()
            axs[j].set_title(['EAST-WEST', 'Z', 'NORTH-SOUTH'][j], loc='left')

            # Add vertical lines at the peak frequencies
            peak_frequencies = peaks_dict[centri_dir][0]
            for freq in peak_frequencies:
                axs[j].axvline(x=freq, color='magenta', linestyle='--', alpha=0.5)

            peak_text = "Centrifuges Operating Frequencies:\n" + "\n".join(f"{idx+1}: {freq:.2f} Hz / {freq*60:.2f} RPM" for idx, freq in enumerate(peak_frequencies))

            # Add a text box for the peak frequencies
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            axs[j].text(0.02, 0.02, peak_text, transform=axs[j].transAxes, fontsize=8,
                        verticalalignment='bottom', bbox=props)

        fig.suptitle(centri_dir, fontsize=16, x=0.85)

        # Call tight_layout before setting y limits
        plt.tight_layout(rect=[0, 0, .9, 1])

        # Now set y limits
        for ax in axs:
            ax.set_ylim([-150, 10])

        # Save the figure in SVG format
        plt.savefig(f'{centri_dir}_comparison.svg', format='svg')

        plt.show()
        


data_dict,centri_dirs = load_data()
print(data_dict)
final_data_dict = set_array(centri_dirs)
peaks_dict = get_peaks(final_data_dict)
plot_comparison_peaks(final_data_dict, peaks_dict)

plot_psd(final_data_dict)






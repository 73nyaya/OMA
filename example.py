import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import math, cmath

data_dir = Path.cwd() / 'data'
file_name = data_dir / 'NORTH-SOUTH.txt'

file_path = data_dir / file_name

# Read the file
with open(file_path, 'r') as file:
    # If the data is separated by whitespace and has a regular structure
    acceleration_data = np.loadtxt(file)
    acceleration_data = acceleration_data
# Now `acceleration_data` is a numpy array containing your acceleration data
# print(acceleration_data)


# Plot the data
#plt.figure(figsize=(10, 5))  # Create a new figure with a certain size
#plt.plot(acceleration_data)  # Plot the acceleration data
#plt.title('Acceleration Data Over Time')  # Set the title of the plot
#plt.xlabel('Sample Number')  # Set the x-axis label
#plt.ylabel('Acceleration')  # Set the y-axis label
#plt.grid(True)  # Show grid
#plt.show()  # Display the plot

sampling_freq = 4000
N = len(acceleration_data)
print(N)


delta_t = 1 / sampling_freq
print(delta_t)

# Create a scatter plot
plt.psd(acceleration_data, Fs = 4000, NFFT = 2**17)
plt.xlim([0, 20])
plt.show()
exit()

N1 = int(N/2)
delta_w = 2*np.pi / (N*delta_t)
Y_N={}
S_N=[]
w=np.empty(N1)
print("N1: ",N1)
for k in range(0, N1):
    w[k]=k*delta_w
    sum=0

    for i in range(0,N):
        sum += acceleration_data[i]*cmath.exp(-1j*w[k]*i*delta_t)
    print(sum)
    Y_N[w[k]] = math.sqrt(delta_t/(2*np.pi*N))*sum 
    S_N.append((w[k],(Y_N[w[k]]*Y_N[w[k]].conjugate()).real))
    if k > 377:
        break
print(S_N)

x, y = zip(*S_N)

# Create a scatter plot
plt.plot(x, y)

# Optionally, you can also plot lines connecting the points
plt.plot(x, y)


# Add titles and labels (optional)
plt.title('Plot of Points')

# Show the plot
plt.show()
print("end")
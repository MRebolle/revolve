import matplotlib
from sys import platform
if platform == "darwin":
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from glob import glob
import pandas as pd
from mpl_toolkits import mplot3d
import numpy as np
import os


# Parameters
path = "/home/maarten/projects/revolve-simulator/revolve/output/cpg_bo/main_1556883301/"
var1 = "range_ub"
var2 = "signal_factor"
parameter_file = "parameters.txt"


# Get all sub-directories
path_list = glob(path + "*")
path_list = [path_ for path_ in path_list if os.path.isdir(path_)]
n_dirs = len(path_list)

# Holder
results = np.empty((n_dirs, 3))

# Check if it's numeric:
for ix, path_ in enumerate(path_list):
    try:
        int(path_.split("/")[-1] )
    except:
        continue

    # Get parameters for this file.
    subfolder_list = glob(path_ + "/*/")
    parameters = [(line.rstrip('\n')) for line in open(path_ + "/" + subfolder_list[0].split("/")[-2] +"/" + parameter_file)]
    for param in parameters:
        if(var1 in param):
            results[ix, 0] = float(param.split(":")[-1])
        if(var2 in param):
            results[ix, 1] = float(param.split(":")[-1])

    # Get Fitness. This is an average file in path_
    fitness = ".".join(glob(path_ + "/*.png")[0].split("/")[-1].split(".")[:-1])
    results[ix, 2] = fitness

# Combine results
df = pd.DataFrame(results)
results = df.sort_values(by = [0,1]).to_numpy()

# Prepare for 3D plot
my_size = int(np.sqrt(n_dirs))
X =results[:,0].reshape((my_size,  my_size))
Y =results[:,1].reshape((my_size,  my_size))
Z =results[:,2].reshape((my_size,  my_size))

# Construct 3D plot
fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.set_xlabel(var1)
ax.set_ylabel(var2)
ax.set_zlabel("fitness")
plt.savefig(path + "3Dplot.png")

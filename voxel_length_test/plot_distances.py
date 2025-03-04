'''
plotting csv files for james.
'''

import os
import argparse
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

PARENTDIR = Path(__file__).parent.resolve()
FILEFOLDER = "distance_outputs"

def plot_all(csv_filename):
    '''
    Given a csv with distances, plots the distances.
    '''
    #read
    folder_path = os.path.join(PARENTDIR, FILEFOLDER)

    df = pd.read_csv(folder_path + "/" + csv_filename)

    #start plot
    plottitle = csv_filename[:-4] + " actions"
    plt.title(plottitle)
    plt.ylabel("distances")
    plt.xlabel("steps")

    # get columns
    cols = df.columns.tolist()

    # Test - can we see where there is action by plotting the differential?
    # plot_differentials(df, cols)

    for col in cols:
        to_plot = list(df[col])
        smoothed_data = gaussian_filter1d(to_plot, sigma=1) # Adjust sigma for smoothing strength
        plt.plot(range(len(to_plot)), smoothed_data, label=col)

    #plt.axvline(x=19, color='b', linestyle=':', linewidth=2)
    #plt.axvline(x=31, color='b', linestyle=':', linewidth=2)
    #plt.arrow(x=19, y=1.8, dx=10.3, dy=0, 
    #     width=0.01, head_width=0.05, head_length=2, 
    #     fc='r', ec='r')
    #plt.text(20, 1.7, "12 steps", fontsize=8, color='red')
    plt.legend(loc='upper center')
    plt.savefig(os.path.join(folder_path, plottitle + '.png'))
    plt.close()

def plot_differentials(df, cols):
    for col in cols:
        y = list(df[col])
        x = np.linspace(0, len(y), len(y))
        dy_dx = np.diff(y) / np.diff(x)
        x_mid = (x[:-1] + x[1:]) / 2
        smoothed_data = gaussian_filter1d(dy_dx, sigma=2) # Adjust sigma for smoothing strength
        plt.plot(x_mid, smoothed_data, label="Derivative of " + col)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Numerical Differentiation of Discrete Data')
    plt.legend()
    plt.show()

def get_latest_file():
    """
    Finds the most recently created file in a folder matching a given pattern.
    
    Returns:
        str: The path to the most recently created file, or None if no files match the pattern.
    """
    this_dir = Path(__file__).parent.resolve()
    files = glob.glob(os.path.join(this_dir, FILEFOLDER) + "/*.csv")
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime).split("/")[-1]
    return latest_file


if __name__ == "__main__":

    #args
    PARSER = argparse.ArgumentParser(description="Arguments for simple experiment.")
    PARSER.add_argument("--csv_filename", type=str, default=get_latest_file(),
                        help="The csv file of the robot distances you want to plot.")

    ARGS = PARSER.parse_args()

    plot_all(ARGS.csv_filename)

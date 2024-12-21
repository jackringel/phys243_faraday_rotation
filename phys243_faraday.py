import numpy as np
import matplotlib.pyplot as plt
import math

def read_faraday():
    filename = open('phys243_faraday.csv','r')
    file = filename.read()
    filename.close()
    return file

def plot_malus():
    points = np.arange(90, 465, 15)
    lines = read_faraday().split('\n')[1:]
    vals = []
    for line in lines:
        vals.append(float(line.split(',')[1]))
    plt.scatter(points, vals, color='red', label='Experimental Data')
    xvals = np.linspace(90, 450, 500)
    xvals_rad = np.deg2rad(xvals)
    I0 = 62.45
    yvals = I0 * np.pow(np.cos(xvals_rad), 2)
    plt.plot(xvals, yvals, label=r'Theoretical $I = I_0 \cos^2 \theta$', color='blue')
    plt.xlabel(r'Angle $\theta$ (degrees)')
    plt.ylabel(r'Intensity $I$ (micro-watts)')
    plt.title("Verification of Malus's Law")
    plt.legend()
    plt.grid(True)
    plt.xlim(90, 450)
    plt.ylim(0, I0 * 1.1)
    plt.show()

def plot_r2():
    I0 = 62.45
    lines = read_faraday().split('\n')[1:]
    vals = []
    for line in lines:
        vals.append(float(line.split(',')[1]))
    means = []
    std_errs = []
    response = "a"
    while response:
        response = input('comma-separated indices to lump together: ')
        if response:
            response = response.split(',')
            asdf = []
            for val in response:
                asdf.append(vals[int(val)])
            mean,dev,err = stats(asdf)
            means.append(mean)
            std_errs.append(err)
    xvals = np.arange(0, 105, 15)
    new_xvals = np.pow(np.cos(np.deg2rad(xvals)), 2)
    total_mean = sum(means)/len(means)
    residuals = 0
    for i in range(len(new_xvals)):
        residuals += math.pow(means[i]-I0*new_xvals[i], 2)
    total = 0
    for i in range(len(new_xvals)):
        total += math.pow(means[i]-total_mean,2)
    r2 = 1 - residuals/total
    theoretical_x = np.linspace(0, 90, 100)
    new_x = np.pow(np.cos(np.deg2rad(theoretical_x)), 2)
    theoretical_y = I0 * new_x
    plt.errorbar(new_xvals, means, yerr=std_errs, fmt='o', markersize=2, color='red', label='Experimental Data')
    plt.plot(new_x, theoretical_y, label=r'Theoretical Data', color='blue')
    plt.xlabel(r'$cos^2(\theta)$ (degrees)')
    plt.ylabel(r'Intensity $I$ (micro-watts)')
    plt.title("Curve-Fitting for Malus's Law")
    plt.legend()
    plt.grid(True)
    plt.xlim(0, max(new_xvals))
    plt.ylim(0, I0 * 1.1)
    plt.text(0.05, 0.95, f'$R^2 = {r2:.4f}$', transform=plt.gca().transAxes,
         fontsize=12, verticalalignment='top')
    plt.show()
    

def stats(vals):
    mean = sum(vals)/len(vals)
    deviations = []
    for val in vals:
        deviations.append(math.pow(val-mean,2))
    std_dev = math.sqrt(sum(deviations)/len(vals))
    std_err = std_dev/math.sqrt(len(vals))
    return mean, std_dev, std_err

def graph_verdet():
    lines = read_faraday().split('\n')[17:23]
    bs = []
    angles = []
    errors = []
    for line in lines:
        bs.append(float(line.split(',')[12]))
        angles.append(float(line.split(',')[13]))
        errors.append(float(line.split(',')[14]))
    plt.errorbar(bs, angles, yerr=errors, fmt='o', markersize=2, color="red", label="Experimental Data")
    theoretical_x = np.linspace(0, 257.6, 500)
    theoretical_y = 0.008188485 * theoretical_x #calculated verdet*length from sheet
    plt.plot(theoretical_x, theoretical_y, label=r'Theoretical Data', color='blue')
    plt.xlabel(r'$B$ (gauss)')
    plt.ylabel('Change in Angle (degrees)')
    plt.title('Angle vs. Magnetic Field')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, max(bs))
    plt.ylim(0, max(angles)*1.1)
    plt.text(0.05, 0.95, f'$R^2 = {0.9994:.4f}$', transform=plt.gca().transAxes,
         fontsize=12, verticalalignment='top') #calculated from sheet
    plt.show()

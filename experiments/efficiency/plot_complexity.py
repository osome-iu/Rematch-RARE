import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import ticker
font = {'size':17}
matplotlib.rc('font', **font)
matplotlib.rcParams['figure.dpi'] = 200
import os
import pandas as pd
import numpy as np

def create_log_bin(old_data, x, y, base):
    data = old_data.copy()
    # storing just the integer of the log values unless the value in np.nan
    data[f'int_log{base}({x})'] = [int(np.emath.logn(base, xi)) if xi else np.nan for xi in list(data[x])]
    data[f'{y}_averaged_log{base}({x})'] = np.nan
    # iterating over the unique values of the log integers
    unique_intx = list(data[f'int_log{base}({x})'].unique()) 
    data_bin = {}
    for xi in unique_intx:
        if not np.isnan(xi):
            # getting index of rows where log integer is xi 
            xi_data_idx = data.index[data[f'int_log{base}({x})'] == xi].tolist()
            # collecting and averaging all y values corresponding to the rows where 'int_log{base}({x})' = xi
            data_bin[base**xi] = np.nanmean(data.loc[xi_data_idx, y])
    # if the unique value is nan then the corresponding averaged y value is also nan
    data_bin = pd.DataFrame.from_records(list(data_bin.items()), columns = [f'{x}', f'average {y}'])
    return data_bin

def create_bin(old_data, x, y, base):
    data = old_data.copy()
    # storing just the integer of the log values unless the value in np.nan
    data[f'int_{base}({x})'] = [int(xi/base) if xi else np.nan for xi in list(data[x])]
    data[f'{y}_averaged_{base}({x})'] = np.nan
    # iterating over the unique values of the log integers
    unique_intx = list(data[f'int_{base}({x})'].unique()) 
    data_bin = {}
    for xi in unique_intx:
        if not np.isnan(xi):
            # getting index of rows where log integer is xi 
            xi_data_idx = data.index[data[f'int_{base}({x})'] == xi].tolist()
            # collecting and averaging all y values corresponding to the rows where 'int_log{base}({x})' = xi
            data_bin[base*xi] = np.nanmean(data.loc[xi_data_idx, y])
    # if the unique value is nan then the corresponding averaged y value is also nan
    data_bin = pd.DataFrame.from_records(list(data_bin.items()), columns = [f'{x}', f'average {y}'])
    return data_bin

def calculate_linear_fit(data_, x, y, line_start, line_end):
    data_line_ind = data_.index[(data_[x] >= line_start) & (data_[x] < line_end)].tolist()
    data_line = np.polyfit(data_.loc[data_line_ind, x].tolist(), data_.loc[data_line_ind, y].tolist(), 1)
    data_fit = np.poly1d(data_line)
    print(np.poly1d(data_fit))
    return data_fit

def calculate_loglinear_fit(data_, x, y, line_start, line_end):
    data_line_ind = data_.index[(data_[x] >= line_start) & (data_[x] < line_end)].tolist()
    data_line = np.polyfit(data_.loc[data_line_ind, x].tolist(), data_.loc[data_line_ind, f'log10({y})'].tolist(), 1)
    data_fit = np.poly1d(data_line)
    print(np.poly1d(data_fit))
    return data_fit

def calculate_loglog_fit(data_log, x, y, line_start, line_end):
    data_line_ind = data_log.index[(data_log[f'log10({x})'] >= line_start) & (data_log[f'log10({x})'] < line_end)].tolist()
    data_line = np.polyfit(data_log.loc[data_line_ind, f'log10({x})'].tolist(), data_log.loc[data_line_ind, f'log10({y})'].tolist(), 1)
    data_fit = np.poly1d(data_line)
    print(np.poly1d(data_fit))
    return data_fit

def plot_linear_fit(binned_data, x, y, line_style, line_label):
    # setting the intercept of the line on the x axis (where the curve start to look like a line)
    data_min_x = min(binned_data[x])
    data_max_x = max(binned_data[x])

    # finding the index of rows where x is greater min_x
    data_fit = calculate_linear_fit(binned_data, x, y, data_min_x, data_max_x)
    
    data_min_log10y = data_fit(data_min_x)
    data_max_log10y = data_fit(data_max_x)
    
    plt.plot([data_min_x, data_max_x], [data_min_log10y, data_max_log10y], color = 'black', linestyle = line_style, label = line_label)

def plot_loglinear_fit(ax1, binned_data, x, y, color, line_label):
    # setting the intercept of the line on the x axis (where the curve start to look like a line)
    data_min_x = min(binned_data[x])
    data_max_x = max(binned_data[x])

    # finding the index of rows where x is greater min_x
    data_fit = calculate_loglinear_fit(binned_data, x, y, data_min_x, data_max_x)
    
    data_min_log10y = data_fit(data_min_x)
    data_max_log10y = data_fit(data_max_x)

    ax1.plot([data_min_x, data_max_x], [10**data_min_log10y, 10**data_max_log10y], color = color, linestyle = 'solid')
        

def plot_loglog_fit(data_log, x, y, color):
    # setting the intercept of the line on the x axis (where the curve start to look like a line)
    # data_min_log10x = min(data_log[f'log10({x})'])
    data_min_log10x = 1.5
    data_max_log10x = max(data_log[f'log10({x})'])

    # finding the index of rows where x is greater min_x
    data_fit = calculate_loglog_fit(data_log, x, y, data_min_log10x, data_max_log10x)
    
    # slopes and one point on the line    
    data_min_log10y = data_fit(data_min_log10x)
    data_max_log10y = data_fit(data_max_log10x)
    
    plt.plot([10**data_min_log10x, 10**data_max_log10x], [10**(data_min_log10y-0.25), 10**(data_max_log10y-0.25)], color = color, linestyle = 'solid')


def plot_time_log(args, metric_labels, metric_data):
    x = 'n'
    y = 'time'
    y2 = f'average {y}'
    title = f'{y2} binned {x}'
    file = title.replace(' ','_')
    symbol_styles = ['o','v','s','*','X','D','p']
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']
    # binning and plotting
    for i, data in enumerate(metric_data):
        base = 1.2
        # creating bins
        data_ = create_log_bin(data, x, y, base)
        data_[f'log10({x})'] = np.log10(data_[x])
        data_[f'log10({y2})'] = np.log10(data_[y2])
        data_.to_csv(os.path.join(args.datapath, f"all_{file}_{base}_{metric_labels[i]}_logbin.csv"), index = False)
        data_ = pd.read_csv(os.path.join(args.datapath, f"all_{file}_{base}_{metric_labels[i]}_logbin.csv"))
        plt.plot(data_[x], data_[y2], symbol_styles[i], markersize=8, label = r"$\it{"+metric_labels[i]+"}$", color = colors[i])
        
    for i, metric_label in enumerate(metric_labels):
        if i == 0 or i == 4:
            data_ = pd.read_csv(os.path.join(args.datapath, f"all_{file}_{base}_{metric_label}_logbin.csv"))
            # plot loglog
            plot_loglog_fit(data_, x, y2, colors[i])
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel(r'$N$')
    plt.ylabel(r'average time (seconds)')
    plt.xlim(10**0, 10**2.4)
    plt.legend(loc = 'upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(args.datapath, f'all_{file}_{base}_loglog_plot.png'))
    plt.close()

def plot_search_spaces(args, metric_labels, metric_data):
    x = 'n'
    y = 'search_spaces'
    y2 = f'average {y}'
    title = f'{y2} binned {x}'
    file = title.replace(' ','_')
    symbol_styles = ['o','v','s','*','X','D','p']
    colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']
    fig, ax1 = plt.subplots()
    # binning and plotting
    for i, data in enumerate(metric_data):
        base = 10
        # creating bins
        data_ = create_bin(data, x, y, base)
        # create log10 column
        data_[f'log10({y2})'] = np.log10(data_[y2])
        data_.to_csv(os.path.join(args.datapath, f"all_{file}_{base}_{metric_labels[i]}_bin.csv"), index = False)
        data_ = pd.read_csv(os.path.join(args.datapath, f"all_{file}_{base}_{metric_labels[i]}_bin.csv"))
        ax1.plot(data_[x], data_[y2], symbol_styles[i], markersize=8, label = metric_labels[i], color = colors[i])
    
    # for i,_ in enumerate(metric_labels):
    #     data_ = pd.read_csv(os.path.join(args.datapath, f"all_{file}_{base}_{metric_labels[i]}_bin.csv"))
    #     # plot loglinear
    #     plot_log_linear_fit(ax1, data_, x, y2, colors[i], line_labels[i])
    
    axins = inset_axes(ax1, width='40%', height='40%', loc='lower right', bbox_to_anchor=(-0.5, 0.5, 1, 1), bbox_transform=ax1.transAxes)
    for i,_ in enumerate(metric_labels):
        if i > 1:
            data_ = pd.read_csv(os.path.join(args.datapath, f"all_{file}_{base}_{metric_labels[i]}_bin.csv"))
            # plot loglinear
            axins.plot(data_[x], data_[y2], symbol_styles[i], markersize=5, label = metric_labels[i], color = colors[i])
    # axins.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    axins.set_yscale('log')
    axins.tick_params(axis='x', labelsize=10)
    axins.tick_params(axis='y', labelsize=10)
    ax1.set_yscale('log')
    ax1.set_xlabel(r"$N$")
    ax1.set_ylabel(r'average search space')
    # ax1.legend(loc = 'upper right', bbox_to_anchor=(0.45, 0, 1, 1))
    # mark_inset(ax1, axins, loc1=2, loc2=1)
    fig.savefig(os.path.join(args.datapath, f'all_{file}_{base}_loglinear_plot.png'), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Complexity Plot")
    parser.add_argument('-dp','--datapath', metavar = 'data path', type = str,help = 'Data Path',default = 'data/processed/AMR3.0/')
    args = parser.parse_args()
    metric_labels = ['smatch', 's2match', 'sembleu', 'wlk', 'rematch']
    metric_data = [pd.read_csv(os.path.join(args.datapath, f"all_unwiki_500k_1_{model}_data.csv")) for model in metric_labels]
    # copying rematch 'n' column to 'wlk'
    metric_data[-2]['n'] = metric_data[-1]['n']
    plot_time_log(args, metric_labels, metric_data)
    plot_search_spaces(args, metric_labels, metric_data)

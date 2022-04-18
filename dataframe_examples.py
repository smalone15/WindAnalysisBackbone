import pandas as pd
import datetime as dt
import random
import matplotlib.pyplot as plt
import calendar as cal
import numpy as np
from scipy.stats import pearsonr
from create_datasets import random_data, create_ref_data


def scatter_plot(mast_data: pd.DataFrame, title: str, graph_output: str):
    """
    :param mast_data: full dataset dataframe concat with ref dataset by month
    :param title: name of the dataset
    :param graph_output: output path as a string
    :return:
    """
    # cleaning data first for nans
    mast_data = mast_data.fillna(0)
    plt.figure()
    plt.scatter(mast_data['ref_data'], mast_data['data'], s=1, c='blue')
    plt.rcParams['figure.figsize'] = [10,7]
    plt.xlabel('Reference Wind Speed [m/s]')
    plt.ylabel('Mast Wind Speed [m/s]')
    plt.title(title, fontsize=20)
    # this is causing errors with nans - need them to pass as 0 instead
    z1 = np.polyfit(mast_data['ref_data'], mast_data['data'], 1)
    slope = z1[0]
    intercept = z1[1]
    p1 = np.poly1d(z1)
    plt.plot(mast_data['ref_data'], p1(mast_data['ref_data']), "k-")
    # get r2 values and plot on 5
    rsquared1 = pearsonr(mast_data['ref_data'], mast_data['data'])
    rsquared1 = rsquared1[0]
    r2 = '$R^2={0:.3f}'.format(rsquared1)
    # print the equation of best fit line
    bfline = 'y=' + str(p1)
    lst = [r2, bfline]
    plt.legend(lst, markerscale=0, handletextpad=0, handlelength=0, fontsize='large')
    save_path = f"{graph_output}{title}.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close('all')
    return slope, intercept, rsquared1


def plot_monthly(monthly_concurrent, graph_output, key):
    # Plotting monthly average datasets against each other
    plt.figure()
    plt.plot(monthly_concurrent.index.values, monthly_concurrent['ref_data'], label='Reference')
    plt.plot(monthly_concurrent.index.values, monthly_concurrent['data'], label='Site Data')
    plt.plot(monthly_concurrent.index.values, monthly_concurrent['scaled_data'], label='Adjusted Site Data')
    plt.title('Monthly Average Wind Speed')
    plt.ylabel('Wind Speed [m/s]')
    plt.legend()
    plt.savefig(f"{graph_output}Monthly_Average_{key}.png", bbox_inches='tight')
    plt.clf()

def compile_dfs(reference_dataset, mast_data_dataset):
    """
    This function should create the month columns, sort by day and timestamp and provide the means for each of these
    :param reference_dataset: Pretty self-explanatory, the reference dataset that's used on this mast
    :param mast_data_dataset: Also, the mast dataset that's being used. Only one of the masts should be input here, if
        there are multiple in a site this should be run for each mast with the same ref dataset input each time.
    :return: Output Df with month column, means for each timestamp and cleaned data with nans for missing datapoints
    """
    # This needs to get the correct column. Should be set for a specific input dataset or by column name (using column name here)



    # Setting the month for each timestep
    reference_dataset['Month'] = pd.DatetimeIndex(reference_dataset['datetime']).month
    mast_data_dataset['Month'] = pd.DatetimeIndex(mast_data_dataset['datetime']).month

    # Mean of each day in the dataset ,can also be made to do timesteps if needed
    reference_yearly_avg = reference_dataset.groupby(
        [reference_dataset['datetime'].dt.month, reference_dataset['datetime'].dt.day]).mean()
    mast_yearly_avg = mast_data_dataset.groupby(
        [mast_data_dataset['datetime'].dt.month, mast_data_dataset['datetime'].dt.day]).mean()

    # Make the datatype of month back to int
    mast_yearly_avg['Month'] = mast_yearly_avg['Month'].astype(int)
    reference_yearly_avg['Month'] = reference_yearly_avg['Month'].astype(int)

    # compile the ref data into the mast dataset - avoids using non datapoints,
    #   also cuts out a lot of the reference data if there are missing days in the original dataset
    mast_yearly_avg['ref_data'] = reference_yearly_avg['data']


    return reference_yearly_avg, mast_yearly_avg


# Some random mast data to test with
data_dfs = random_data()

# Add reference datasets to each site
for site_name in data_dfs.items():
    site_name = create_ref_data(site_name)


# This is where the actual dbm tool starts
# The plot func is run for each site
for site in data_dfs.items():
    # the functions here are also run for each mast key in each site, minus the ref_data
    for mast_key in site[1]:
        if mast_key == 'ref_data':
            break
        else:
            df1, site[1][mast_key] = compile_dfs(reference_dataset=site[1]['ref_data'], mast_data_dataset=site[1][mast_key])
            print(f'finished {mast_key}')

        slope, intercept, rsquared = {}, {}, {}
        # merge 2 dataframes for each month, fill in missing pieces of data between them with the NaN, now, hopefully they can be plotted seperately, but passed in the same dataframe into a function and indexed correctly by month?
        for month in site[1][mast_key]['Month'].unique():
            # Plot the current month, doesn't matter which order since unique should run through all of them
            slope[month], intercept[month], rsquared[month] = scatter_plot(
                mast_data=site[1][mast_key][site[1][mast_key]['Month'] == month],
                title=f"Monthly_Correlation - {mast_key}_{cal.month_name[month]}", graph_output="outputs/")

        # sort by month column for monthly means, this should happen after the scatter plot - this is your correlation factor
        mast_dataset = site[1][mast_key].groupby('Month').mean()

        # I want to scale the original data to the ref_data - this part might not be what's correct, but it sounds fun
        mast_dataset['scaled_data'] = (1-((1-(mast_dataset['ref_data']/mast_dataset['data']))/2))*mast_dataset['data']


        plot_monthly(monthly_concurrent=mast_dataset, graph_output="outputs/", key=f"{site[0]}_{mast_key}")

print("Hold Up")




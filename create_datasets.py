import pandas as pd
import random
import numpy as np
import datetime as dt


def random_data():
    site_names = ['Sage Draw', 'Plum Creek', 'Dermott Wind', 'Lockett', 'Helena', 'Haystack']

    # Simulate creation of mast files
    mast_dfs = {}

    # pick site names to use
    rand_sites_num = random.randint(1, 6)
    sites = random.choices(site_names, k=rand_sites_num)

    # Randomly add mast numbers to each site
    for site_name in sites:

        # Randomly make some mast numbers
        mast_list = {}
        for x in range(1, random.randint(2, 5)):
            mast_num = "Mast {0:04}".format(random.randint(0000, 9999))
            mast_list[mast_num] = None
            # add random data for each mast
            for mast in mast_list:
                dates = []
                example_data = []
                starting_date = dt.datetime(year=random.randint(2018, 2020), month=random.randint(1, 12),
                                            day=random.randint(1, 28))
                for x in range(1, random.randint(24 * 180, 24 * 900)):
                    date_to_add = starting_date + x * dt.timedelta(hours=1)
                    dates.append(date_to_add)
                    example_data.append(random.uniform(0, 18))
                    data = {
                        "datetime": dates,
                        'data': example_data,
                    }
                mast_list[mast] = pd.DataFrame(data)

        # Add masts to each site name
        mast_dfs[site_name] = mast_list

    print('Masts Generated')
    return mast_dfs


def create_ref_data(data_structure, **kwargs):
    """
    Made to work with the above function's data structure: for a single site
    :param data_structure: see above description. Data should be setup the same way as in this file
    :return:
    """
    ref_dataframe = kwargs.get('ref_data', None)

    # If no optional ref_dataframe inputted, create a random one
    if ref_dataframe is None:
        #create random dataset
        dates = []
        example_data = []
        starting_date = dt.datetime(year=random.randint(1990, 2020), month=random.randint(1, 12),
                                    day=random.randint(1, 28))
        for x in range(1, random.randint(24 * 365, 24 * 900)):
            date_to_add = starting_date + x * dt.timedelta(hours=1)
            dates.append(date_to_add)
            example_data.append(random.uniform(0, 18))
            data = {
                "datetime": dates,
                'data': example_data,
            }
        data_structure[1]['ref_data'] = pd.DataFrame(data)
    else:
        data_structure[1]['ref_data'] = ref_dataframe


random_dfs = random_data()
print("Hooray!")



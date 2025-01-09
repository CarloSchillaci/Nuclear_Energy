import pandas as pd
import numpy as np

# get dataset file
main_df = pd.read_csv('chernobyl.csv')

# renaming columns and removing the ones that won't be used in the analysis
main_df.columns = ['country', 'country_code', 'locality', 'latitude', 'longitude', 'date', 'end_time', 'duration', 'iodine131', 'caesium134', 'caesium137']
main_df = main_df.drop(columns=['end_time', 'duration'])

# replacing country abreviations with country names
main_df['country'].replace({'AU': 'Austria',
                       'BE': 'Belgium',
                       'CH': 'Switzerland',
                       'CZ': 'Czechoslovakia',
                       'DE': 'Germany',
                       'ES': 'Spain',
                       'F': 'France',
                       'FI': 'Finland',
                       'GR': 'Greece',
                       'HU': 'Hungary',
                       'IR': 'Ireland',
                       'IT': 'Italy',
                       'NL': 'Netherlands',
                       'NO': 'Norway',
                       'SE': 'Sweden',
                       'UK': 'United Kingdom'}, inplace=True)

# changing date column to datetime format
main_df['date']= pd.to_datetime(main_df['date'])

# clearing Iodine 131, Caesium 134 and Caesium 137 columns from incorrect strings that make its dtype = object.
# removing strange '<' strings from columns.
main_df[['iodine131', 'caesium134', 'caesium137']] = main_df[['iodine131', 'caesium134', 'caesium137']].replace('<',np.NaN)
# removing strange 'L' strings from columns.
main_df[['iodine131', 'caesium134', 'caesium137']] = main_df[['iodine131', 'caesium134', 'caesium137']].replace('L',np.NaN)
# removing strange 'L' strings from columns.
main_df[['iodine131', 'caesium134', 'caesium137']] = main_df[['iodine131', 'caesium134', 'caesium137']].replace('L',np.NaN)
# removing strange 'N' strings from columns.
main_df[['iodine131', 'caesium134', 'caesium137']] = main_df[['iodine131', 'caesium134', 'caesium137']].replace('N',np.NaN)

# transforming the columns dtype to numeric.
main_df[['iodine131', 'caesium134', 'caesium137']] = main_df[['iodine131', 'caesium134', 'caesium137']].apply(pd.to_numeric)

# checking dtypes after transformation
main_df[['iodine131', 'caesium134', 'caesium137']].dtypes

# renaming lat and long columns to fix swapped dataset
main_df = main_df.rename(columns={'latitude': 'longitude', 'longitude': 'latitude'})

# swaping lat/long values that are misplaced
main_df[['longitude','latitude']] = main_df[['longitude','latitude']].where(main_df['latitude'] > main_df['longitude'], main_df[['latitude','longitude']].values)

# setting locality and data as our indexes
main_df.set_index(['locality', 'date'], inplace=True)

# creating a new df grouping by those columns and getting the mean values for the numerical columns
avgdates_df = main_df.groupby(['locality','date','country'],sort=False).mean()

# interpolating NaN values
avgdates_int_df = avgdates_df.interpolate(method='linear', axis=0)


# creating new dataframe to get only the countries and isotopes columns
per_country = main_df.reset_index()
per_country = per_country[['country', 'iodine131', 'caesium134', 'caesium137']]
per_country = per_country.groupby(['country']).sum()
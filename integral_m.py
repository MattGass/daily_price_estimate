# firstly, I added 3 column to the excel file as below:
# daily_start: polynomial function value for the first day of each month as well as the last
# day of the previous month
# daily_end: polynomial function value for the last day of each month, as well as first day
# of the next month.
# day_no: day number starting from the first day of the first month to the end of the last month
# ------------------------------ Import Libraries -----------------------------
import datetime
import os  # Miscellaneous operating system interfaces
from functools import reduce
from pathlib import Path
import jalaali
import numpy as np
import pandas as pd  # Python Data Analysis Library
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from python.handlers.config import data_path

# datapath sample: PosixPath('/media/maanib/BE14638A1463450D/pyprojects/customer_analytics/data')
# --------------------------- Read PC2 monthly data ---------------------------
# cwd = Path.cwd()
df = pd.read_excel(
    os.path.join(data_path, 'PC2_monthly2_ahmath.xlsx'),
)
# ---------------- Integral PC2 monthly for finding daily data ----------------
daily_detail = []
for index, row in df.iterrows():
    B = int(row['day_no'])  # last day of the month
    A = int(row['day_no'] - row['weights'] + 1)  # first day of the month

    arr_a = np.array([
        [(pow(B, 3)-pow(A, 3))/3, (pow(B, 2)-pow(A, 2)) /
         2, (B-A)],  # auc (integral value) for the
        # range of (A,B): integral(aX^2+bX+c), X = A to X = B
        [pow(B, 2), B, 1],  # polynomial value (aX^2+bX+c) for X=B
        [pow(A, 2), A, 1]  # polynomial value (aX^2+bX+c) for X=A
    ])
    # results of matrice
    arr_b = np.array([row['PC2'], row['daily_end'], row['daily_start']])
    # multiplication of arr_a * (a, b, c)
    x = np.linalg.solve(arr_a, arr_b)  # calculate a, b, & c
    for i in range(A, B+1):
        daily_detail.append(x[0]*pow(i, 2) + x[1]*i + x[2])
print('')
# -------------------------- Make Dataframe with dates ------------------------
df_daily = pd.DataFrame({
    'date': pd.date_range(
        start=datetime.date(2018, 4, 21),
        end=datetime.date(2020, 11, 20),
        freq='D'
    ),
    'pc2': daily_detail
})
# ------------------------------ Make jalaali dates ---------------------------
df_daily['DateFA'] = 'a'
df_daily['MonthFa'] = 'a'
df_daily['YearFA'] = 'a'
for i, row in df_daily.iterrows():
    # pd.Series(row['DateString'].split('/')).iloc[3]
    a = row['date']
    b = datetime.datetime.strftime(a, "%Y-%m-%d")
    # print(int(b[0:4]), int(b[5:7]), int(b[8:10]))
    Startatdate1 = jalaali.Jalaali.to_jalaali(
        int(b[0:4]), int(b[5:7]), int(b[8:10]))
    Startatdate2 = str(Startatdate1['jy']) + '-' + \
        str(Startatdate1['jm']) + '-' + str(Startatdate1['jd'])
    year = str(Startatdate1['jy'])
    month = str(Startatdate1['jm'])
    df_daily.at[i, 'DateFA'] = Startatdate2
    df_daily.at[i, 'YearFA'] = year
    df_daily.at[i, 'MonthFa'] = month
    # print(date)
print(df_daily.dtypes)
df_daily = df_daily.sort_values(by='date', ascending=True)
# ------------------------------ grouping aggregate ---------------------------
df_monthly = df_daily.groupby(['YearFA', 'MonthFa']).agg(
    {'pc2': 'sum'}
).reset_index()
print(df_monthly.dtypes)
df_monthly_ref = pd.read_excel(
    os.path.join(data_path, 'df_mo_refpc2.xlsx'),
)
df_monthly[['YearFA', 'MonthFa']] = df_monthly[['YearFA', 'MonthFa']].astype(int)
print(df_monthly_ref.dtypes)
df_monthly_compare = pd.merge(
    left=df_monthly, right=df_monthly_ref, how='outer', on=['YearFA', 'MonthFa']
)
r2 = r2_score(df_monthly_compare['PC2_ref'], df_monthly_compare['pc2'])
print(r2)
# ---------------------------------- export data ------------------------------
# df_daily.to_csv(
#     os.path.join((data_path).resolve(), 'df_daily_pc2_integral.csv')
# )

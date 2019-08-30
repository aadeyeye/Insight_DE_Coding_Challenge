import pandas as pd
import numpy as np
import time
tic = time.time()
border_data = pd.read_csv('C:/Users/muyiw/OneDrive/Documents/Insight_DE/Border_Crossing_Entry_Data.csv') #Border_Crossing_Entry_Data

#Fetch border crossing data from csv file
border_data.columns = border_data.columns.str.strip()
border_data = border_data.drop(['Port Name', 'State', 'Port Code'], axis=1)
frame = pd.DataFrame(columns = border_data.columns)

df =  pd.DataFrame(columns = frame.columns)#**************
df['Average'] = np.nan
report =  pd.DataFrame(columns = frame.columns)#**************
avg =  pd.DataFrame(columns = frame.columns)#**************

avg['Average'] = np.nan
report['Average'] = np.nan
msr = list(border_data.Measure.unique())

for y in range(len(msr)):
            frame = border_data.loc[border_data['Measure'].isin([msr[y]])]
            frame = frame.iloc[::-1]
            frame['Average'] = np.nan
            mts = list(frame.Date.unique())
            border = list(frame.Border.unique())
            for m in range(len(mts)):
                for b in range(len(border)):
                    top = frame.loc[frame['Date'].isin([mts[m]])]
                    top = top.loc[top['Border'].isin([border[b]])]
                    sigma = top.Value.sum()
                    top = top.reset_index(drop=True)                        
                    df = df.append(top.iloc[0])
                    df = df.reset_index(drop=True)                        
                    df.Value[-1:] = sigma
#                    df['Date'] = pd.to_datetime(df['Date'])
                    avg = avg.append(df[-1:])
                    avg = avg.sort_index()#values(by='Date') #(by = 'Index'
rollavg = pd.DataFrame(columns = avg.columns)
for i in range(len(msr)):
    for e in range(len(border)):    
        capture = avg.loc[avg['Measure'].isin([msr[i]])]
        capture = capture.loc[capture['Border'].isin([border[e]])]
        capture['Average'] = capture.Value.rolling(5, min_periods = 1).mean().round() #.reset_index(drop = True)               
        rollavg = rollavg.append(capture)
rollavg['Date']= pd.to_datetime(rollavg['Date'])
rollavg = rollavg.sort_values(by = 'Date')
rollavg = rollavg.iloc[::-1]
rollavg = rollavg.reset_index(drop=True) 
save = rollavg.to_csv(r'C:/Users/muyiw/OneDrive/Documents/Insight_DE/report.txt', encoding='utf-8')
print('Runtime is %s minutes' %(round((time.time() - tic)/60)))
                            
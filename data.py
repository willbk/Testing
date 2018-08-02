import numpy as np
import pandas as pd
from datetime import datetime

df = pd.read_csv("USDJPY-2018-03.csv")
df.columns = ['Symbol',"Date","bid","ask"]
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d %H:%M:%S.%f')
df.index = df['Date']
df = df.drop(['Date','Symbol'],axis=1)

df.index.name = None

# t1 = datetime.now()
dfbid = df['bid']
dfspread = df['ask']-df['bid']

dfBidResample = df['bid'].resample('1Min').ohlc()
# appeartly the 00:00:00 means the 00:00:00 to 00:00:01 minutes
dfCloseSpread = dfspread.resample('1Min').ohlc()[['close']]
# dfCloseSpread = pd.DataFrame(dfCloseSpread)
# dt = datetime.now() - t1

# now the dfBidResample and dfCloseSpread is what we want.

dfSave = pd.DataFrame(np.concatenate((dfBidResample.values,dfCloseSpread.values),axis=1),index=dfBidResample.index.values)
columnNames = ['open','high','low','close','lastSpread']
dfSave.columns = columnNames

# now let's check if there is any none in the sequence
# acutally let's check if there is any time interval where a large gap of 2 mins happens.

for i,col in enumerate(columnNames):
    colume = dfSave[col]
    columeValues = colume.values
    nanPosition = np.where(np.isnan(columeValues))
    if np.shape(nanPosition)[1]>0:
        # there there are blanks
        blankString = nanPosition[0]
        # now find out the tuple of _hold = [start missing, end missing]
        missingTuple = []
        skip = False
        for j,pos in enumerate(blankString):

            if skip == False:
                _hold = [pos, None]
            else:
                None

            if j<len(blankString)-1:
                if blankString[j+1] - pos ==1:
                    skip = True
                else:
                    skip = False
                    _hold[1] = pos
                    missingTuple.append(_hold)


# there are a lot of missing values in time steps. I need to selectively clean the values.
# a good way is to check if the missing value exceed a day, which is more than 60*24 =
daySkipThreshold = 60*24
# an ideal format is the starting and the end of the blank as tuples.

missingTuple = np.array(missingTuple)
missDis = missingTuple[:,1] - missingTuple[:,0]

# i thik to generate these trade ready sequences should be Python's work. Python should find the sequence
# that has a nice features that we consider to be an entry point, and then we generate those into our environment.
# for starters I can just use data generated now.

dfSaveCsv = dfSave.ix[:1300]
dfSaveCsv.to_csv('sampleTest.csv')
# so the genrated sequence has to be no gap between.
# somehow I have to put time as a variable in the data.

# however suppose this is the file we want to test on, how should I get the C++ running.
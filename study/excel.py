import csv
from matplotlib import pyplot as plt
from datetime import datetime

filename = 'sitka_weather_2014.csv'

with open(filename,'r',encoding='utf-8') as f:
    reader3 = csv.reader(f)
    header_row = next(reader3)

    highs,dates,lows =[], [],[]
    for row in reader3:
        current_date = datetime.strptime(row[0],'%Y-%m-%d')
        dates.append(current_date)
        highs.append(int(row[1]))
        lows.append(int(row[3]))

    fig = plt.figure(dpi=97,figsize=(13,6))
    plt.plot(dates,highs,c='red',alpha=0.5)
    plt.plot(dates,lows,c='blue',alpha=0.5)
    plt.fill_between(dates,highs,lows,facecolor='blue',alpha=0.1)

    plt.title('daily high temp,july 2014',fontsize=24)
    plt.xlabel('xxx',fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('temp(F)',fontsize=16)
    plt.tick_params(labelsize=16)
    plt.show()
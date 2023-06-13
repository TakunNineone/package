import datetime
str='2023-04-28 22:48:15.325000'
date=datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S.%f')
print(date)
print(int(date.strftime('%Y%m%d%H%M%S%f')))
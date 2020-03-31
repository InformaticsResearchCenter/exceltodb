import pandas
import config

from datetime import datetime, timedelta
from googletrans import Translator
from sqlalchemy import create_engine

def openFile():
    dataframe = pandas.read_excel(io=config.filename, sheet_name=0)
    return dataframe

def dataframeToDB(dataframe):
    dataframe.to_sql(name=config.table_name, con=dbConnect(), if_exists='append', index=False)

def setDefaultEmail(dataframe, emailcolumn):
    dataframe[emailcolumn]='default@email.com'
    return dataframe

def setTrxID(dataframe, trxidcolumn):
    bulan = datetime.now().strftime('%m')
    tahun = datetime.now().strftime('%Y')[2:]
    dataframe[trxidcolumn]=dataframe[trxidcolumn].str[:-4]+bulan+tahun
    return dataframe

def setTrxAmount(dataframe, trxamountcolumn):
    dataframe[trxamountcolumn]=7500000
    return dataframe

def setExpiredDate(dataframe, expireddatecolumn):
    inputData=True
    while inputData:
        print('Masukkan Tahun, Bulan dan Tanggal Expired\nContoh:\nTahun: 2020\nBulan: 10\nHari: 10\n')
        years=input('Tahun: ')
        months=input('Bulan: ')
        days=input('Hari: ')
        try:
            expired_date=datetime(year=int(years), month=int(months), day=int(days)).strftime('%Y-%m-%d')
            dataframe[expireddatecolumn] = expired_date
            inputData=False
            return dataframe
        except Exception as e:
            translate = Translator()
            print(translate.translate(str(e), dest="id").text+'\n')

def setExpiredTime(dataframe, expiredtimecolumn):
    print('\nMasukkan Jam, Menit, dan Detik Expired\n')
    hours=input("Jam:")
    minutes=input("Menit:")
    seconds=input("Detik:")
    expired_time=timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    dataframe[expiredtimecolumn] = str(expired_time)
    return dataframe

def dbConnect():
    engine=create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user=config.db_username,pw=config.db_password,db=config.db_name))
    return engine

def matchTrxwithVA(dataframe, trxidcolumn, virtualaccountcolumn):
    data=[]
    for i in dataframe[trxidcolumn]:
        for j in dataframe[virtualaccountcolumn]:
            npm_trxid=i.split('-')[2]
            npm_va=str(j)[-7:]
            if npm_trxid[0] != 1:
                npm_start=npm_trxid[0]
                npm_end=npm_trxid[1]
                npm_trxid=npm_end+npm_start+npm_trxid[2:]
            if npm_trxid == npm_va:
                data.append('match')
    return len(data)

def removeUnname(dataframe):
    dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed')]
    return dataframe
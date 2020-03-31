import exceltodb

df=exceltodb.openFile()
if df.index.stop == exceltodb.matchTrxwithVA(df, trxidcolumn='trx_id', virtualaccountcolumn='virtual_account'):
    df=exceltodb.removeUnname(df)
    exceltodb.setDefaultEmail(df, 'customer_email')
    exceltodb.setTrxID(df, 'trx_id')
    exceltodb.setExpiredDate(df, 'expired_date')
    exceltodb.setExpiredTime(df, 'expired_time')
    exceltodb.setTrxAmount(df, 'trx_amount')
    exceltodb.dataframeToDB(df)
else:
    print('DATA NOT MATCH')
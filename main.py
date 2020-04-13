import pandas as pd
import pymysql, config

def dbConnectSiap():
    db=pymysql.connect(config.db_host_siap, config.db_username_siap, config.db_password_siap, config.db_name_siap)
    return db

def openFile():
    dataframe = pd.read_excel(io='va.xlsx', sheet_name=0)
    pd.set_option('display.max_columns', 5)
    return dataframe

def getStudentData(studentid):
    db=dbConnectSiap()
    sql='select Nama, HandphoneOrtu, EmailOrtu from simak_mst_mahasiswa where MhswID={studentid}'.format(studentid=studentid)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            ret=rows
        else:
            ret=''
    return ret

def cekNumber(row):
    studentid=row['trx_id'].split("-")[2]
    print('On Proccess: {studentid}'.format(studentid=studentid))
    data=getStudentData(studentid=studentid)
    if row['customer_phone']==data[1]:
        ret=True
    else:
        ret=False
    return ret

def setNumber(row):
    studentid = row['trx_id'].split("-")[2]
    print('On Proccess Set Phone Number: {studentid}'.format(studentid=studentid))
    data=getStudentData(studentid=studentid)
    return data[1]

df=openFile()
df['isPhoneNumber']=df.apply(cekNumber, axis=1)
phonetrue=df.loc[df['isPhoneNumber']==True]
phonefalse=df.loc[df['isPhoneNumber']==False]
phonefalse['customer_phone']=df.apply(setNumber, axis=1)
df_fix=pd.concat([phonetrue, phonefalse])
pd.set_option('display.max_columns', 3000)
df_fix['isPhoneNumber']=df_fix.apply(cekNumber, axis=1)
truekek=df_fix.loc[df_fix['isPhoneNumber']==True]
print(len(truekek))
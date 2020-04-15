import pandas as pd
import pymysql, config
import time

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

def normalizePhonenumber(num):
    if num is not None:
        num = num.replace('â','')
        num = num.replace('€','')
        num = num.replace('¬','')
        num = num.replace(' ','')
        num = num.replace('!', '')
        num = num.replace('#', '')
        num = num.replace('$', '')
        num = num.replace('%', '')
        num = num.replace('^', '')
        num = num.replace('&', '')
        num = num.replace('*', '')
        num = num.replace('(', '')
        num = num.replace(')', '')
        num = num.replace('-', '')
        num = num.replace('_', '')
        num = num.replace('+', '')
        num = num.replace('=', '')
        num = num.replace('[', '')
        num = num.replace(']', '')
        num = num.replace('{', '')
        num = num.replace('}', '')
        num = num.replace('|', '')
        num = num.replace(';', '')
        num = num.replace(':', '')
        num = num.replace("'", '')
        num = num.replace('"', '')
        num = num.replace('<', '')
        num = num.replace('>', '')
        num = num.replace(',', '')
        num = num.replace('.', '')
        num = num.replace('?', '')
        num = num.replace('/', '')
        num = num.replace('`', '')
        num = num.replace('~', '')
        num = num.replace('@', '')
        num=num.strip()
    return num

def normalizeEmail(email):
    if email is not None:
        email = email.replace('¬', '')
        email=email.replace('â', '')
        email=email.replace('€', '')
        email=email.replace(' ', '')
        email=email.replace('!', '')
        email=email.replace('#', '')
        email=email.replace('$', '')
        email=email.replace('%', '')
        email=email.replace('^', '')
        email=email.replace('&', '')
        email=email.replace('*', '')
        email=email.replace('(', '')
        email=email.replace(')', '')
        email=email.replace('-', '')
        email=email.replace('_', '')
        email=email.replace('+', '')
        email=email.replace('=', '')
        email=email.replace('[', '')
        email=email.replace(']', '')
        email=email.replace('{', '')
        email=email.replace('}', '')
        email=email.replace('|', '')
        email=email.replace(';', '')
        email=email.replace(':', '')
        email=email.replace("'", '')
        email=email.replace('"', '')
        email=email.replace('<', '')
        email=email.replace('>', '')
        email=email.replace(',', '')
        email=email.replace('.', '')
        email=email.replace('?', '')
        email=email.replace('/', '')
        email=email.replace('`', '')
        email=email.replace('~', '')
        email=email.strip()
    return email

def setName(row):
    studentid = row['trx_id'].split("-")[2]
    print('On Proccess Set Name: {studentid}'.format(studentid=studentid))
    data=getStudentData(studentid=studentid)
    if data[0] is None or data[0] is 'NULL':
        ret='NULL'
    else:
        ret=normalizePhonenumber(data[0])
    return ret

def setNumber(row):
    studentid = row['trx_id'].split("-")[2]
    print('On Proccess Set Phone Number: {studentid}'.format(studentid=studentid))
    data=getStudentData(studentid=studentid)
    if data[1] is None or data[1] is 'NULL':
        ret='NULL'
    else:
        ret=normalizePhonenumber(data[1])
    return ret

def setEmail(row):
    studentid = row['trx_id'].split("-")[2]
    print('On Proccess Set E-mail: {studentid}'.format(studentid=studentid))
    data=getStudentData(studentid=studentid)
    if data[2] is None or data[2] is 'NULL':
        ret='NULL'
    else:
        ret=normalizeEmail(data[2])
    return ret

start=time.time()
df=openFile()
df['customer_name']=df.apply(setName, axis=1)
print("Finish Set Name")
df['customer_phone']=df.apply(setNumber, axis=1)
print("Finish Set Phone Number")
df['customer_email']=df.apply(setEmail, axis=1)
print("Finish Set E-mail")
end=time.time()

print('Time Execution: {time} Seconds'.format(time=end-start))

print(df[['customer_name', 'customer_phone', 'customer_email']])

# df['isPhoneNumber']=df.apply(cekNumber, axis=1)
# phonetrue=df.loc[df['isPhoneNumber']==True]
# phonefalse=df.loc[df['isPhoneNumber']==False]
# phonefalse['customer_phone']=df.apply(setNumber, axis=1)
# df_fix=pd.concat([phonetrue, phonefalse])
# df_fix['isPhoneNumber']=df_fix.apply(cekNumber, axis=1)
# truekek=df_fix.loc[df_fix['isPhoneNumber']==True]
# pd.set_option('display.max_rows', 3000)
# print(truekek['customer_phone'])
from urllib import parse as urlparse

from sqlalchemy import create_engine

from models import RpcParam

# 테스트DB
# server = '192.168.250.108,1433'
# database = 'ERPDHENT'
# username = 'sa'
# password = 'Ict2022@_!'
# 실DB
server = 'data.egibiz.co.kr'
database = 'LEXCO'
username = 'EGIERPDB'
password = 'rla994869!'
params = urlparse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

def common_rpc_call(models: RpcParam):
    global cursor
    try:
        connection = engine.raw_connection()
        cursor = connection.cursor()
        operation = f'EXEC {models.rpc_id} '
        for i, v in enumerate(models.param):
            if i == 0:
                operation = operation + f'?'
            else:
                operation = operation + f', ?'
        operation = operation.rstrip()
        cursor.execute(operation, models.param)
        r = [dict((cursor.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cursor.fetchall()]
        if models.is_one == 1:
            r = r[0] if len(r) else r
        connection.commit()
        cursor.close()
        return {
            'result': r,
            'msg': 'OK',
            'detail': 'OK',
        }
    except Exception as e:
        cursor.close()
        return {
            'result': '',
            'msg': 'Fail',
            'detail': f'{e}',
        }

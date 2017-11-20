import psycopg2


def connect(connection_string):
    conn_string = connection_string
    return psycopg2.connect(conn_string);


def copy(con, schema='public', table='table', s3bucket='bucket_name', s3key='key', redshift_role='role'):
    sql = """COPY """ + schema + """.""" + table + """
                FROM 's3://""" + s3bucket + """/""" + s3key + """'
                IAM_ROLE '""" + redshift_role + """'
                REMOVEQUOTES
                DELIMITER '|';
                COMMIT;"""

    cur = con.cursor()
    cur.execute(sql)


def unload(con, s3bucket='bucket_name', s3key='key', redshift_role='role', sql_transform=''):
    sql = """UNLOAD ('""" + sql_transform + """')
                TO 's3://""" + s3bucket + """/""" + s3key + """'
                IAM_ROLE '""" + redshift_role + """'
                ADDQUOTES;
                COMMIT;"""

    cur = con.cursor()
    cur.execute(sql)

def execute_ddl(con, ddl):
    sql = ddl
    cur = con.cursor()
    cur.execute(sql)


def close_connection(con):
    con.close()

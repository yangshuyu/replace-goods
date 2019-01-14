import os
from sqlalchemy import create_engine, exc, text as sql_text
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import io
import logging
logger = logging.getLogger('db_utils')

REDSHIFT_DB_URL = os.environ.get('REDSHIFT_DB_URL') or 'postgresql://cm_yangshuyu:6m48jNDBEfE6FPtk@172.31.0.231:5439/cmdata_new'
SERVERDB_DB_URL = os.environ.get('SERVERDB_DB_URL') or 'postgresql://:@127.0.0.1:5432/cmdata_new_dev'
# SERVERDB_DB_URL = os.environ.get('SERVERDB_DB_URL')

assert REDSHIFT_DB_URL != None, 'Redshift URL == None'
assert SERVERDB_DB_URL != None, 'Django DB URL == None'


INDEX_SQL = {
    "rep2_item_store_date_": ['CREATE INDEX rep2_{cmid}_item_store_date_idx ON rep2_item_store_date_{cmid} ("foreign_item_id", "date");']
}

def get_df(db_url, query):
    engine = create_engine(db_url)
    con = engine.connect()
    try:
        return pd.read_sql_query(sql_text(query), con=engine)
    except exc.SQLAlchemyError as e:
        print(e)
    finally:
        con.close()


def set_df(db_url, df, databases):
    engine = create_engine(db_url)
    con = engine.connect()
    try:
        df.to_sql(databases, con=engine, if_exists='replace', index=False)
    except exc.SQLAlchemyError as e:
        print(e)
    finally:
        con.close()


def append_set_df(db_url, df, databases):
    engine = create_engine(db_url)
    con = engine.connect()
    try:
        df.to_sql(databases, con=engine, if_exists='append', index=False)
    except exc.SQLAlchemyError as e:
        print(e)
    finally:
        con.close()


# def exist_df(db_url, databases):
#     engine = create_engine(db_url)
#     Base = declarative_base()
#     Base.metadata.reflect(engine)
#     tables = Base.metadata.tables
#     if databases in tables.keys():
#         return True
#     else:
#         return False


def exist_df(db_url, table):
    engine = create_engine(db_url)
    con = engine.connect()
    try:
        sql1 = "select * from to_regclass('{table}')".format(table=table)
        table_exist = con.execute(sql_text(sql1)).fetchall()
        return table_exist[0][0]
    except exc.SQLAlchemyError as e:
        print(e)
    finally:
        con.close()


def write_to_table(df, table_name, db_url, if_exists='replace'):
    db_engine = create_engine(db_url)# 初始化引擎
    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep='|', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
                               index=False, if_exists=if_exists,schema = '')
    table.create()
    string_data_io.seek(0)
    string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            cmid = table_name.split('_')[-1]
            tname = '_'.join(table_name.split('_')[:-1])
            if tname in INDEX_SQL:
                for _sql in INDEX_SQL[tname]:
                    cursor.execute(_sql.format(cmid=cmid))
            copy_cmd = "COPY %s FROM STDIN WITH DELIMITER '|' CSV" %table_name
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()


def append_to_table(df, table_name, db_url, if_exists='append'):
    try:
        db_engine = create_engine(db_url)# 初始化引擎
        string_data_io = io.StringIO()
        df.to_csv(string_data_io, sep='|', index=False)
        string_data_io.seek(0)
        string_data_io.readline()  # remove header
        with db_engine.connect() as connection:
            with connection.connection.cursor() as cursor:
                copy_cmd = "COPY %s FROM STDIN WITH DELIMITER '|' CSV" %table_name
                cursor.copy_expert(copy_cmd, string_data_io)
            connection.connection.commit()
    except Exception as e:
        logger.info(e)
        logger.exception(e)
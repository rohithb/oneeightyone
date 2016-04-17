from query_preprocessing.helper import operator_lookup
from django.db import connection

def prepare_query(queryType, selectors, constraints, dbtable):
    sql = 'SELECT '
    if queryType == 'LIST':
        for sel in selectors:
            sql = sql + sel + ', '
    elif queryType == 'COUNT':
        sql = 'SELECT COUNT(*) '
    elif queryType =='SUM':
        for sel in selectors:
            sql = sql + 'SUM('+sel+'), '
    elif queryType =='AVG':
        for sel in selectors:
            sql = sql + 'AVG('+sel+'), '
    sql = sql.rstrip(', ')
    sql = sql +' FROM '+ dbtable + ' WHERE '
    for orPart in constraints:
        if 'AND' in orPart:
            for andPart in orPart['AND']:
                sql = sql + andPart['attribute'] + operator_lookup[andPart['relation']] + andPart['value']
                sql = sql + ' AND '
            sql = sql.rstrip('AND ')
        else:
            sql = sql + orPart['attribute'] + operator_lookup[orPart['relation']] + orPart['value']
            sql = sql + ' OR '
        sql = sql.rstrip('OR ')
    return sql

def execute_query(sql_query):
    cursor = connection.cursor()
    cursor.execute(sql_query)
    columns = [col[0] for col in cursor.description]
    results =  cursor.fetchall()
    return columns, results
    
import sqlite3

class db_connection:
    # todo 1: transaction
    # todo 2: more (select) generalization (specific column, range)
    # todo 3: prompt message
    # todo 4 update
    # todo 5: order or use pandas?
    # todo 6: UNIQUE CONSTRAINT Exception
    # todo 7: auto_increment

    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)
    
    def __del__(self):
        self.__conn.close()
    
    def __process(self, statement):
        '''
        '''
        if isinstance(statement, str):
            # print("original statement: ", statement)
            # tmp = '"' + statement + '"'
            # print("tmp: ", tmp)
            return '"' + statement + '"'
        return str(statement)

    def insert(self, table, values):
        sql = 'INSERT INTO ' + table + ' VALUES('
        if values:
            for item in values[:-1]:
                sql += self.__process(item) + ','
            sql = sql + self.__process(values[-1]) + ')'
            print(sql)
            self.__conn.execute(sql)
            self.__conn.commit()
        else:
            print('Nothing to insert')
    
    def select(self, table, **kwargs):
        sql = 'SELECT * FROM ' + table
        if kwargs:
            sql = sql + ' WHERE '
            for key, value in kwargs.items():
                sql += key + '=' + self.__process(value) + ' AND '
            sql = sql[:-5]
        return list(self.__conn.execute(sql))
    
    def update(self, table, condtion_key=None, condtion_value=None, **kwargs):
        if not kwargs:
            print('Nothing to update.')
        return
        sql = ' UPDATE ' + table + ' SET '
        for key, value in kwargs.items():
            sql = sql + key + '=' + self.__process(value) + ' AND '
        sql = sql[:-5] + ' WHERE ' + condtion_key + '='
        if isinstance(condtion_value, str):
            sql += self.__process(condtion_value)
        self.__conn.execute(sql)
        self.__conn.commit()
    
    def delete(self, table, **kwargs):
        sql = 'DELETE FROM ' + table
        # print("kwargs: ", kwargs)
        if kwargs:
            sql = sql + ' WHERE '
            for key, value in kwargs.items():
                # print("type: ", type(value))
                sql += key + '=' + self.__process(value) + ' AND '
                # sql += key + '=' + value + ' AND '
            # print("sql before slice: ",  sql)
            sql = sql[:-5]
            # print("delete sql: ", sql)
        self.__conn.execute(sql)
        self.__conn.commit()


def sqlhelper(table, operation, cond:dict):
    conn = db_connection('db_comp0066.db')
    if operation == 'insert':
        values = ([i for i in cond.values()][0])
        result = conn.insert(table, values)
    elif operation == 'select':
        result = conn.select(table, **cond)
        return result
    elif operation == "update":
        result = conn.update(table, **cond)
    elif operation == 'delete':
        result = conn.delete(table, **cond)
    del conn


# test for drug CRUD

sql_result = sqlhelper('drug', 'select', {'drug_id':'2'})

sqlhelper('drug', 'insert', {'values':[3, 'name', 'dosage', 'frequency']})

sqlhelper('drug', 'delete', {'drug_id':4})


# test for gp insert

sqlhelper('gp', 'insert', {'values':[2, 'Kris', 'Oz', 'male', '2020-12-10', 'abc@d.com', '123456', '2020-12-10 10:00', 100, 1, 1]})

print(sql_result)
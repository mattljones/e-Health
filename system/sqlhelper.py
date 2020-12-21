import sqlite3
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))
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
    conn = db_connection('database/db_comp0066.db')
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

# sql_result = sqlhelper('drug', 'select', {'drug_id':'2'})
# print(sql_result)

# sqlhelper('drug', 'insert', {'values':[3, 'name', 'dosage', 'frequency']})

# sqlhelper('drug', 'delete', {'drug_id':4})


# test for gp
# sql_result = sqlhelper('gp', 'select', {'gp_id':'17'})


from system import utils

# ad_p = utils.hash_salt('root@EH_24').hex()

# sqlhelper('admin', 'insert', {'values':[1, 'Admin', 'Admin', 'not known', '1990-01-01', 'admin@ehealth.com', ad_p, '2020-12-20 17:35:12']})

# for i in range(19, 55):
#     sqlhelper('gp', 'delete', {'gp_id':i})
#     print("GP (id: )" + str(i) + "has been deleted")


# hg_p = utils.hash_salt('Lumos#9Reparo').hex()
# rw_p = utils.hash_salt("wizard'schess100").hex()
# hp_p = utils.hash_salt('Expecto^Patronum7').hex()

# sqlhelper('patient', 'insert', {'values':[51, 16, 'Hermione', 'Granger', 'female', '1979-09-19', 'hermione.g@gryffindor.com', hg_p, '2020-12-20 13:11:05', 'yes', 'yes', 'confirmed']})

# sqlhelper('patient', 'insert', {'values':[52, 16, 'Ron', 'Weasley', 'male', '1980-03-01', 'ron.w@weasley.com', rw_p, '2020-12-20 13:15:05', 'yes', 'yes', 'confirmed']})

# sqlhelper('patient', 'insert', {'values':[53, 17, 'Harry', 'Potter', 'male', '1980-07-31', 'harry.potter@hogwarts.com', hp_p, '2020-12-20 13:21:06', 'yes', 'yes', 'confirmed']})




# sql_result = sqlhelper('patient', 'select', {'patient_id':'51'})
# print(sql_result)


# lp_p = utils.hash_salt('ferment1858').hex()
# ej_p = utils.hash_salt('17@vaCCi*98').hex()
# jl_p = utils.hash_salt('anti&1865/septic').hex()

# sqlhelper('gp', 'insert', {'values':[16, 'Louis', 'Pasteur', 'male', '1822-12-27', 'louis.p@gmail.com', lp_p, '2020-12-20 12:31:31', 3, 1, 1, 'active']})

# sqlhelper('gp', 'insert', {'values':[17, 'Edward', 'Jenner', 'male', '1749-05-17', 'edward.j@msn.com', ej_p, '2020-12-20 12:32:50', 2, 2, 2, 'active']})

# sqlhelper('gp', 'insert', {'values':[18, 'Joseph', 'Lister', 'male', '1827-04-05', 'joseph.l@outlook.com', jl_p, '2020-12-20 12:49:24', 5, 5, 3, 'active']})

# sqlhelper('gp', 'delete', {'gp_id':16})
# sqlhelper('gp', 'delete', {'gp_id':17})
# sqlhelper('gp', 'delete', {'gp_id':18})
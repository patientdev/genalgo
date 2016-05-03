import sqlite3


class ResultsDatabase(object):

    TABLE_NAME = 'genalgo_results'
    TABLE_COLUMNS = ['given_number INT', 'duration REAL', 'successful_sequence TEXT', 'generations INT']

    def __init__(self):
        self.conn = sqlite3.connect('results.db')
        self.cur = self.conn.cursor()

        try:
            self.cur.execute('CREATE TABLE {table_name} ({table_columns})'.format(table_name=ResultsDatabase.TABLE_NAME, table_columns=', '.join(ResultsDatabase.TABLE_COLUMNS)))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            pass

    def insert_results(self, results={'given_number': 0, 'duration': 0.0, 'successful_sequence': '0110', 'generations': 0}):
        self.cur.execute("INSERT INTO {table_name} VALUES ({given_number}, {duration}, '{successful_sequence}', {generations})".format(table_name=ResultsDatabase.TABLE_NAME, given_number=results['given_number'], duration=results['duration'], successful_sequence=results['successful_sequence'], generations=results['generations']))

        self.conn.commit()

        return self.cur

    def __del__(self):
        self.conn.close()
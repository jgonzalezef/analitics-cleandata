import mysql.connector
class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.connect()

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, values=None):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
                self.connection.commit()
                cursor.close()
            except mysql.connector.Error as e:
                print(f"Error executing query: {e}")
                return None

    def execute_read_query(self, query):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
            except mysql.connector.Error as e:
                print(f"Error executing query: {e}")
                return None

    def create_record(self, table, columns, values):
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(values))})"
        self.execute_query(query, values)

    def read_records(self, table, columns=None, condition=None):
        query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_read_query(query)

    def update_record(self, table, new_values, condition):
        set_values = ', '.join([f"{key}='{value}'" for key, value in new_values.items()])
        query = f"UPDATE {table} SET {set_values} WHERE {condition}"
        print(query)
        self.execute_query(query)

    def delete_record(self, table, condition):
        query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query)

    

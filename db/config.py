import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DB:
    con = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv("DB_PORT"),
    )

    cur = con.cursor()

    def select(self):
        fields = ','.join(self.fields) if self.fields else '*'
        table_name = self.__class__.__name__.lower()
        query = f"""select {fields} from {table_name}"""
        self.cur.execute(query)
        return self.cur

    def insert_into(self, **params):
        fields = ','.join(params.keys())
        values = tuple(params.values())
        table_name = self.__class__.__name__.lower()
        query = f"""insert into {table_name}({fields}) values ({','.join(['%s'] * len(params))})"""
        self.cur.execute(query, values)
        self.con.commit()

    def update(self, qrcode_id: str, **kwargs):
        table_name = self.__class__.__name__.lower()
        f = list(kwargs.keys())
        f.append(' ')
        set_fields = " = %s,".join(f).strip(', ')
        params = list(kwargs.values())
        params.append(qrcode_id)
        query = f"""update {table_name} set {set_fields} where id=%s"""
        self.cur.execute(query, params)
        self.con.commit()
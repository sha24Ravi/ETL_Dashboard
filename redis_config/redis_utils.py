import redis, pickle
from databricks import sql
import pandas as pd


class redis_config:
    def __init__(self):
        self.redis_config={'host':'localhost', 'port':6379, 'db':0}
        self.DataBricks_config={'server_hostname':'', 'http_path':'', 'access_token':''}
        self.key="chur_datase"
        self.ttl=86400

    def save_to_redis(self,df):
        r= redis.Redis(host=self.redis_config['host'],
                       port=self.redis_config['port'],
                       db=self.redis_config['db'])
        r.set(name=self.key,value=pickle.dumps(df),ex=self.ttl)


    def load_from_redis(self):
         r= redis.Redis(host=self.redis_config['host'],
                       port=self.redis_config['port'],
                       db=self.redis_config['db'])
         data= r.get(self.key)
         if data:
              data=pickle.loads(data)
              df = pd.DataFrame(data)
              return df
         else:
             return None

    def load_from_databricks(self):
        conn= sql.connect(server_hostname=self.DataBricks_config['server_hostname'],
                          http_path=self.DataBricks_config['http_path'],
                          access_token=self.DataBricks_config['access_token'])
        query = f"SELECT * FROM workspace.churn_schema.churn_dataset limit 300"
        with conn.cursor() as cursor:
          cursor.execute(query)
          result = cursor.fetchall()
          columns = [col[0] for col in cursor.description]
          df = pd.DataFrame(result, columns=columns)
        conn.close()
        return df          
    
    def load_churn_data(self):
        data= self.load_from_redis()
        if data is None:
         print("databricks")
         df = self.load_from_databricks()
         self.save_to_redis(df)
         return df
        else:
            print("redis")
            return data
        
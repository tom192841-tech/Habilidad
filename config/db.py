from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:@localhost/fastapi_db")

meta = MetaData()

conn = engine.connect()
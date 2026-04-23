import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://srJ4FHEkidWpp2C.root:4FoxBli4jvgz3hzx@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test"

engine = create_engine( 
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ssl_ca": "ca.pem"
        }
    }
    )

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
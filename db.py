from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+mysqldb://srJ4FHEkidWpp2C.root:4FoxBli4jvgz3hzx@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test?ssl_mode=VERIFY_IDENTITY&ssl_ca=<CA_PATH>"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl":{
            "ssl":True
        }
    }
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base
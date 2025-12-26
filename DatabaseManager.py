from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from tables import Base, GameInfo, PlayerInfo, Decisions, Nation
import sqlalchemy
import oracledb
import os

class DatabaseManager:
    def __init__(self):
        try:
            load_dotenv()
            DB_USER = "ADMIN"
            DB_PASSWORD = os.environ.get("DB_PASSWORD")
            HOST = "adb.eu-stockholm-1.oraclecloud.com"
            PORT = "1521"
            SERVICE_NAME = "ge72a74000425b4_ecgame_tp.adb.oraclecloud.com"
            DB_CONNECT_STRING = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.eu-stockholm-1.oraclecloud.com))(connect_data=(service_name=ge72a74000425b4_ecgame_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'
            connection_url = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{SERVICE_NAME}"
            self.conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_CONNECT_STRING)

            self.engine: sqlalchemy.Engine = create_engine("oracle+oracledb://", creator= lambda: self.conn, echo=True)
            print("Successfully connected to the database")
                    
        except Exception as e:
            print(f"There was an error while trying to connect to the database: {e}")

    def create_all_tables(self):
        Base.metadata.create_all(self.engine)
    
    def drop_all_tables(self):
        Base.metadata.drop_all(self.engine)
    
    def initiate_new_game(self):
        new_game: GameInfo = GameInfo()
        with Session(self.engine) as session:
            session.add(new_game)
            session.commit()
            print("Initiated a new game")
    
    def add_new_player(self, user_id, game_id: int, leader_name: str, nation_name: str):
        new_nation = Nation(
            decisions=Decisions()
        )



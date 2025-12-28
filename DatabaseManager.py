from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from tables import Base, GameInfo, PlayerInfo, Decisions, Nation
import pandas as pd
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
        ## TODO add some safeguards
        new_game: GameInfo = GameInfo()
        with Session(self.engine) as session:
            session.add(new_game)
            session.commit()
            print("Initiated a new game")
    
    def add_new_player(self, user_id, game_id: int, leader_name: str, nation_name: str):
        new_player_info = PlayerInfo(game_id=game_id, user_id=user_id, leader_name=leader_name, nation_name=nation_name)
        new_decisions = Decisions(game_id=game_id, user_id=user_id, round_id=0)
        new_nation = Nation(
            decisions=new_decisions,
            player_info=new_player_info,
            game_id=game_id,
            user_id=user_id,
            round_id=0
        )
        with Session(self.engine) as session:
            session.add(new_nation)
            session.commit()
            print(f"Added a player {user_id} to game {game_id}")

    def fetch_nations_as_pd_dataframe(self, game_id: int|None = None, user_id: int|None = None, round_id: int|None = None) -> pd.DataFrame:
        statement = sqlalchemy.select(Nation)
        if game_id is not None:
            statement = statement.where(Nation.game_id == game_id)
        if user_id is not None:
            statement = statement.where(Nation.user_id == user_id)
        if round_id is not None:
            statement = statement.where(Nation.round_id == round_id)
        return pd.read_sql_query(statement, self.engine)

    def fetch_active_game_id(self, user_id) -> int|None:
        statement = sqlalchemy.select(PlayerInfo.game_id).where(PlayerInfo.user_id == user_id, PlayerInfo.is_active == True)
        with Session(self.engine) as session:
            game_id: int|None = session.execute(statement).scalar()
        return game_id
    
    def fetch_player_info_as_pd_dataframe() -> pd.DataFrame:
        pass
        
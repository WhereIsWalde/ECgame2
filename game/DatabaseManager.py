from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, selectinload, make_transient
from game.tables import Base, GameInfo, PlayerInfo, Decisions, Nation, MarketInfo
from game.GameManager import GameManager
import pandas as pd
import sqlalchemy
import oracledb
import os

class DatabaseManager:
    def __init__(self):
        try:
            self.game_manager = GameManager()
            load_dotenv()
            DB_USER = "ADMIN"
            DB_PASSWORD = os.environ.get("DB_PASSWORD")
            HOST = "adb.eu-stockholm-1.oraclecloud.com"
            PORT = "1521"
            SERVICE_NAME = "ge72a74000425b4_ecgame_tp.adb.oraclecloud.com"
            DB_CONNECT_STRING = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.eu-stockholm-1.oraclecloud.com))(connect_data=(service_name=ge72a74000425b4_ecgame_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'
            connection_url = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{SERVICE_NAME}"
            self.conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_CONNECT_STRING)

            self.engine: sqlalchemy.Engine = create_engine("oracle+oracledb://", creator= lambda: self.conn, echo=False)
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
    
    def add_new_player(self, user_id: str, game_id: int, leader_name: str, nation_name: str):
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

    def advance_round(self, game_id: int, round_id: int|None = None):
        if round_id == None:
            round_id = self.fetch_current_round_id(game_id)
        list_of_nations: list[Nation] = self._get_list_of_nations(game_id=game_id, round_id=round_id)
        ## Computes changes inplace for list_of_nations, returns market_prices, net_suply and demand
        market_prices, net_supply, net_demand = self.game_manager.compute_round_of_states(list_of_nations)
        market_prices, net_supply, net_demand = self.__market_prices_supply_demand_to_db_form(market_prices, net_supply, net_demand)
        list_of_nations = [nation.create_nation_copy() for nation in list_of_nations]
        
        market_info = MarketInfo(game_id=game_id, round_id=round_id,**market_prices, **net_supply, **net_demand)
        
        with Session(self.engine) as session:
            session.add_all(list_of_nations)
            session.add(market_info)
            session.commit()

        self._increment_current_round(game_id=game_id)

    def save_decisions(self, game_id: int, user_id: str, round_id: int, dec_data: dict) -> bool:
        statement = (
            sqlalchemy.update(Decisions)
            .where(Decisions.game_id == game_id)
            .where(Decisions.user_id == user_id)
            .where(Decisions.round_id == round_id)
            .values(**dec_data)  # Unpack your dictionary directly here
        )
        with Session(self.engine) as session:
            result: sqlalchemy.Result = session.execute(statement)
            session.commit()
        
        if result.rowcount == 0:
            print("No matching decision found to update.")
            return False
        return True
        
    def fetch_nations_as_pd_dataframe(self, game_id: int|None = None, user_id: str|None = None, round_id: int|None = None, merge_PlayerInfo: bool = False) -> pd.DataFrame:
        if merge_PlayerInfo:
            statement = (sqlalchemy.select(Nation, PlayerInfo.nation_name, PlayerInfo.leader_name)
                         .join(PlayerInfo, (Nation.user_id == PlayerInfo.user_id) & (Nation.game_id == PlayerInfo.game_id)))
        else:
            statement = sqlalchemy.select(Nation)
        if game_id is not None:
            statement = statement.where(Nation.game_id == game_id)
        if user_id is not None:
            statement = statement.where(Nation.user_id == user_id)
        if round_id is not None:
            statement = statement.where(Nation.round_id == round_id)

        return pd.read_sql_query(statement, self.engine)

    def fetch_active_game_id(self, user_id: str) -> int|None:
        statement = sqlalchemy.select(PlayerInfo.game_id).where(PlayerInfo.user_id == user_id, PlayerInfo.is_active == True)
        with Session(self.engine) as session:
            game_id: int|None = session.execute(statement).scalar_one_or_none()
        return game_id

    def fetch_market_info_as_dataframe(self, game_id: int, round_id: int = None) -> pd.DataFrame:
        statement = sqlalchemy.select(MarketInfo).where(MarketInfo.game_id == game_id)
        if round_id != None:
            statement = statement.where(MarketInfo.round_id == round_id)
        return pd.read_sql_query(statement, self.engine)
        
        
    def fetch_current_round_id(self, game_id: int) -> int|None:
        statement = sqlalchemy.select(GameInfo.current_round).where(GameInfo.game_id == game_id)
        with Session(self.engine) as session:
            round_id: int|None = session.execute(statement).scalar()
        return round_id
    
    def _get_list_of_nations(self, game_id: int, round_id: int) -> list[Nation]:
        statement = (sqlalchemy.select(Nation)
                     .options(selectinload(Nation.decisions))
                     .options(selectinload(Nation.player_info))
                     .where(Nation.game_id == game_id, Nation.round_id == round_id)
        )
        with Session(self.engine) as session:
            list_of_nations: list[Nation] = session.execute(statement).scalars().all()
            return list_of_nations

    def _increment_current_round(self, game_id: int):
        statement = (
            sqlalchemy.update(GameInfo)
            .where(GameInfo.game_id == game_id)
            .values(current_round = GameInfo.current_round + 1)
        )
        with Session(self.engine) as session:
            session.execute(statement)
            session.commit()

    def __market_prices_supply_demand_to_db_form(self, market_prices: dict, supply: dict, demand: dict) -> tuple[dict,dict,dict]:
        market_prices = {"price_" + key: value for key, value in market_prices.items()}
        supply = {"supply_" + key: value for key, value in supply.items()}
        demand = {"demand_" + key: value for key, value in demand.items()}
        return market_prices, supply, demand

import inspect as py_inspect
from sqlalchemy import Column, Integer, String, Float, ForeignKey, inspect, ForeignKeyConstraint, UniqueConstraint, Identity
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy.orm import relationship, declarative_base, DeclarativeBase

from C import *

class Base(DeclarativeBase, MappedAsDataclass):
    pass

class GameInfo(Base):
    __tablename__ = "game_info"

    game_id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True, init=False)
    num_of_rounds: Mapped[int] = mapped_column(Integer, default=20)
    current_round: Mapped[int] = mapped_column(Integer, default=0)
    num_of_players: Mapped[int] = mapped_column(Integer, default=0)
    max_num_of_players: Mapped[int] = mapped_column(Integer, default=12)
    is_active: Mapped[int] = mapped_column(Integer, default=1)


class Decisions(Base):
    __tablename__ = "decisions"
    __table_args__ = (
        UniqueConstraint("game_id", "user_id", "round_id", name="decisions_uix_game_user_round"),
    )
    #nation = relationship("Nation", back_populates="decisions")

    decision_id: Mapped[int] = mapped_column(Identity(start=1), primary_key=True, init=False)

    nation_id: Mapped[int] = mapped_column(ForeignKey("nations.nation_id"), init=False)

    game_id: Mapped[int] =     mapped_column(Integer, default= 0)
    user_id: Mapped[int] =     mapped_column(Integer, default= 0)
    round_id: Mapped[int] =    mapped_column(Integer, default= 0)
    
    farm_area_fraction: Mapped[float] =              mapped_column(Float, default= 0.5)
    production_area_fraction: Mapped[float] =        mapped_column(Float, default= 0.5)

    LQ_goods_production_fraction: Mapped[float] =    mapped_column(Float, default= 0.5)
    HQ_goods_production_fraction: Mapped[float] =    mapped_column(Float, default= 0.5)

    LQ_food_production_fraction: Mapped[float] =     mapped_column(Float, default= 0.33)
    specials_production_fraction: Mapped[float] =    mapped_column(Float, default= 0.34)
    HQ_food_production_fraction: Mapped[float] =     mapped_column(Float, default= 0.33)
    
    fossil_fuels_burned: Mapped[float] =             mapped_column(Float, default= 0.0)

    electricity_allocated_food: Mapped[float] =      mapped_column(Float, default= 0.0)
    electricity_allocated_goods: Mapped[float] =     mapped_column(Float, default= 0.0)

    resources_distributed_LQfood: Mapped[float] =    mapped_column(Float, default= 0.0)
    resources_distributed_HQfood: Mapped[float] =    mapped_column(Float, default= 0.0)
    resources_distributed_specials: Mapped[float] =  mapped_column(Float, default= 0.0)
    resources_distributed_LQgoods: Mapped[float] =   mapped_column(Float, default= 0.0)
    resources_distributed_HQgoods: Mapped[float] =   mapped_column(Float, default= 0.0)

    investments_food :Mapped[float] =                  mapped_column(Float, default= 0.0)
    investments_goods :Mapped[float] =                 mapped_column(Float, default= 0.0)
    investments_fossil_fuels :Mapped[float] =          mapped_column(Float, default= 0.0)
    investments_renewable_electricity :Mapped[float] = mapped_column(Float, default= 0.0)
    investments_nuclear_electricity :Mapped[float] =   mapped_column(Float, default= 0.0)
    investments_energy_efficiency :Mapped[float] =     mapped_column(Float, default= 0.0)
    investments_environment :Mapped[float] =           mapped_column(Float, default= 0.0)
    investments_human_services :Mapped[float] =        mapped_column(Float, default= 0.0)
    
    imports_LQfood :Mapped[float] =                    mapped_column(Float, default= 0.0)
    imports_HQfood :Mapped[float] =                    mapped_column(Float, default= 0.0)
    imports_specials :Mapped[float] =                  mapped_column(Float, default= 0.0)
    imports_LQgoods :Mapped[float] =                   mapped_column(Float, default= 0.0)
    imports_HQgoods :Mapped[float] =                   mapped_column(Float, default= 0.0)
    imports_electricity :Mapped[float] =               mapped_column(Float, default= 0.0)
    imports_fossil_fuels :Mapped[float] =              mapped_column(Float, default= 0.0)

    exports_LQfood :Mapped[float] =                    mapped_column(Float, default= 0.0)
    exports_HQfood :Mapped[float] =                    mapped_column(Float, default= 0.0)
    exports_specials :Mapped[float] =                  mapped_column(Float, default= 0.0)
    exports_LQgoods :Mapped[float] =                   mapped_column(Float, default= 0.0)
    exports_HQgoods :Mapped[float] =                   mapped_column(Float, default= 0.0)
    exports_electricity :Mapped[float] =               mapped_column(Float, default= 0.0)
    exports_fossil_fuels :Mapped[float] =              mapped_column(Float, default= 0.0)

    def get_investments(self) -> dict:
        all_vars: dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {k.removeprefix("investments_"): v for k,v in all_vars.items() if k.startswith("investments")}
    def get_imports(self) -> dict:
        all_vars: dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {k.removeprefix("imports_"): v for k,v in all_vars.items() if k.startswith("imports")}
    def get_exports(self) -> dict:
        all_vars: dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {k.removeprefix("exports_"): v for k,v in all_vars.items() if k.startswith("exports")}
    def get_resources_distributed(self) -> dict:
        all_vars: dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {k.removeprefix("resources_distributed_"): v for k,v in all_vars.items() if k.startswith("resources_distributed")}


class PlayerInfo(Base):
    __tablename__ = "player_info"

    #nation = relationship("Nation", back_populates="player_info")

    game_id: Mapped[int] =     mapped_column(Integer, primary_key=True, default= 0)
    user_id: Mapped[int] =     mapped_column(Integer, primary_key=True, default= 0)
    leader_name: Mapped[str] = mapped_column(String(20), default="0")
    nation_name: Mapped[str] = mapped_column(String(20), default="0")
    #history: Mapped[list["Nation"]] = relationship("Nation", back_populates="player_info")


class Nation(Base):
    __tablename__ = "nations"
    __table_args__ = (
        UniqueConstraint("game_id", "user_id", "round_id", name="uix_game_user_round"),
        ForeignKeyConstraint(["game_id"], ["game_info.game_id"]),
        ForeignKeyConstraint(
            ["game_id", "user_id"], 
            ["player_info.game_id", "player_info.user_id"]
        ),
    )

    decisions: Mapped["Decisions"] = relationship("Decisions")
    player_info: Mapped["PlayerInfo"] = relationship("PlayerInfo")

    nation_id: Mapped[int] = mapped_column(Identity(start=1), primary_key=True, init=False)
    
    game_id: Mapped[int] = mapped_column(Integer, default= 0) 
    user_id: Mapped[int] = mapped_column(Integer, default=0)
    round_id: Mapped[int] = mapped_column(Integer, default= 0)

    total_utility: Mapped[float] =  mapped_column(Float, default= 0.0)
    population: Mapped[float] =     mapped_column(Float, default= 1000.0)
    death_rate: Mapped[float] =     mapped_column(Float, default= 10.0)
    birth_rate: Mapped[float] =     mapped_column(Float, default= 100.0)
    wealth: Mapped[float] =         mapped_column(Float, default= 0.0)

    environment_quality: Mapped[float] =             mapped_column(Float, default= 4.0)
    energy_efficiency_multiplier: Mapped[float] =    mapped_column(Float, default= 1.0)
    effect_of_trade_on_developement: Mapped[float] = mapped_column(Float, default= 1.0)
    human_services_capital: Mapped[float] =          mapped_column(Float, default= 2.0)

    resources_LQfood:        Mapped[float] = mapped_column(Float, default= 500.0)
    resources_HQfood:        Mapped[float] = mapped_column(Float, default= 500.0)
    resources_specials:      Mapped[float] = mapped_column(Float, default= 500.0)
    resources_LQgoods:       Mapped[float] = mapped_column(Float, default= 500.0)
    resources_HQgoods:       Mapped[float] = mapped_column(Float, default= 500.0)
    resources_electricity:   Mapped[float] = mapped_column(Float, default= 500.0)
    resources_fossil_fuels:  Mapped[float] = mapped_column(Float, default= 500.0)

    prod_cap_food:                  Mapped[float] = mapped_column(Float, default= 300.0)
    prod_cap_goods:                 Mapped[float] = mapped_column(Float, default= 300.0)
    prod_cap_fossil_fuels:          Mapped[float] = mapped_column(Float, default= 300.0)
    prod_cap_renewable_electricity: Mapped[float] = mapped_column(Float, default= 300.0)
    prod_cap_nuclear_electricity:   Mapped[float] = mapped_column(Float, default= 300.0)
    prod_cap_energy_efficiency:     Mapped[float] = mapped_column(Float, default= 300.0)
    prod_cap_environment:           Mapped[float] = mapped_column(Float, default= 300.0)
    prod_cap_human_services:        Mapped[float] = mapped_column(Float, default= 300.0)

    @property
    def elec_to_full_capacity_food(self) -> float:
        return self.prod_cap_food*BASE_RESOURCES_PER_PRODUCTION_CAPACITY_FOOD * ELECTRICITY_PER_FOOD * self.energy_efficiency_multiplier
    @property
    def elec_to_full_capacity_goods(self) -> float:
        return self.prod_cap_goods * ELECTRICITY_PER_GOODS * BASE_RESOURCES_PER_PRODUCTION_CAPACITY_GOODS * self.energy_efficiency_multiplier
    @property
    def elec_to_full_capacity_pop(self) -> float:
        return self.population * ELECTRICITY_PER_POP

    def get_resources(self) -> dict:
        all_vars: dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {k.removeprefix("resources_"): v for k,v in all_vars.items() if k.startswith("resources")}
    def set_resources(self, **kwargs):
        for resource, value in kwargs.items():
            attr_name = f"resources_{resource}"
            if hasattr(self, attr_name):
                setattr(self, attr_name, value)
            else: print(f"There's no resource {resource}")   
    def get_prod_caps(self) -> dict:
        all_vars: dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {k.removeprefix("prod_cap_"): v for k,v in all_vars.items() if k.startswith("prod_cap")}
    def set_prod_caps(self, **kwargs):
        for prod_cap, value in kwargs.items():
            attr_name = f"prod_cap_{prod_cap}"
            if hasattr(self, attr_name):
                setattr(self, attr_name, value)
            else: print(f"There's no prod_cap {prod_cap}") 
    def get_properties(self) -> dict:
        return {name: getattr(self, name) for name, value in py_inspect.getmembers(type(self), lambda v: isinstance(v, property))}
    def get_LQfoodPerPopPerYear(self):
        return (self.decisions.resources_distributed_LQfood / (self.population * 5))
    def get_HQfoodPerPopPerYear(self):
        return (self.decisions.resources_distributed_HQfood / (self.population * 5))
    def get_specialsPerPopPerYear(self): 
        return (self.decisions.resources_distributed_specials / (self.population * 5))
    def get_LQgoodsPerPopPerYear(self):
        return (self.decisions.resources_distributed_LQgoods /(self.population * 5))
    def get_HQgoodsPerPopPerYear(self):
        return (self.decisions.resources_distributed_HQgoods / (self.population * 5))


from Nation import Nation, Decisions
import math
import random
from C import *


class GameManager():
    def __init__(self):
        self.list_of_states: list[Nation] = []

    def __get_foodToBeProduced(self, state: Nation):
            base_rate = BASE_RESOURCES_PER_PRODUCTION_CAPACITY_FOOD
            prod_cap = state.prod_cap_food
            # Effect of environment on good production
            # environment_quality is between 0 and 10
            env = min(0.5 + state.environment_quality/10, 1.3)
            el_frac = state.decisions.electricity_allocated_food / state.elec_to_full_capacity_food
            area_frac = state.decisions.farm_area_fraction
            
            # Formula for food gained, including all of the different multipliers
            total_food_gained = prod_cap * base_rate * env * el_frac * area_frac 

            LQ_food_gained = total_food_gained * state.decisions.LQ_food_production_fraction
            HQ_food_gained = total_food_gained * state.decisions.HQ_food_production_fraction / 3
            SP_food_gained = total_food_gained * state.decisions.specials_production_fraction / 2
            return LQ_food_gained, HQ_food_gained, SP_food_gained
    def __get_goodsToBeProduced(self, state: Nation):
        base_rate = BASE_RESOURCES_PER_PRODUCTION_CAPACITY_GOODS
        prod_cap = state.prod_cap_goods
        # HSC_mult: Production is 3% smaller while HSC is less than 7, and then gives 1% productivity per HSC
        # works quadratically on HQ goods
        HSC_mult = 0.97 + (max(state.human_services_capital - 7, 0) / 100)
        el_frac = state.decisions.electricity_allocated_goods / state.elec_to_full_capacity_goods
        area_frac = state.decisions.production_area_fraction

        total_goods_gained = prod_cap * base_rate * HSC_mult * el_frac * area_frac

        LQ_goods_gained = total_goods_gained * state.decisions.LQ_goods_production_fraction
        HQ_goods_gained = total_goods_gained * state.decisions.HQ_goods_production_fraction * HSC_mult / 3
        return LQ_goods_gained, HQ_goods_gained
    def __get_electricityToBeProduced(self, state: Nation):
        base_rate = BASE_RESOURCES_PER_PRODUCTION_CAPACITY_ELECTRICITY
        prod_cap_rew = state.prod_cap_renewable_electricity
        prod_cap_nuc = state.prod_cap_nuclear_electricity
        
        fossil_fuel_electricity_gained = base_rate * state.decisions.fossil_fuels_burned
        # Renewable energy varies randomly by 25%
        renewable_electricity_gained = base_rate * prod_cap_rew * (0.75 + 0.5*random.random())
        # Nuclear electricity scales with education
        HSC_mult = 1 + 3 * (max(state.human_services_capital - 15, 0) / 100)
        nuclear_electricity_gained = base_rate * prod_cap_nuc * HSC_mult

        total_elecricity_gained = fossil_fuel_electricity_gained \
                                + renewable_electricity_gained \
                                + nuclear_electricity_gained \
                                - state.elec_to_full_capacity_pop
        
        total_elecricity_gained = max(total_elecricity_gained, 0)
        return total_elecricity_gained
    def __get_fossil_fuelsToBeProduced(self, state: Nation):
        return BASE_RESOURCES_PER_PRODUCTION_CAPACITY_ELECTRICITY * state.prod_cap_fossil_fuels

    def develop_market_prices(self, list_of_states: list[Nation], epsilon: float = 0.01) -> dict:
        if len(list_of_states) == 0:
            print("Empty list of states!")
            return
        # Returns prices Dict[str]: float of resource market prices
        #         net_supply Dict[str]: float 
        #         net_demand Dict[str]: float
        
        # imported = bought / demand
        # exported = sold / supply
        BASE_RESOURCE_K =  {
            "LQfood": 1.2,
            "HQfood": 1.3,
            "LQgoods": 1.4,
            "HQgoods": 1.5,
            "specials": 1.5,
            "electricity": 2,
            "fossil_fuels": 1.5,
        }
        RESOURCES: list[str] = BASE_RESOURCE_K.keys()
        net_supply = {key: 0 for key in RESOURCES}
        net_demand = {key: 0 for key in RESOURCES}

        prices = {key: 0 for key in RESOURCES}

        for state in list_of_states:
            exports: dict = state.decisions.get_exports()
            imports: dict = state.decisions.get_imports()
            print(exports)
            print(imports)
            for resource in RESOURCES:
                net_supply[resource] += exports[resource]
                net_demand[resource] += imports[resource]

        for resource in RESOURCES:
            s = net_supply[resource]
            d = net_demand[resource]
            k = BASE_RESOURCE_K[resource]

            price = math.exp(k*(d - s) / (d + s + epsilon))

            prices[resource] = price

        return prices, net_supply, net_demand

    def update_finances_of_states(self, list_of_states: list[Nation], prices, net_supply, net_demand):
        # Calculates money spend by each states and updates wealth
        # Calculates and updates ETD for each state
        # Updates resource inventory of each state with imports and exports
        if len(list_of_states) == 0:
            print("Empty list of states!")
            return
        n = len(list_of_states)
        total_supply_of_the_world = sum(net_supply.values())
        total_demand_of_the_world = sum(net_demand.values())
        total_market_value = total_supply_of_the_world + total_demand_of_the_world

        for state in list_of_states:
            RESOURCES: dict = state.get_resources()
            money_spend_by_state = 0
            money_earned_by_state = 0
            exports: dict = state.decisions.get_exports()
            imports: dict = state.decisions.get_imports()

            updated_resources: dict = {}
            for resource in RESOURCES:
                # Calculates money spend by each states
                money_spend_by_state += imports[resource] * prices[resource]
                money_earned_by_state += exports[resource] * prices[resource]

                # Updates resource inventory of each state with imports and exports
                updated_resources[resource] = RESOURCES[resource] + imports[resource] - exports[resource]
            
            state.set_resources(**updated_resources) 
            
                
            # Updates wealth
            state.wealth *= 1.1 # Debt or investment
            state.wealth += 0.95 * money_earned_by_state - money_spend_by_state

            market_share_of_state = (money_earned_by_state + money_spend_by_state) / (total_market_value + 0.00001)

            # Update ETD
            state.effect_of_trade_on_developement = min(max(market_share_of_state * n, 0.5), 1.5)
        
        # IMPORTS, EXPORTS, ETD AND WEALTH UPDATED

    def update_environment_of_states(self, list_of_states: list[Nation]):
        
        def update_environment_of_state(state: Nation):
            x = state.environment_quality # Previous environment quality
            a,k,b = 2.2, 0.42, 5
            # Previous environment affects investments done to current environment
            prev_env_coeff = a / (1+math.exp(-k*(x-b)))

            fossil_fuel_burn_damage = state.decisions.fossil_fuels_burned / 10

            fossil_fuel_mine_damage = state.prod_cap_fossil_fuels / 10

            electricity_damage = (state.prod_cap_nuclear_electricity + state.prod_cap_renewable_electricity ) / 10
            
            production_damage = state.prod_cap_goods * state.decisions.production_area_fraction

            specials_damage = state.prod_cap_food * state.decisions.farm_area_fraction * state.decisions.specials_production_fraction
            
            total_damage_to_env = fossil_fuel_burn_damage * 4 + 0.5*electricity_damage \
                                + production_damage * 2 + specials_damage + fossil_fuel_mine_damage
            
            total_env_protection = 10 * state.prod_cap_environment * prev_env_coeff

            # every 3333 points in damage / protection gets you +- 1 environmet score
            # i.e. + 10000 protection gets env += 3 and - 10000 gets env -= 3
            environment_delta = (total_env_protection - total_damage_to_env) * (3 / 10000)
            
            # Max change in environment in 5 years is 3
            environment_delta = max(environment_delta, -3 + 0.05*random.random())
            environment_delta = min(environment_delta, 3 + 0.05*random.random())

            state.environment_quality = x + environment_delta

            # Environment quality is between 0 and 10
            state.environment_quality = max(state.environment_quality, 0 )
            state.environment_quality = min(state.environment_quality, 10)


        for state in list_of_states:
            update_environment_of_state(state)

    def update_human_services_capital_of_states(self, list_of_states: list[Nation]):
        for state in list_of_states:
            previous_HSC = state.human_services_capital
            # main eq.
            if previous_HSC <= 30:
                delta_HSC = state.prod_cap_human_services / (1000 * math.sqrt(previous_HSC))
            else:
                delta_HSC = state.prod_cap_human_services/ (10000 * math.sqrt(previous_HSC))
            
            new_HSC = previous_HSC  + delta_HSC
            state.human_services_capital = new_HSC

    def update_population_BR_DR_of_states(self, list_of_states: list[Nation]):
        def update_population_of_state(state:Nation):
            state.population += (state.birth_rate - state.death_rate) / 1000
        def update_birth_rate_of_state(state:Nation):
            x,k,x0 = state.human_services_capital, 0.9, 5.5
            state.birth_rate = math.exp(-(k*x-x0))
        def update_death_rate_of_state(state: Nation):
            env = state.environment_quality
            environment_factor = 3 - env if env < 3 else 0
            foodPerPopPerYear = state.get_LQfoodPerPopPerYear() + state.get_HQfoodPerPopPerYear()
            food_factor = 10 - 10*foodPerPopPerYear if foodPerPopPerYear < 1 else 0
            state.death_rate = 9 + food_factor + environment_factor

        for state in list_of_states:
            update_population_of_state(state)
            update_birth_rate_of_state(state)
            update_death_rate_of_state(state)

    def update_inventory_of_states(self, list_of_states: list[Nation]):
        
        def update_food_inventory_of_state(state: Nation):
            LQ_food_gained, HQ_food_gained, SP_food_gained = self.__get_foodToBeProduced(state)
            RESOURCES: dict = state.get_resources()
            state.set_resources(LQfood = RESOURCES["LQfood"] + LQ_food_gained,
                                HQfood = RESOURCES["HQfood"] + HQ_food_gained,
                                specials = RESOURCES["specials"] + SP_food_gained)
                
        def update_goods_inventory_of_state(state: Nation):
            LQ_goods_gained, HQ_goods_gained = self.__get_goodsToBeProduced(state)
            RESOURCES: dict = state.get_resources()
            state.set_resources(LQgoods = RESOURCES["LQgoods"] + LQ_goods_gained,
                                HQgoods = RESOURCES["HQgoods"] + HQ_goods_gained)

        def update_electricity_inventory_of_state(state: Nation):
            total_elecricity_gained = self.__get_electricityToBeProduced(state)
            total_fossils_gained = self.__get_fossil_fuelsToBeProduced(state)
            RESOURCES: dict = state.get_resources()
            state.set_resources(electricity = total_elecricity_gained,
                                fossil_fuels = RESOURCES["fossil_fuels"] + total_fossils_gained)
            
        # Update for all states
        for state in list_of_states:
            update_food_inventory_of_state(state)
            update_goods_inventory_of_state(state)
            update_electricity_inventory_of_state(state)

    def apply_deprication_for_states(self, list_of_states: list[Nation]):
        resource_deprication_coeffs = {
                "food": 0.8,
                "goods": 0.8,
                "fossil_fuels": 0.8,
                "renewable_electricity": 0.8,
                "nuclear_electricity": 0.75,
                "energy_efficiency": 0.8,
                "environment": 0.4,
                "human_services": 0.1
            }
        
        def apply_deprication_for_state(state: Nation):
            updated_prod_caps: dict = {}
            for resource, dep_coeff in resource_deprication_coeffs.items():
                # Trade know-how reduces deprication
                ETD_coeff = state.effect_of_trade_on_developement
                ETD_coeff = (ETD_coeff - 1) / 3 + 1
                # Education reduces deprication
                HSC_coeff = 1 + state.human_services_capital / 1000
                PROD_CAPS: dict = state.get_prod_caps()
                updated_prod_caps[resource] = PROD_CAPS[resource] * dep_coeff * ETD_coeff * HSC_coeff
            state.set_prod_caps(**updated_prod_caps)

        for state in list_of_states:
            apply_deprication_for_state(state)

    def apply_investments_of_states(self, list_of_states: list[Nation]):
        def apply_investments_of_state(state: Nation):
            # How much does production capacity increase per invested LQgood
            increase_per_investment = {
                "food": 0.5,
                "goods": 0.5,
                "fossil_fuels": 5,
                "renewable_electricity": 5,
                "nuclear_electricity": 5,
                "energy_efficiency": 1,
                "environment": 1,
                "human_services": 1
            }
            updated_prod_caps: dict = {}
            for investment, value in state.decisions.get_investments().items():
                PROD_CAPS: dict = state.get_prod_caps()
                total_cap_increase = value * increase_per_investment[investment] * state.effect_of_trade_on_developement
                updated_prod_caps[investment] = PROD_CAPS[investment] + total_cap_increase
            state.set_prod_caps(**updated_prod_caps)

        for state in list_of_states:
            apply_investments_of_state(state)
        
    def update_energy_need_of_states(self, list_of_states: list[Nation]):
        # Energy effiency is different from the rest of the investments
        # It applies immediately in the following round
        def update_energy_efficiency_multiplier_of_state(state: Nation):
            # It is a ratio between weighted average of goods/food production capacity and 
            # electricity eff. production capacity
            eff_mult = ((state.prod_cap_goods * ELECTRICITY_PER_GOODS
                                                + state.prod_cap_food * ELECTRICITY_PER_FOOD) / 2 
                                                / (state.prod_cap_energy_efficiency + 0.0001) )
            eff_mult = max(eff_mult, 0.3)
            eff_mult = min(eff_mult, 1.3)
            
            state.energy_efficiency_multiplier = eff_mult
        
        for state in list_of_states:
            update_energy_efficiency_multiplier_of_state(state)

    def update_utility_of_states(self, list_of_states: list[Nation], market_prices):

        def compute_risk_of_state(state: Nation, market_prices):
            # total risk is composed of 
            # food aid (low food per pop) [0,30]
            # nuclear safety (too much nuclear power with little human services capital) [0, 50]
            # financial risk (debt) [0, inf)
            # Risk creates a multiplier [0,1] that reduces current utility gained
            def compute_food_aid_risk():
                foodPerPopPerYear = state.get_LQfoodPerPopPerYear() + state.get_HQfoodPerPopPerYear()
                return  max(30*(1 - foodPerPopPerYear), 0)

            food_aid_risk = compute_food_aid_risk()

            def compute_nuclear_risk():
                nuc_prod = state.prod_cap_nuclear_electricity
                HSC = state.human_services_capital
                k = 3.5
                return (3*nuc_prod) / (HSC ** k)
            
            nuclear_risk = compute_nuclear_risk()

            def compute_financial_risk(market_prices: dict):
                LQfood, HQfood, SP = self.__get_foodToBeProduced(state)
                LQgoods, HQgoods = self.__get_goodsToBeProduced(state)
                electricity = self.__get_electricityToBeProduced(state)
                fossil_fuel = self.__get_fossil_fuelsToBeProduced(state)
                p = market_prices.values()
                resource_amounts: dict = {"LQfood": LQfood,"HQfood": HQfood,"specials": SP, "LQgoods": LQgoods, "HQgoods": HQgoods, 
                                          "electricity": electricity,"fossil_fuels": fossil_fuel}
                
                prod_value = sum(resource_amounts[item] * market_prices[item] for item in market_prices)

                imports: dict = state.decisions.get_imports()
                exports: dict = state.decisions.get_exports()
                import_value = sum(imports[item]*market_prices[item] for item in market_prices)
                export_value = sum(exports[item]*market_prices[item] for item in market_prices)

                GDP =  import_value  + export_value + prod_value

                ratio = state.wealth / GDP
                if ratio >= -0.8:
                    risk = 0
                elif ratio < - 0.8:
                    risk = 10
                elif ratio < - 1:
                    risk = 20
                elif ratio < - 2:
                    risk = 30
                elif ratio < - 3:
                    risk = ratio * 10**(ratio - 2)
                return risk

            financial_risk = compute_financial_risk(market_prices)

            return food_aid_risk + nuclear_risk + financial_risk

        def compute_UTF_of_state(state: Nation):
            #Total utility from food distribution
            LQfoodPerPopPerYear = state.get_LQfoodPerPopPerYear()
            HQfoodPerPopPerYear = state.get_HQfoodPerPopPerYear()
            total_food = LQfoodPerPopPerYear + HQfoodPerPopPerYear

            def LQfoodUtility(LQfoodPerPopPerYear, total_food):
                x = total_food
                if x < 20:
                    utility_per_LQ_food = -(1/5) * x + 4
                else:
                    utility_per_LQ_food = 0
                return LQfoodPerPopPerYear * utility_per_LQ_food
            def HQfoodUtility(HQfoodPerPopPerYear, total_food):
                x = total_food
                if x <= 10:
                    utility_per_HQ_food = (1/5) * x
                elif x > 10:
                    utility_per_HQ_food = 2
                else:
                    utility_per_HQ_food = -(1/35) * x + 90/35
                return HQfoodPerPopPerYear * utility_per_HQ_food
            
            return LQfoodUtility(LQfoodPerPopPerYear, total_food) + HQfoodUtility(HQfoodPerPopPerYear, total_food)

        def compute_UTG_of_state(state: Nation):
            #Total utility from goods and specials

            LQgoodsPerPopPerYear = state.get_LQgoodsPerPopPerYear()
            HQgoodsPerPopPerYear = state.get_HQgoodsPerPopPerYear()
            specialsPerPopPerYear = state.get_specialsPerPopPerYear()

            total_material = LQgoodsPerPopPerYear + HQgoodsPerPopPerYear + specialsPerPopPerYear

            def LQgoodsUtility(LQgoodsPerPopPerYear, total_material):
                x = total_material
                if x <= 20:
                    utility_per_LQ_good = -(3/20) * x + 3
                else:
                    utility_per_LQ_good = 0
                return utility_per_LQ_good * LQgoodsPerPopPerYear  
            def HQgoodsUtility(HQgoodsPerPopPerYear, total_material):
                x = total_material
                if x <= 20:
                    utility_per_HQ_good = (1/5) * x
                else:
                    utility_per_HQ_good = -(1/45) * x + 40 / 9
                return utility_per_HQ_good * HQgoodsPerPopPerYear
            def specialsUtility(specialsPerPopPerYear, total_material):
                x = total_material
                if x <= 20:
                    utility_per_special = 1.5
                else:
                    utility_per_special = -(1/120) * x + 5/3
                return utility_per_special * specialsPerPopPerYear
            
            return (LQgoodsUtility(LQgoodsPerPopPerYear, total_material) 
                + HQgoodsUtility(HQgoodsPerPopPerYear, total_material)
                + specialsUtility(specialsPerPopPerYear, total_material))

        def compute_UTE_of_state(state: Nation):
            # Total utility from the environment
            return state.environment_quality

        def update_utility_of_state(state: Nation, market_prices):
            risk = compute_risk_of_state(state, market_prices)
            UTF = compute_UTF_of_state(state)
            UTG = compute_UTG_of_state(state)
            UTE = compute_UTE_of_state(state)

            state.total_utility += (0.1 + UTF + UTG + UTE) * (100 - risk) / 100
        
        prices,_,_ = self.develop_market_prices(list_of_states)

        for state in list_of_states:
            update_utility_of_state(state, prices)
            
    def reset_decisions_of_states(self, list_of_states: list[Nation]):

        def reset_decisions_of_state(state: Nation):
            fracs: dict = {
            "farm_area_fraction": state.decisions.farm_area_fraction,
            "production_area_fraction": state.decisions.production_area_fraction,
            "LQ_goods_production_fraction": state.decisions.LQ_goods_production_fraction,
            "HQ_goods_production_fraction": state.decisions.HQ_goods_production_fraction,
            "LQ_food_production_fraction": state.decisions.LQ_food_production_fraction,
            "specials_production_fraction": state.decisions.specials_production_fraction,
            "HQ_food_production_fraction": state.decisions.HQ_food_production_fraction
            }
            state.decisions = Decisions(game_id=state.game_id, user_id=state.user_id, round_id=state.round_id, **fracs)
        
        for state in list_of_states:
            reset_decisions_of_state(state)

    def compute_round_of_states(self, list_of_states: list[Nation]) -> list[Nation]:

        prices, net_supply, net_demand = self.develop_market_prices(list_of_states)

        self.update_finances_of_states(list_of_states, prices, net_supply, net_demand)

        self.update_environment_of_states(list_of_states)

        self.update_human_services_capital_of_states(list_of_states)

        self.update_population_BR_DR_of_states(list_of_states)

        self.update_inventory_of_states(list_of_states)

        self.apply_deprication_for_states(list_of_states)

        self.apply_investments_of_states(list_of_states)

        self.update_energy_need_of_states(list_of_states)

        self.update_utility_of_states(list_of_states, prices)

        self.reset_decisions_of_states(list_of_states)
        
        return list_of_states

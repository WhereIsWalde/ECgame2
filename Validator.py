from game.tables import Nation, Decisions
from sqlalchemy import inspect, Float
class Validator:
    def __init__(self):
        pass

    def validate_state(self, state: Nation) -> list[tuple[bool, str]]:
        ## Return values
        is_correct: bool = True
        final_error_text: str = ""

        validation_list: list[tuple[bool, str]] = [
            self.__decision_values_are_non_negative(state),
            self.__fractions_are_correct(state),
            self.__electricity_allocation_is_correct(state),
            self.__only_existing_resources_are_used(state)
        ]

        for validation_check_is_correct, error_text in validation_list:
            if not validation_check_is_correct:
                is_correct = False
                final_error_text += error_text

        return is_correct, final_error_text

    def __decision_values_are_non_negative(self, state: Nation) -> tuple[bool, str]:
        columns = inspect(type(state.decisions)).columns
        has_negative_values =  any(getattr(state.decisions, c.name) < 0 
                for c in columns 
                if isinstance(c.type, Float) and getattr(state.decisions, c.name) is not None
            )
        if has_negative_values:
            return False, "All decision values should be non-negative.\n"
        return True, ""

    def __fractions_are_correct(self, state: Nation) -> tuple[bool, str]:
        ## Return values
        is_correct: bool = True
        final_error_text: str = ""
        
        ## Check each fraction is between 0 and 1
        fracs: dict = {
            "farm_area_fraction": state.decisions.farm_area_fraction,
            "production_area_fraction": state.decisions.production_area_fraction,
            
            "LQ_food_production_fraction": state.decisions.LQ_food_production_fraction,
            "HQ_food_production_fraction": state.decisions.HQ_food_production_fraction,
            "specials_production_fraction": state.decisions.specials_production_fraction,
            
            "LQ_goods_production_fraction": state.decisions.LQ_goods_production_fraction,
            "HQ_goods_production_fraction": state.decisions.HQ_goods_production_fraction
        }

        for fraction_name, fraction_value in fracs.items():
            is_between, error_text = self.__check_number_is_between(fraction_value, 0.0, 1.0, fraction_name)
            if not is_between:
                is_correct = False
                final_error_text += error_text

        ## Check fractions sum to 1
        if not state.decisions.farm_area_fraction + state.decisions.production_area_fraction == 1:
            is_correct = False
            final_error_text += "farm_area_fraction and production_area_fraction should sum to 1.0\n"

        if not state.decisions.LQ_food_production_fraction + state.decisions.HQ_food_production_fraction + state.decisions.specials_production_fraction == 1:
            is_correct = False
            final_error_text += "LQ_food, HQ_food and specials production fractions should sum to 1.0\n"
        
        if not state.decisions.LQ_goods_production_fraction + state.decisions.HQ_goods_production_fraction == 1:
            is_correct = False
            final_error_text += "LQ_goods and HQ_goods production fractions should sum to 1.0\n"
        
        return is_correct, final_error_text
            
    def __electricity_allocation_is_correct(self, state: Nation) -> tuple[bool, str]:
        is_correct: bool = True
        final_error_text: str = ""
        if state.decisions.electricity_allocated_food > state.elec_to_full_capacity_food:
            is_correct = False
            final_error_text += "You should not allocate more electricity to food than is needed for full capacity."
        if state.decisions.electricity_allocated_goods > state.elec_to_full_capacity_goods:
            is_correct = False
            final_error_text += "You should not allocate more electricity to goods than is needed for full capacity."
        return is_correct, final_error_text
    
    def __only_existing_resources_are_used(self, state: Nation) -> tuple[bool, str]:
        is_correct: bool = True
        error_text: str = ""
        ## There should be enough LQFOOD
        if state.decisions.resources_distributed_LQfood + state.decisions.exports_LQfood > state.resources_LQfood:
            is_correct = False
            error_text += "You can't distribute and export more LQfood than you have.\n"
        ## There should be enough HQFOOD
        if state.decisions.resources_distributed_HQfood + state.decisions.exports_HQfood > state.resources_HQfood:
            is_correct = False
            error_text += "You can't distribute and export more HQfood than you have.\n"
        ## There should be enough specials
        if state.decisions.resources_distributed_specials + state.decisions.exports_specials > state.resources_specials:
            is_correct = False
            error_text += "You can't distribute and export more specials than you have.\n"
        ## There should be enough LQgoods
        total_LQgoods_used: float = sum(state.decisions.get_investments().values()) + state.decisions.exports_LQgoods + state.decisions.resources_distributed_LQgoods
        if total_LQgoods_used > state.resources_LQgoods:
            is_correct = False
            error_text += "You can't distribute, export and invest more LQgoods than you have.\n"
        ## There should be enough HQgoods
        if state.decisions.resources_distributed_HQgoods + state.decisions.exports_HQgoods > state.resources_HQgoods:
            is_correct = False
            error_text += "You can't distribute and export more HQgoods than you have.\n"
        ## There should be enough Electricity
        total_elec = state.decisions.electricity_allocated_food + state.decisions.electricity_allocated_goods + state.decisions.exports_electricity
        if total_elec > state.resources_electricity:
            is_correct = False
            error_text += "You can't allocate and export more electricity than you have.\n"
        ## There should be enough fossil fuels
        if state.decisions.fossil_fuels_burned + state.decisions.exports_fossil_fuels > state.resources_fossil_fuels:
            is_correct = False
            error_text += "You can't burn and export more fossil fuels than you have.\n"
        return is_correct, error_text

    def __check_number_is_between(self, number: float | int, a: float, b: float, var_name: str = "") -> tuple[bool, str]:
        if number >= a and number <= b:
            return True, ""
        return False, var_name + f" should be between {a} and {b}\n"




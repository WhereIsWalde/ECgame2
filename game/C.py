#### Game constants

class NationStart:
    """All starting values for a new Nation entity."""

    # Base Stats (Level 1)
    UTILITY = 0.0
    POPULATION = 1000.0
    DEATH_RATE = 10.0
    BIRTH_RATE = 100.0
    WEALTH = 0.0

    class Modifiers:
        """Environmental and efficiency modifiers."""
        ENVIRONMENT_QUALITY = 4.0
        ENERGY_EFFICIENCY = 1.0
        EFFECT_OF_TRADE_ON_DEVELOPEMENT = 1.0
        HUMAN_SERVICES_CAPITAL = 2.0

    class Resources:
        """Starting resource stockpiles."""
        LQ_FOOD = 400.0
        HQ_FOOD = 80.0
        SPECIALS = 200.0
        LQ_GOODS = 980.0
        HQ_GOODS = 150.0
        ELECTRICITY = 800.0
        FOSSIL_FUELS = 200.0

    class ProdCaps:
        """Starting production capacities."""
        FOOD = 88.0
        GOODS = 45.0
        FOSSIL_FUELS = 120.0
        RENEWABLE_ELEC = 30.0
        NUCLEAR_ELEC = 0.0
        ENERGY_EFFICIENCY = 0.0
        ENVIRONMENT = 0.0
        HUMAN_SERVICES = 0.0

class ElectricityUse:
    PER_UNIT_FOOD_PRODUCED: float = 0.25
    PER_UNIT_GOODS_PRODUCED: float = 0.75
    PER_POP: float = 0.2

class ResourceProduction:
    FOOD_PER_PROD_CAP = 12
    GOODS_PER_PROD_CAP = 10
    ELECTRICITY_PER_PROD_CAP = 15
    FOSSIL_FUELS_PER_PROD_CAP = 14

class Investment:
    FOOD_PROD_CAP_INCREASE_PER_GOOD = 0.5
    GOODS_PROD_CAP_INCREASE_PER_GOOD = 0.5
    FOSSIL_FUELS_PROD_CAP_INCREASE_PER_GOOD = 1.0
    RENEWABLE_ELEC_PROD_CAP_INCREASE_PER_GOOD = 1.0
    NUCLEAR_ELEC_PROD_CAP_INCREASE_PER_GOOD = 1.0
    ENERGY_EFFICIENCY_PROD_CAP_INCREASE_PER_GOOD = 1.0
    ENVIRONMENT_PROD_CAP_INCREASE_PER_GOOD = 1.0
    HUMAN_SERVICES_PROD_CAP_INCREASE_PER_GOOD = 1.0

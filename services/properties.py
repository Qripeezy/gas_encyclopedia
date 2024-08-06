from CoolProp.CoolProp import PropsSI


def calc_property(param_to_calc: str, param1: str, value1: float, param2: str, value2: float, gas: str) -> float:
    return PropsSI(param_to_calc, param1, value1, param2, value2, gas)

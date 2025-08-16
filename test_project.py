import pandas as pd
import numpy as np
from project import calc_bollinger_bands

def main():
    test_calc_bollinger_bands()


def test_calc_bollinger_bands():
    # Data provided
    std_list = [1.23, 1.45, 1.67, 1.89, 2.01, 2.22, 2.43, 2.64, 2.85, 3.06]
    dates = [
        "2025-08-04", "2025-08-05", "2025-08-06", "2025-08-07", "2025-08-08",
        "2025-08-11", "2025-08-12", "2025-08-13", "2025-08-14", "2025-08-15"
    ]
    ema_values = [
        207.5836, 207.3916, 207.6118, 208.0889, 208.9124,
        209.6287, 210.4139, 211.3126, 212.1544, 212.9166
    ]

    # Create DataFrame
    df = pd.DataFrame(ema_values, index=pd.to_datetime(dates), columns=["EMA"])
    # print(df)
    # print(std_list)
    
    # Perform actual correct calculations
    test_bb = []
    for i, ema_curr in enumerate(df["EMA"]):
        std_dev_curr = std_list[i]
        upper_limit = ema_curr + std_dev_curr
        lower_limit = ema_curr - std_dev_curr
        test_bb.append({"upper": upper_limit, "lower": lower_limit})
    
    # print(test_bb)

    # Test calculate bollinger band function
    actl_bb = calc_bollinger_bands(std_list, df)
    # print(actl_bb)
    assert actl_bb == test_bb


def test_function_2():
    ...


def test_function_n():
    ...


if __name__ == "__main__":
    main()
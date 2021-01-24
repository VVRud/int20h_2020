import argparse
import pandas as pd


def check_price(value) -> float:
    value = float(value)
    if value <= 0:
        raise argparse.ArgumentTypeError(
            f"Price value '{value}' is invalid. Must be positive."
        )
    return value


def check_fee(value) -> float:
    value = float(value)
    if value < 0 or value > 1:
        raise argparse.ArgumentTypeError(
            f"Fee value '{value}' is invalid. Must be in range [0, 1]."
        )
    return value


def parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="LTV calculator.", epilog="INT20H 'Xterm-inate' team."
    )

    parser.add_argument(
        "--path", type=str, required=False, default="./data_analytics.csv",
        help="path to csv file with columns 'Subscriber ID' and 'Event Date'"
    )
    parser.add_argument(
        "--price", type=check_price, required=False, default=9.99,
        help="app price, must be positive float number"
    )
    parser.add_argument(
        "--fee", type=check_fee, required=True, default=0.3,
        help="fee taken by the store (0.3 for AppStore, 0.2 for PlayStore)"
    )
    parser.add_argument(
        "--with_retention", required=False, default=False, action='store_true',
        help="calculate LTV with retention (default: calculation using ARPU)"
    )

    return parser


def perform_calculations(
        data: pd.DataFrame, price: float, fee: float,
        with_retention: bool = True
        ) -> float:
    """
    Calculate LTV.

    Parameters
    ----------
    data: pandas.DataFrame
        data storage with all the data we need for calculations
    price: float
        application subscription price
    fee: float
        market fee in percents ranged in [0, 1]
    with_retention: bool
        if we should use retention calculation method instead of
        average money spend (default: False)

    Returns
    -------
    float
        LTV value
    """
    data = (data
            .groupby(by="Subscriber ID").count()
            .reset_index()
            .groupby(by="Event Date").count()
            .sort_index()
            )["Subscriber ID"]
    weeks, user_counts = data.index.values - 1, data.values

    if with_retention:
        users = user_counts[::-1].cumsum()[::-1]
        ltv = (users[1:] / users[0:-1]).cumprod().sum() * price * (1 - fee)
    else:
        ltv = (
            weeks * user_counts * price * (1 - fee)
        ).sum() / user_counts.sum()

    return ltv


if __name__ == "__main__":
    parser = parser().parse_args()

    data = pd.read_csv(parser.path)[["Event Date", "Subscriber ID"]]
    data["Event Date"] = pd.to_datetime(data["Event Date"])

    ltv = perform_calculations(
        data, parser.price, parser.fee, parser.with_retention
    )

    print(f"Calculated LTV: {ltv}")

from dataclasses import dataclass
from typing import List, Tuple

from bs4 import BeautifulSoup

TRADING_EMAIL_SUBJECT = "Contract Note Statement from Trading 212"


@dataclass(init=False)
class TradingRow:
    """
    "№",
    "Order ID",
    "Instrument/ISIN",  # this 2
    "Direction",
    "Quantity",  # this 4
    "Price",  # this 5
    "Total amount",
    "Trading day",  # this 7
    "Trading  time",
    "Commission",
    "Charges and fees",
    "Order Type",
    "Execution venue",
    "Exchange rate",
    "Total cost",
    """

    nr: int
    order_id: str
    instrument_isid: str
    direction: str
    quantity: float
    price: float
    total_amount: float
    trading_day: str
    trading_time: str
    commision: float
    charges_and_fees: float
    order_type: str
    execution_venue: str
    exchange_rate: float
    total_cost: float

    def __init__(
        self,
        nr: str,
        order_id: str,
        instrument_isin: str,
        direction: str,
        quantity: str,
        price: str,
        total_amount: str,
        trading_day: str,
        trading_time: str,
        commision: str,
        charges_and_fees: str,
        order_type: str,
        execution_venue: str,
        exchange_rate: str,
        total_cost: str,
    ) -> None:
        self.nr = int(nr)  # 4
        self.order_id = order_id  # POS427262481
        self.symbol, self.isin = instrument_isin.split("/")  # PFE/US7170811035
        self.direction = direction  # Buy
        self.quantity = float(quantity)  # 0.015931
        self.price = float(price.split(" ")[0])  # 31.3837 EUR
        self.total_amount = float(total_amount.split(" ")[0])  # 0.5 EUR
        self.trading_day = trading_day  # 15-09-2020
        self.trading_time = trading_time  # 13:32:24
        self.commision = float(commision.split(" ")[0])  # 0 EUR
        self.charges_and_fees = float(charges_and_fees.split(" ")[0])  # 0 EUR
        self.order_type = order_type  # MARKET
        self.execution_venue = execution_venue  # Over the Counter (OTC)
        self.exchange_rate = float(exchange_rate.split(" ")[0])  # 0.84221
        self.total_cost = float(total_cost.split(" ")[0])  # 0.5 EUR

    ROWS = [
        "№",
        "Order ID",
        "Instrument/ISIN",
        "Direction",
        "Quantity",
        "Price",
        "Total amount",
        "Trading day",
        "Trading  time",
        "Commission",
        "Charges and fees",
        "Order Type",
        "Execution venue",
        "Exchange rate",
        "Total cost",
    ]

    def __eq__(self, other) -> bool:
        return self.order_id == other.order_id

    def __repr__(self) -> str:
        return f"{self.symbol}:{self.direction}:{self.quantity}:{self.trading_day}"


class TradingParser:
    def __init__(self, raw_html: str) -> None:
        self.raw_html = raw_html
        self.soup = BeautifulSoup(raw_html, features="lxml")

    @property
    def tables(self):
        return self.soup.find_all("table")

    @property
    def positions_table(self):
        return self.tables[3]

    def table_rows(self, table):
        return table.findAll("tr")

    def row_colums(self, row):
        return row.findAll("td")

    def get_positions(self) -> List[TradingRow]:
        positions = []
        for row in self.table_rows(self.positions_table):
            _column_data = []

            for column in self.row_colums(row):
                if not column.text:
                    continue

                _column_data.append(column.text.strip())

            if not len(_column_data) == 15:
                continue

            positions.append(TradingRow(*_column_data))

        return positions


class TradingExporter:
    YFINANCE_ROWS = [
        "Symbol",
        "Trade Date",
        "Purchase Price",
        "Quantity",
    ]

    @staticmethod
    def to_yfinance_row(row: TradingRow) -> Tuple[str, str, float, float]:
        day, month, year = row.trading_day.split("-")
        return (
            row.symbol,
            f"{year}{month}{day}",
            row.price / row.exchange_rate,
            row.quantity,
        )

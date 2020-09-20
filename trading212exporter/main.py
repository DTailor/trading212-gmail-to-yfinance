from simplegmail import Gmail
from simplegmail.query import construct_query
from trading212exporter.trading212 import (
    TRADING_EMAIL_SUBJECT,
    TradingParser,
    TradingExporter,
)

import csv


def fetch_messages(gmail, query):
    return gmail.get_messages(query=construct_query(query))


if __name__ == "__main__":
    gmail = Gmail()

    trading_messages = fetch_messages(
        gmail,
        {"subject": TRADING_EMAIL_SUBJECT, "after": "2020/09/14"},
    )
    all_positions = []
    for message in trading_messages:
        trading = TradingParser(message.html)

        all_positions.extend(trading.get_positions())

    with open("yfinance.csv", "w+") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(TradingExporter.YFINANCE_ROWS)
        for position in all_positions:
            writer.writerow(TradingExporter.to_yfinance_row(position))

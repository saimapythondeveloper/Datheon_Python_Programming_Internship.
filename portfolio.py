
import csv
import os
from datetime import datetime

import yfinance as yf

SUMMARY_FILE = "portfolio_summary.csv"


def get_stock_price(ticker):
    """Fetch the latest available stock price."""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="5d")

        if history.empty:
            return None

        return float(history["Close"].dropna().iloc[-1])

    except Exception:
        return None


def get_positive_number(prompt):
    """Accept only positive numeric values."""
    while True:
        try:
            value = float(input(prompt))

            if value > 0:
                return value

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")


def save_to_csv(rows, totals):
    """Append portfolio results to a CSV log."""
    file_exists = (
        os.path.exists(SUMMARY_FILE)
        and os.path.getsize(SUMMARY_FILE) > 0
    )

    with open(SUMMARY_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Ticker",
                "Buy Price",
                "Quantity",
                "Current Price",
                "Invested Capital",
                "Market Value",
                "Profit/Loss",
                "Return (%)"
            ])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for row in rows:
            writer.writerow([timestamp] + row)

        writer.writerow([
            timestamp,
            "TOTAL",
            "",
            "",
            "",
            f"{totals['invested']:.2f}",
            f"{totals['market_value']:.2f}",
            f"{totals['profit_loss']:.2f}",
            f"{totals['return_pct']:.2f}"
        ])


def main():
    portfolio = {}

    print("\n" + "=" * 55)
    print("       STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 55)

    while True:
        ticker = input(
            "\nEnter stock ticker (e.g., AAPL, MSFT): "
        ).strip().upper()

        if not ticker or not ticker.replace(".", "").isalnum():
            print("Invalid ticker format.")
            continue

        if ticker in portfolio:
            print("This ticker is already in your portfolio.")
            continue

        buy_price = get_positive_number("Enter purchase price ($): ")
        quantity = get_positive_number("Enter number of shares: ")

        print(f"Fetching latest available price for {ticker}...")
        current_price = get_stock_price(ticker)

        if current_price is None:
            print("Could not retrieve a price for this ticker.")
            print("Check the ticker and your internet connection.")
            retry = input("Try another ticker? (y/n): ").strip().lower()

            if retry != "y":
                break

            continue

        portfolio[ticker] = {
            "buy_price": buy_price,
            "quantity": quantity,
            "current_price": current_price
        }

        print(f"{ticker} added at ${current_price:.2f} per share.")

        more = input("Add another stock? (y/n): ").strip().lower()

        if more != "y":
            break

    if not portfolio:
        print("\nNo stocks were added. Exiting.")
        return

    rows = []
    total_invested = 0.0
    total_market_value = 0.0

    print("\n" + "=" * 100)
    print("PORTFOLIO PERFORMANCE REPORT")
    print("=" * 100)

    print(
        f"{'Ticker':<10}{'Buy Price':>12}{'Quantity':>12}"
        f"{'Current':>12}{'Invested':>14}{'Market Value':>15}"
        f"{'P/L':>12}{'Return %':>12}"
    )
    print("-" * 100)

    for ticker, data in portfolio.items():
        buy = data["buy_price"]
        quantity = data["quantity"]
        current = data["current_price"]

        invested = buy * quantity
        market_value = current * quantity
        profit_loss = market_value - invested
        return_pct = (profit_loss / invested) * 100

        total_invested += invested
        total_market_value += market_value

        rows.append([
            ticker,
            f"{buy:.2f}",
            f"{quantity:g}",
            f"{current:.2f}",
            f"{invested:.2f}",
            f"{market_value:.2f}",
            f"{profit_loss:.2f}",
            f"{return_pct:.2f}"
        ])

        print(
            f"{ticker:<10}{buy:>12.2f}{quantity:>12g}"
            f"{current:>12.2f}{invested:>14.2f}"
            f"{market_value:>15.2f}{profit_loss:>12.2f}"
            f"{return_pct:>11.2f}%"
        )

    total_profit_loss = total_market_value - total_invested
    total_return = (
        (total_profit_loss / total_invested) * 100
        if total_invested else 0
    )

    print("-" * 100)
    print(f"Total invested:     ${total_invested:,.2f}")
    print(f"Current market value: ${total_market_value:,.2f}")
    print(f"Total profit/loss:  ${total_profit_loss:,.2f}")
    print(f"Overall return:     {total_return:.2f}%")

    totals = {
        "invested": total_invested,
        "market_value": total_market_value,
        "profit_loss": total_profit_loss,
        "return_pct": total_return
    }

    save_to_csv(rows, totals)

    print(f"\nPortfolio log saved to {SUMMARY_FILE}")
    print("Thank you for using the tracker!")


if __name__ == "__main__":
    main()

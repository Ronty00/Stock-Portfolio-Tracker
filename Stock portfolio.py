# import yfinance as yf
# from tabulate import tabulate

# # Portfolio storage
# portfolio = []

# # Fetch real-time stock data using Yahoo Finance
# def get_stock_data(ticker):
#     try:
#         stock = yf.Ticker(ticker)
#         stock_info = stock.history(period="1d")  # Get today's stock data
#         if not stock_info.empty:
#             latest_close = stock_info["Close"].iloc[-1]  # Latest closing price
#             return {"ticker": ticker.upper(), "price": latest_close}
#         else:
#             print(f"No data found for ticker: {ticker}")
#             return None
#     except Exception as e:
#         print(f"Error fetching data for {ticker}: {e}")
#         return None

# # Display portfolio
# def display_portfolio():
#     if not portfolio:
#         print("\nYour portfolio is empty.\n")
#         return

#     table = []
#     total_investment = 0
#     total_current_value = 0

#     for stock in portfolio:
#         stock_data = get_stock_data(stock["ticker"])
#         if stock_data:
#             current_value = stock["shares"] * stock_data["price"]
#             table.append(
#                 [
#                     stock["ticker"],
#                     stock["shares"],
#                     f"₹{stock['purchase_price']:.2f}",
#                     f"₹{stock_data['price']:.2f}",
#                     f"₹{current_value:.2f}",
#                 ]
#             )
#             total_investment += stock["shares"] * stock["purchase_price"]
#             total_current_value += current_value
#         else:
#             print(f"Error: Could not retrieve data for {stock['ticker']}.")

#     print("\nYour Portfolio:")
#     print(tabulate(table, headers=["Ticker", "Shares", "Buy Price", "Current Price", "Current Value"], tablefmt="fancy_grid"))

#     # Display portfolio summary
#     print("\nPortfolio Summary:")
#     print(f"Total Investment: ₹{total_investment:.2f}")
#     print(f"Total Current Value: ₹{total_current_value:.2f}")
#     profit_loss = total_current_value - total_investment
#     print(f"Profit/Loss: ₹{profit_loss:.2f}")

# # Add stock to portfolio
# def add_stock():
#     ticker = input("Enter the stock ticker symbol (e.g., RELIANCE.NS, TCS.NS): ").upper()
#     stock_data = get_stock_data(ticker)
#     if not stock_data:
#         print("Error: Invalid ticker symbol or unable to fetch stock data.")
#         return

#     try:
#         shares = int(input(f"Enter the number of shares for {ticker}: "))
#         purchase_price = float(input(f"Enter the purchase price for {ticker} (in ₹): "))
#         portfolio.append({
#             "ticker": ticker,
#             "shares": shares,
#             "purchase_price": purchase_price
#         })
#         print(f"{shares} shares of {ticker} added to your portfolio.")
#     except ValueError:
#         print("Invalid input. Please enter numeric values for shares and price.")

# # Remove stock from portfolio
# def remove_stock():
#     ticker = input("Enter the stock ticker symbol to remove: ").upper()
#     for stock in portfolio:
#         if stock["ticker"] == ticker:
#             portfolio.remove(stock)
#             print(f"{ticker} has been removed from your portfolio.")
#             return
#     print(f"{ticker} is not in your portfolio.")

# # Main menu
# def main():
#     while True:
#         print("\n=== Stock Portfolio Tracker ===")
#         print("1. View Portfolio")
#         print("2. Add Stock")
#         print("3. Remove Stock")
#         print("4. Exit")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             display_portfolio()
#         elif choice == "2":
#             add_stock()
#         elif choice == "3":
#             remove_stock()
#         elif choice == "4":
#             print("Thank you for using the Stock Portfolio Tracker. Goodbye!")
#             break
#         else:
#             print("Invalid choice. Please try again.")

# # Run the application
# if __name__ == "__main__":
#     main()





# import tkinter as tk
# from tkinter import ttk, messagebox
# import sqlite3
# import yfinance as yf
# from decimal import Decimal

# # Database setup
# def setup_database():
#     conn = sqlite3.connect("portfolio.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS stocks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             ticker TEXT NOT NULL,
#             shares INTEGER NOT NULL,
#             purchase_price REAL NOT NULL
#         )
#     """)
#     conn.commit()
#     conn.close()

# # Fetch real-time stock data using Yahoo Finance
# def get_stock_data(ticker):
#     try:
#         stock = yf.Ticker(ticker)
#         stock_info = stock.history(period="1d")
#         if not stock_info.empty:
#             latest_close = stock_info["Close"].iloc[-1]
#             return {"ticker": ticker.upper(), "price": latest_close}
#         else:
#             return None
#     except Exception as e:
#         return None

# # Add stock to the database and portfolio
# def add_stock():
#     ticker = ticker_entry.get().upper()
#     shares = shares_entry.get()
#     price = price_entry.get()

#     if not ticker or not shares or not price:
#         messagebox.showerror("Input Error", "All fields are required!")
#         return

#     try:
#         shares = int(shares)
#         price = float(price)
#     except ValueError:
#         messagebox.showerror("Input Error", "Shares must be an integer and price must be a number!")
#         return

#     stock_data = get_stock_data(ticker)
#     if not stock_data:
#         messagebox.showerror("Error", f"Could not fetch data for ticker: {ticker}")
#         return

#     conn = sqlite3.connect("portfolio.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO stocks (ticker, shares, purchase_price) VALUES (?, ?, ?)", (ticker, shares, price))
#     conn.commit()
#     conn.close()

#     messagebox.showinfo("Success", f"{shares} shares of {ticker} added to your portfolio!")
#     update_portfolio_table()

# # Remove stock from the database and portfolio
# def remove_stock():
#     selected_item = portfolio_tree.selection()
#     if not selected_item:
#         messagebox.showerror("Error", "No stock selected to remove.")
#         return

#     ticker = portfolio_tree.item(selected_item)["values"][0]

#     conn = sqlite3.connect("portfolio.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM stocks WHERE ticker = ?", (ticker,))
#     conn.commit()
#     conn.close()

#     messagebox.showinfo("Success", f"{ticker} removed from your portfolio!")
#     update_portfolio_table()

# # Load portfolio from database
# def load_portfolio():
#     conn = sqlite3.connect("portfolio.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT ticker, shares, purchase_price FROM stocks")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# # Update the portfolio table
# def update_portfolio_table():
#     for item in portfolio_tree.get_children():
#         portfolio_tree.delete(item)

#     portfolio = load_portfolio()
#     total_investment = Decimal(0.00)
#     total_current_value = Decimal(0.00)

#     for stock in portfolio:
#         ticker, shares, purchase_price = stock
#         stock_data = get_stock_data(ticker)
#         if stock_data:
#             current_price = stock_data["price"]
#             current_value = shares * current_price
#             total_investment += shares * purchase_price
#             total_current_value += current_value
#             portfolio_tree.insert(
#                 "",
#                 "end",
#                 values=(
#                     ticker,
#                     shares,
#                     f"₹{purchase_price:.2f}",
#                     f"₹{current_price:.2f}",
#                     f"₹{current_value:.2f}",
#                 ),
#             )

#     total_investment_label.config(text=f"Total Investment: ₹{total_investment:.2f}")
#     total_value_label.config(text=f"Total Current Value: ₹{total_current_value:.2f}")
#     profit_loss = total_current_value - total_investment
#     profit_loss_label.config(
#         text=f"Profit/Loss: ₹{profit_loss:.2f}", fg="green" if profit_loss >= 0 else "red"
#     )

# # Refresh stock prices every 5 seconds
# def refresh_prices():
#     update_portfolio_table()
#     root.after(5000, refresh_prices)  # Schedule the next refresh in 5000 ms (5 seconds)

# # Create the main GUI window
# root = tk.Tk()
# root.title("Stock Portfolio Tracker")
# root.geometry("800x600")
# root.configure(bg="#f0f8ff")

# # Title
# title_label = tk.Label(root, text="Stock Portfolio Tracker", font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#333")
# title_label.pack(pady=10)

# # Input Frame
# input_frame = tk.Frame(root, bg="#f0f8ff")
# input_frame.pack(pady=10)

# ticker_label = tk.Label(input_frame, text="Ticker Symbol:", font=("Helvetica", 12), bg="#f0f8ff")
# ticker_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
# ticker_entry = tk.Entry(input_frame, font=("Helvetica", 12))
# ticker_entry.grid(row=0, column=1, padx=5, pady=5)

# shares_label = tk.Label(input_frame, text="Shares:", font=("Helvetica", 12), bg="#f0f8ff")
# shares_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
# shares_entry = tk.Entry(input_frame, font=("Helvetica", 12))
# shares_entry.grid(row=1, column=1, padx=5, pady=5)

# price_label = tk.Label(input_frame, text="Purchase Price (₹):", font=("Helvetica", 12), bg="#f0f8ff")
# price_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
# price_entry = tk.Entry(input_frame, font=("Helvetica", 12))
# price_entry.grid(row=2, column=1, padx=5, pady=5)

# add_button = tk.Button(input_frame, text="Add Stock", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=add_stock)
# add_button.grid(row=3, column=0, columnspan=2, pady=10)

# remove_button = tk.Button(input_frame, text="Remove Selected Stock", font=("Helvetica", 12), bg="#f44336", fg="white", command=remove_stock)
# remove_button.grid(row=4, column=0, columnspan=2, pady=5)

# # Portfolio Table
# columns = ("Ticker", "Shares", "Buy Price", "Current Price", "Current Value")
# portfolio_tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
# for col in columns:
#     portfolio_tree.heading(col, text=col)
#     portfolio_tree.column(col, anchor="center")
# portfolio_tree.pack(pady=10)

# # Portfolio Summary
# summary_frame = tk.Frame(root, bg="#f0f8ff")
# summary_frame.pack(pady=10)

# total_investment_label = tk.Label(summary_frame, text="Total Investment: ₹0.00", font=("Helvetica", 14), bg="#f0f8ff")
# total_investment_label.grid(row=0, column=0, padx=10)

# total_value_label = tk.Label(summary_frame, text="Total Current Value: ₹0.00", font=("Helvetica", 14), bg="#f0f8ff")
# total_value_label.grid(row=0, column=1, padx=10)

# profit_loss_label = tk.Label(summary_frame, text="Profit/Loss: ₹0.00", font=("Helvetica", 14), bg="#f0f8ff", fg="green")
# profit_loss_label.grid(row=0, column=2, padx=10)

# # Initialize database and load portfolio
# setup_database()
# update_portfolio_table()

# # Start real-time price updates
# refresh_prices()

# # Run the application
# root.mainloop()







import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from decimal import Decimal
import yfinance as yf

# Database setup
def setup_database():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            shares INTEGER NOT NULL,
            purchase_price TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Fetch real-time stock data using Yahoo Finance
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.history(period="1d")
        if not stock_info.empty:
            latest_close = stock_info["Close"].iloc[-1]
            return {"ticker": ticker.upper(), "price": Decimal(latest_close)}
        else:
            return None
    except Exception as e:
        return None

# Add stock to the database and portfolio
def add_stock():
    ticker = ticker_entry.get().upper()
    shares = shares_entry.get()
    price = price_entry.get()

    if not ticker or not shares or not price:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        shares = int(shares)
        price = Decimal(price)
    except ValueError:
        messagebox.showerror("Input Error", "Shares must be an integer and price must be a valid number!")
        return

    stock_data = get_stock_data(ticker)
    if not stock_data:
        messagebox.showerror("Error", f"Could not fetch data for ticker: {ticker}")
        return

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stocks (ticker, shares, purchase_price) VALUES (?, ?, ?)", (ticker, shares, str(price)))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"{shares} shares of {ticker} added to your portfolio!")
    update_portfolio_table()

# Remove stock from the database and portfolio
def remove_stock():
    selected_item = portfolio_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No stock selected to remove.")
        return

    ticker = portfolio_tree.item(selected_item)["values"][0]

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stocks WHERE ticker = ?", (ticker,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"{ticker} removed from your portfolio!")
    update_portfolio_table()

# Load portfolio from database
def load_portfolio():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ticker, shares, purchase_price FROM stocks")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Update the portfolio table
def update_portfolio_table():
    for item in portfolio_tree.get_children():
        portfolio_tree.delete(item)

    portfolio = load_portfolio()
    total_investment = Decimal("0.00")
    total_current_value = Decimal("0.00")

    for stock in portfolio:
        ticker, shares, purchase_price = stock
        shares = int(shares)
        purchase_price = Decimal(purchase_price)

        stock_data = get_stock_data(ticker)
        if stock_data:
            current_price = stock_data["price"]
            current_value = shares * current_price
            total_investment += shares * purchase_price
            total_current_value += current_value
            portfolio_tree.insert(
                "",
                "end",
                values=(
                    ticker,
                    shares,
                    f"₹{purchase_price:.2f}",
                    f"₹{current_price:.2f}",
                    f"₹{current_value:.2f}",
                ),
            )

    total_investment_label.config(text=f"Total Investment: ₹{total_investment:.2f}")
    total_value_label.config(text=f"Total Current Value: ₹{total_current_value:.2f}")
    profit_loss = total_current_value - total_investment
    profit_loss_label.config(
        text=f"Profit/Loss: ₹{profit_loss:.2f}", fg="green" if profit_loss >= 0 else "red"
    )

# Refresh stock prices every 5 seconds
def refresh_prices():
    update_portfolio_table()
    root.after(5000, refresh_prices)  # Schedule the next refresh in 5000 ms (5 seconds)

# Create the main GUI window
root = tk.Tk()
root.title("Stock Portfolio Tracker")
root.geometry("800x600")
root.configure(bg="#f0f8ff")

# Title
title_label = tk.Label(root, text="Stock Portfolio Tracker", font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#333")
title_label.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root, bg="#f0f8ff")
input_frame.pack(pady=10)

ticker_label = tk.Label(input_frame, text="Stock Symbol:", font=("Helvetica", 12), bg="#f0f8ff")
ticker_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
ticker_entry = tk.Entry(input_frame, font=("Helvetica", 12))
ticker_entry.grid(row=0, column=1, padx=5, pady=5)

shares_label = tk.Label(input_frame, text="Number of Shares:", font=("Helvetica", 12), bg="#f0f8ff")
shares_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
shares_entry = tk.Entry(input_frame, font=("Helvetica", 12))
shares_entry.grid(row=1, column=1, padx=5, pady=5)

price_label = tk.Label(input_frame, text="Purchase Price (₹):", font=("Helvetica", 12), bg="#f0f8ff")
price_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
price_entry = tk.Entry(input_frame, font=("Helvetica", 12))
price_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(input_frame, text="Add Stock", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=add_stock)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

remove_button = tk.Button(input_frame, text="Remove Selected Stock", font=("Helvetica", 12), bg="#f44336", fg="white", command=remove_stock)
remove_button.grid(row=4, column=0, columnspan=2, pady=5)

# Portfolio Table
columns = ("Stock", "Shares Quantity", "Buy Price", "Current Price", "Current Value")
portfolio_tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    portfolio_tree.heading(col, text=col)
    portfolio_tree.column(col, anchor="center")
portfolio_tree.pack(pady=10)

# Portfolio Summary
summary_frame = tk.Frame(root, bg="#f0f8ff")
summary_frame.pack(pady=10)

total_investment_label = tk.Label(summary_frame, text="Total Investment: ₹0.00", font=("Helvetica", 14), bg="#f0f8ff")
total_investment_label.grid(row=0, column=0, padx=10)

total_value_label = tk.Label(summary_frame, text="Total Current Value: ₹0.00", font=("Helvetica", 14), bg="#f0f8ff")
total_value_label.grid(row=0, column=1, padx=10)

profit_loss_label = tk.Label(summary_frame, text="Profit/Loss: ₹0.00", font=("Helvetica", 14), bg="#f0f8ff", fg="green")
profit_loss_label.grid(row=0, column=2, padx=10)

# Initialize database and load portfolio
setup_database()
update_portfolio_table()

# Start real-time price updates
refresh_prices()

# Run the application
root.mainloop()

import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simulate(df_price, signals, amount, risk_free_rate):
    simulation_data = []
    evaluation_data = []
    simulation = []

    with open("simulation.csv") as file:
        balance = float(amount)
        num_shares = 0
        idx = 0
        in_position = False
        trades = []
        trades_idx = 0

        for row in df_price.itertuples():
            # Get date and price for current day
            date = row.Index
            closing_price = row.Close

            # Record current day data
            today = {"Date": date, "Starting Balance": balance, "Price (Close)": closing_price}

            # Extract trade signal and positions for current day
            signal_current = signals[idx]
            action = signal_current[date]

            # Execute trades (buy/sell/hold)
            if action == "Enter Long" and not in_position:
                # Buy n shares
                start_bal = balance
                num_shares = int(balance / closing_price)
                today["Shares"] = num_shares
                spent = closing_price * num_shares
                trades.append(-1 * spent)
                today["Position"] = "Long"
                today["Holdings Value"] = spent
                cash = balance - spent
                today["Cash"] = cash

                # Update new daily balance & holdings after buying long
                balance = balance - spent + cash
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = balance - start_bal
                in_position = True
            elif action == "Enter Short" and not in_position:
                # Sell n shares
                start_bal = balance
                num_shares = int(balance / closing_price)
                today["Shares"] = num_shares
                earned = closing_price * num_shares
                trades.append(earned)
                today["Position"] = "Short"
                today["Holdings Value"] = earned
                cash = balance + earned
                today["Cash"] = cash

                # Update new daily balance & holdings after short selling
                balance = balance + earned + cash
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = balance - start_bal
                in_position = True
            elif action == "Exit Long" and in_position:
                # Sell n shares
                start_bal = balance
                today["Shares"] = 0
                earned = closing_price * num_shares
                trades[trades_idx] += earned
                trades_idx += 1
                today["Position"] = "NA"
                today["Holdings Value"] = 0
                cash = balance + earned
                today["Cash"] = cash

                # Update new daily balance & holdings after closing long position
                balance = balance + cash
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = balance - start_bal
                in_position = False
            elif action == "Exit Short" and in_position:
                # Buy n shares
                start_bal = balance
                today["Shares"] = 0
                spent = closing_price * num_shares
                trades[trades_idx] -= spent
                trades_idx += 1
                today["Position"] = "NA"
                today["Holdings Value"] = 0
                cash = balance - spent
                today["Cash"] = cash

                # Update new daily balance & holdings after closing long position
                balance = balance + cash
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = balance - start_bal
                in_position = False
            else:
                sys.exit("Simulation Failed")
            
            # Add daily simulation result to overall simulation 
            simulation_data.append(today)
            idx += 1
        
        # Calculate evaluation metrics (Total P/L, Win Rate, Sharpe)
        total_profit_loss = balance - amount

        wins = sum(1 for trade in trades if trade > 0)
        win_rate = wins / len(trades) * 100

        risk_free_per_trade = (float(risk_free_rate) / 100) / len(trades)  # Same unit for mean, s.d., risk free rate
        sharpe = (np.mean(trades) - risk_free_per_trade) / np.std(trades)

        evaluation_data.append({"Total P/L": total_profit_loss, "Win Rate": win_rate, "Sharpe Ratio": sharpe})
        simulation = evaluation_data + simulation_data

        # Write results to csv
        writer = csv.writer(file)
        metrics = simulation[0]
        writer.writerow(metrics.keys())
        writer.writerow(metrics.values())
        daily_data = simulation[1:]
        headers = daily_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(daily_data)

    return simulation


def display(simulation):
    # Display simulation metrics & data
    sim_metrics = simulation[0]
    sim_data = simulation[1]
    dates = [row["Date"] for row in sim_data]
    ending_bal = [row["Ending Balance"] for row in sim_data]
    price = [row["Price (Close)"] for row in sim_data]
    
    print(sim_metrics)
    fig, graph1 = plt.subplots()

    graph1.plot(dates, ending_bal, "b-o", label="Balance")
    graph1.set_xlabel("Date")
    graph1.set_ylabel("Balance", color="b")
    graph1.tick_params(axis="y", labelcolor="b")
    graph2 = graph1.twinx()
    graph2.plot(dates, price, "r-s", label="Price (Close)")
    graph2.set_ylabel("Price (Close)", color="r")
    graph2.tick_params(axis="y", labelcolor="r")

    plt.xticks(rotation=45)
    plt.title("Balance & Price over Time")
    plt.grid(True)
    fig.tight_layout()
    plt.show() 

    return "Success"
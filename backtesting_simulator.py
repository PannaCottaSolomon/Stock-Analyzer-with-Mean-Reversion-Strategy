import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simulate(df_price, signals, amount, risk_free_rate):
    simulation_data = []
    evaluation_data = []
    simulation = []

    with open("simulation.csv", "w") as file:
        balance = float(amount)
        num_shares = 0
        idx = 0
        position_type = "None"  # "None", "Long", or "Short"
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
            if action == "Enter Long" and position_type == "None":
                # Buy shares with all available cash
                start_bal = balance
                num_shares = int(balance / closing_price)
                today["Shares"] = num_shares
                spent = closing_price * num_shares
                trades.append(-1 * spent)  # Negative for buy
                today["Position"] = "Long"
                today["Holdings Value"] = num_shares * closing_price
                cash = balance - spent
                today["Cash"] = cash

                # Update balance (cash remaining after purchase)
                balance = cash
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = 0  # No P/L on entry
                position_type = "Long"
                
            elif action == "Enter Short" and position_type == "None":
                # Short sell shares (borrow and sell)
                start_bal = balance
                num_shares = int(balance / closing_price)
                today["Shares"] = -num_shares  # Negative for short
                earned = closing_price * num_shares
                trades.append(earned)  # Positive for short sell
                today["Position"] = "Short"
                today["Holdings Value"] = -num_shares * closing_price
                cash = balance + earned
                today["Cash"] = cash

                # Update balance (cash from short sale)
                balance = cash
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = 0  # No P/L on entry
                position_type = "Short"
                
            elif action == "Exit Long" and position_type == "Long":
                # Sell long position
                start_bal = balance
                today["Shares"] = 0
                earned = closing_price * num_shares
                trades[trades_idx] += earned  # Add sale proceeds to buy cost
                trades_idx += 1
                today["Position"] = "None"
                today["Holdings Value"] = 0
                cash = balance + earned
                today["Cash"] = cash

                # Update balance (cash from sale)
                balance = cash
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = earned - (num_shares * closing_price)  # P/L from position
                position_type = "None"
                
            elif action == "Exit Short" and position_type == "Short":
                # Buy back short position
                start_bal = balance
                today["Shares"] = 0
                spent = closing_price * num_shares
                trades[trades_idx] -= spent  # Subtract buy cost from short sale proceeds
                trades_idx += 1
                today["Position"] = "None"
                today["Holdings Value"] = 0
                cash = balance - spent
                today["Cash"] = cash

                # Update balance (cash after buying back)
                balance = cash
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = (num_shares * closing_price) - spent  # P/L from position
                position_type = "None"
                
            elif action == "Hold":
                # No action, just track current position value
                start_bal = balance
                if position_type == "Long":
                    today["Shares"] = num_shares
                    today["Position"] = "Long"
                    today["Holdings Value"] = num_shares * closing_price
                    today["Cash"] = balance
                    today["Ending Balance"] = balance + (num_shares * closing_price)
                    today["P/L (Daily)"] = num_shares * (closing_price - closing_price)  # No change if same price
                elif position_type == "Short":
                    today["Shares"] = -num_shares
                    today["Position"] = "Short"
                    today["Holdings Value"] = -num_shares * closing_price
                    today["Cash"] = balance
                    today["Ending Balance"] = balance + (-num_shares * closing_price)
                    today["P/L (Daily)"] = -num_shares * (closing_price - closing_price)  # No change if same price
                else:
                    today["Shares"] = 0
                    today["Position"] = "None"
                    today["Holdings Value"] = 0
                    today["Cash"] = balance
                    today["Ending Balance"] = balance
                    today["P/L (Daily)"] = 0
            else:
                # Invalid action/position combination
                print(f"Invalid action: {action} with position: {position_type}")
                today["Shares"] = num_shares if position_type == "Long" else (-num_shares if position_type == "Short" else 0)
                today["Position"] = position_type
                today["Holdings Value"] = 0
                today["Cash"] = balance
                today["Ending Balance"] = balance
                today["P/L (Daily)"] = 0
            
            # Add daily simulation result to overall simulation 
            simulation_data.append(today)
            idx += 1
        
        # Calculate evaluation metrics (Total P/L, Win Rate, Sharpe)
        final_balance = simulation_data[-1]["Ending Balance"]
        total_profit_loss = final_balance - amount

        # Calculate win rate from completed trades
        completed_trades = trades[:trades_idx] if trades_idx > 0 else []
        wins = sum(1 for trade in completed_trades if trade > 0)
        win_rate = (wins / len(completed_trades) * 100) if completed_trades else 0

        # Calculate Sharpe ratio
        if completed_trades and len(completed_trades) > 1:
            risk_free_per_trade = (float(risk_free_rate) / 100) / len(completed_trades)
            sharpe = (np.mean(completed_trades) - risk_free_per_trade) / np.std(completed_trades)
        else:
            sharpe = 0

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
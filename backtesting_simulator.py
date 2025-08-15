import sys
import pandas as pd
import numpy


def simulate(df_price, signals, amount):
    simulation_data = []
    evaluation_data = []

    with open("simulation.csv") as file:
        balance = float(amount)
        num_shares = 0
        idx = 0
        in_position = False

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
        
        # Calculate evaluation metrics
        total_profit_loss = balance - amount
        

    simulation = evaluation_data + simulation_data
    return simulation
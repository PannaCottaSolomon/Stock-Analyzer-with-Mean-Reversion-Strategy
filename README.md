# Stock Analyzer with Mean Reversion Strategy
#### Video Demo: https://youtu.be/gRbVQzQtPr0
#### Description: A comprehensive stock analyzer that implements a mean reversion trading strategy using technical indicators including Bollinger Bands, RSI (Relative Strength Index), and moving averages. The system executes and simulates trades over a specified time period, providing detailed backtesting results and performance metrics.

## Features

### Technical Analysis
- **Bollinger Bands**: Uses 20-day EMA with 1 standard deviation bands to identify oversold/overbought conditions
- **RSI (14-period)**: Momentum oscillator to confirm entry signals (oversold < 30, overbought > 70)
- **Moving Average Crossover**: Uses 50-day and 200-day EMA for trend confirmation (golden/death cross)
- **Mean Reversion Strategy**: Exits positions when price returns to the 20-day EMA

### Trading Logic
- **Long Entry**: Price below lower Bollinger Band + RSI < 30 + bullish trend (50-day EMA > 200-day EMA)
- **Short Entry**: Price above upper Bollinger Band + RSI > 70 + bearish trend (50-day EMA < 200-day EMA)
- **Exit Conditions**: Price returns to 20-day EMA for both long and short positions

### Backtesting & Analysis
- Complete trade simulation with position tracking
- Performance metrics: Total P/L, Win Rate, Sharpe Ratio
- Visual charts showing balance and price movement over time
- Detailed CSV export of all trades and daily positions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Stock-Analyzer-with-Mean-Reversion-Strategy
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Analyzer
```bash
python project.py
```

The program will prompt you for:
- **Ticker Symbol**: Stock symbol to analyze (e.g., AAPL, MSFT)
- **Time Period**: Number of days to backtest (e.g., 252 for 1 trading year)
- **Initial Capital**: Starting amount in USD (e.g., 10000)
- **Risk-Free Rate**: Annual risk-free rate as percentage (e.g., 5)

### Example Usage
```
Ticker: AAPL
Length of time (days): 252
Initial Amount: 10000
Risk-Free Rate (Annual): 5
```

### Output
The program generates:
1. **Console Output**: Summary of key performance metrics
2. **CSV File**: `simulation_results.csv` with detailed trade-by-trade results
3. **PDF Chart**: `simulation_performance_{TICKER}.pdf` showing balance and price over time
4. **Interactive Plot**: Real-time visualization of performance

## File Structure

```
├── project.py                 # Main application file
├── backtesting_simulator.py   # Trading simulation engine
├── test_project.py           # Unit tests
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## API Configuration

The project uses Alpha Vantage API for real-time financial data. You'll need to:
1. Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Update the `APIKEY` variable in `project.py` with your key

```python
APIKEY = "YOUR_API_KEY_HERE"
```

## Testing

Run the test suite to verify functionality:
```bash
python test_project.py
```

Or using pytest:
```bash
pytest test_project.py -v
```

## Performance Metrics

### Output Metrics
- **Total P/L**: Net profit/loss from all completed trades
- **Win Rate**: Percentage of profitable trades
- **Sharpe Ratio**: Risk-adjusted return measure

### Trading Statistics
- Position tracking (Long/Short/None)
- Daily P/L calculations
- Cash and holdings value monitoring
- Complete trade history

## Technical Requirements

### Dependencies
- **requests**: API calls to Alpha Vantage
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Chart generation and visualization
- **pytest**: Unit testing framework

### Python Version
- Python 3.7 or higher recommended

## Limitations & Considerations

1. **API Rate Limits**: Alpha Vantage free tier has call limits (5 calls per minute, 500 per day)
2. **Historical Data Only**: Uses past data for backtesting (not real-time trading)
3. **Single Asset**: Currently supports one ticker at a time
4. **No Transaction Costs**: Simulation doesn't include brokerage fees or slippage
5. **Market Hours**: Assumes continuous trading without gaps

## Future Improvements

### Planned Features
- **Multi-Asset Portfolio**: Extend to multiple tickers and portfolio-level backtesting
- **Risk Management**: Position sizing and stop-loss mechanisms
- **Advanced Strategies**: Additional technical indicators and strategy combinations
- **Real-time Trading**: Integration with brokerage APIs
- **Web Interface**: User-friendly web dashboard
- **Database Storage**: Historical data caching and storage


### Potential Enhancements
- Machine learning integration for signal optimization
- Options trading strategies
- Sector rotation and market regime detection
- Advanced performance attribution analysis

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is for educational purposes. Always perform your own research and consider the risks before making investment decisions.

## Disclaimer

This software is for educational and research purposes only. It should not be considered as financial advice. Trading stocks involves risk, and past performance does not guarantee future results. Always consult with a qualified financial advisor before making investment decisions.
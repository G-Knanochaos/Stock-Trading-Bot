# Stock-Trading-Bot
Current Specs:
- Updates every morning (with clock checker)
- Thin triple-layer SR identification
- Thin double-layer trend determination using 'Close' price points (better to compare prices during similar times of the day)
- Uses top 10 stocks filter, elimates all STCT (strength trend contradiction test) failures

I am working to improve this program's effeciency and plan to make different versions for testing. If you do plan on using/testing this code while it is in development, make sure to check the config folder and change API_KEY and SECRET_KEY.

HOW TO USE:

Prerequistes: Create Alpaca Account (paper or real), Find the API key and API secret and plug it into the config.py file

Every night, at any time, run the main.py file (figure out how to do this based on your operating system). It will ask you whether or not to oveerride market wait. If you want the program to wait until market open to run, type 'n'. If not, type 'y'. The file will run and (assuming you plugged it into your alpaca account) and buy whichever stocks it chooses based on its analyses. 

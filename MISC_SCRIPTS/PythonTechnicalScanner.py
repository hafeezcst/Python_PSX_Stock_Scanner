from pickle import FALSE
from re import T
from threading import Thread
import datetime
from concurrent.futures import ThreadPoolExecutor
from prometheus_client import Summary
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import time
import mplfinance as mpf
import matplotlib.pyplot as plt
# Define the list of symbols
psx_symbols_KMIALL = [
"ABOT",
"ACPL",
"ADAMS",
"AGHA",
"AGIL",
"AGP",
"AGTL",
"AIRLINK",
"ALNRS",
"ANL",
"APL",
"ARCTM",
"ARPL",
"ASC",
"ASTM",
"ATBA",
"ATLH",
"ATRL",
"AVN",
"BAFS",
"BATA",
"BCL",
"BECO",
"BERG",
"BGL",
"BIFO",
"BIPL",
"BNL",
"BNWM",
"BPL",
"BUXL",
"BWCL",
"BWHL",
"CEPB",
"CHAS",
"CHCC",
"CLOV",
"CLVL",
"COLG",
"CPHL",
"CRTM",
"CSAP",
"CTM",
"DAAG",
"DADX",
"DAWH",
"DCL",
"DCR",
"DFSM",
"DGKC",
"DOL",
"DYNO",
"EFERT",
"EMCO",
"ENGRO",
"EPCL",
"EXIDE",
"FABL",
"FATIMA",
"FCCL",
"FCEPL",
"FECTC",
"FEM",
"FEROZ",
"FFBL",
"FHAM",
"FIBLM",
"FLYNG",
"FPRM",
"FRCL",
"FRSM",
"FTMM",
"FUDLM",
"FZCM",
"GAL",
"GAMON",
"GATI",
"GGGL",
"GGL",
"GHGL",
"GHNI",
"GLAXO",
"GLPL",
"GVGL",
"GWLC",
"HAEL",
"HALEON",
"HCAR",
"HINO",
"HINOON",
"HTL",
"HUBC",
"IBLHL",
"ICL",
"ILP",
"IMAGE",
"INIL",
"ISL",
"ITTEFAQ",
"JSML",
"JVDC",
"KEL",
"KOHC",
"KOHE",
"KOHP",
"KOHTM",
"KSBP",
"KTML",
"LCI",
"LEUL",
"LOTCHEM",
"LPGL",
"LPL",
"LUCK",
"MACFL",
"MARI",
"MEBL",
"MERIT",
"META",
"MFFL",
"MLCF",
"MODAM",
"MSCL",
"MTL",
"MUGHAL",
"NCPL",
"NETSOL",
"NML",
"NRL",
"OBOY",
"OGDC",
"OLPM",
"OML",
"ORM",
"PABC",
"PAEL",
"PAKD",
"PHDL",
"PIBTL",
"PICT",
"PIOC",
"PKGP",
"PKGS",
"PMI",
"PNSC",
"POML",
"POWER",
"PPL",
"PPP",
"PREMA",
"PRL",
"PSEL",
"PSMC",
"PSO",
"PSYL",
"PTL",
"QUET",
"QUICE",
"RMPL",
"RPL",
"RUPL",
"SANSM",
"SARC",
"SASML",
"SAZEW",
"SCL",
"SEARL",
"SFL",
"SGF",
"SGPL",
"SHDT",
"SHEL",
"SHEZ",
"SHFA",
"SHSML",
"SINDM",
"SITC",
"SNAI",
"SNGP",
"SPEL",
"SPL",
"DEF",
"SSGC",
"STCL",
"STML",
"STPL",
"SURC",
"SYS",
"TCORP",
"TELE",
"TGL",
"THALL",
"THCCL",
"TICL",
"TOMCL",
"TOWL",
"TPL",
"TPLP",
"TREET",
"UBDL",
"UCAPM",
"UDPL",
"UNITY",
"WAHN",
"WAVES",
"WTL",
"ZIL",
"ZTL"
]
psx_symbols_KMI100 = [
"MLCF",
"PAEL",
"FFBL",
"FCCL",
"DGKC",
"KEL",
"PPL",
"OGDC",
"SEARL",
"UNITY",
"PIOC",
"AVN",
"CHCC",
"SNGP",
"MUGHAL",
"PSO",
"ILP",
"PIBTL",
"NML",
"EPCL",
"HUBC",
"FCEPL",
"GHGL",
"CEPB",
"ENGRO",
"SHEL",
"ATRL",
"MEBL",
"BIPL",
"EFERT",
"LUCK",
"DCR",
"PABC",
"ISL",
"NRL",
"INIL",
"FABL",
"MTL",
"TGL",
"HINOON",
"AGP",
"LOTCHEM",
"SYS",
"KTML",
"MARI",
"DAWH",
"KOHC",
"BNWM",
"FATIMA",
"GLAXO",
"SHFA",
"PKGS",
"POML",
"APL",
"ARPL",
"JVDC",
"BWCL",
"FHAM",
"THALL",
"LCI",
"PKGP",
"ABOT",
"COLG",
"RMPL",
"PSEL"
]
psx_symbols_KMI30 = ["APL",
"ATRL",
"AVN",
"CHCC",
"DAWH",
"DGKC",
"EFERT",
"ENGRO",
"EPCL",
"FCCL",
"HUBC",
"LOTCHEM",
"LUCK",
"MARI",
"MEBL",
"MLCF",
"MTL",
"NETSOL",
"NRL",
"OGDC",
"PAEL",
"PIOC",
"PPL",
"PRL",
"PSO",
"SHEL",
"SNGP",
"SYS",
"TPLP",
"UNITY"
] 
psx_symbols_QSE= [
"QNBK",
"IQCD",
"QIBK",
"ORDS",
"ERES",
"MARK",
"CBQK",
"MPHC",
"DUBK",
"QEWS",
"QGTS",
"QFLS",
"QIIK",
"QNNS",
"BRES",
"ABQK",
"QATI",
"VFQS",
"QAMC",
"IGRD",
"AHCS",
"GISS",
"DHBK",
"ZHCD",
"UDCD",
"MERS",
"QNCD",
"BLDN",
"QIGD",
"MEZA",
"GWCS",
"MCCS",
"MCGS",
"QFBQ",
"QIMD",
"QISI",
"DOHI",
"QGRI",
"QLMI",
"MRDS",
"SIIS",
"AKHI",
"MKDM",
"WDAM",
"NLCS",
"MHAR",
"QOIS",
"DBIS",
"IHGS",
"FALH",
"QCFS",
"QGMD",
"BEMA",
]
psx_symbols_mylist = [ 
"AGSML",
"ASL",
"AGTL",
"ATRL",
"BIFO",
"CHCC",
"DOL",
"DYNO",
"ENGRO",
"EFERT",
"EXIDE",
"GHNI",
"HCAR",
"HUBC",
"IMAGE",
"INIL",
"ICL",
"LOTCHEM",
"MLCF",
"MARI",
"MEBL",
"MEEZ",
"MLT",
"MUGHAL",
"NRL",
"NETSOL",
"NML",
"PAEL",
"PIBTL",
"PNSC",
"QUICE",
"SAZEW",
"STCL",
"SHEL",
"SPL",
"SYS",
"UNITY",
"WAVES",
"WHALE",
"WTL",
]
def analyze_symbol(symbol, analysis_type, base_url_charts,base_url_finan,base_url_tech):
    try:
        if analysis_type == "M":
            analysis = TA_Handler(symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=Interval.INTERVAL_1_MONTH)
        elif analysis_type == "W":
            analysis = TA_Handler(symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=Interval.INTERVAL_1_WEEK)
        elif analysis_type == "D":
            analysis = TA_Handler(symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=Interval.INTERVAL_1_DAY)
        elif analysis_type == "H":
            analysis = TA_Handler(symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=Interval.INTERVAL_1_HOUR)
        
        if 'analysis' in locals() and analysis is not None and analysis.get_analysis() is not None:
            summary = analysis.get_analysis().summary
           
            if summary is not None: 
                Buy_Signal      = summary['BUY']
                Sell_Signal     = summary['SELL']
                Neutral_Signal  = summary['NEUTRAL']
                RSI             = analysis.get_analysis().indicators['RSI']
                RSI_Last        = analysis.get_analysis().indicators['RSI[1]']
                Close           = analysis.get_analysis().indicators['close']
                Volume          = analysis.get_analysis().indicators['volume']
                AO              = analysis.get_analysis().indicators['AO']
                Change          = analysis.get_analysis().indicators['change']    
                            
                # Construct the website link
                Charts = f"{base_url_charts}{symbol}"
                Financials = f"{base_url_finan}{symbol}/financials-overview/"
                Technicals = f"{base_url_tech}{symbol}/technicals/"

                return symbol, summary, Close,Buy_Signal,Sell_Signal,Neutral_Signal, Volume, RSI, RSI_Last, AO, Change, Charts, Financials, Technicals

    except Exception as e:
        print(f"Exception occurred for symbol: {symbol}")
    return None

def sort_excel(excel_file_path):
    try:
        # Specify the encoding (e.g., 'utf-8', 'latin-1', etc.) based on your file's encoding
        df = pd.read_excel(excel_file_path, parse_dates=['Date and Time'])
        df = df.sort_values(by=['Symbol', 'Date and Time'], ascending=[True, False])
        df.to_excel(excel_file_path, index=True, encoding='utf-8')  # Specify encoding when writing as well
        print(f"CSV file sorted by Symbol and Date and Time.")
    except Exception as e:
        print(f"Error sorting CSV file: {e}")

import mplfinance as mpf
import matplotlib.pyplot as plt

# ...

# ...

def plot_candlestick(symbol, analysis_type, base_url_charts, base_url_finan, base_url_tech):
    try:
        # Perform technical analysis
        analysis = TA_Handler(symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=Interval.INTERVAL_1_DAY)

        if analysis and analysis.get_analysis():
            # Check if candles data is available
            if hasattr(analysis, 'get_candles') and analysis.get_candles():
                # Extract relevant data
                data = analysis.get_candles()

                if not data.empty:
                    # Plot candlestick chart
                    mpf.plot(data, type='candle', mav=(50, 200), volume=True, show_nontrading=True, title=f'Candlestick Chart for {symbol}')

                    # Show RSI chart
                    if 'RSI' in data.columns:
                        plt.figure()
                        plt.plot(data['time'], data['RSI'], label='RSI')
                        plt.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
                        plt.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
                        plt.title(f'RSI for {symbol}')
                        plt.xlabel('Date')
                        plt.ylabel('RSI')
                        plt.legend()
                        plt.show()
                else:
                    print(f"No data available for symbol {symbol}")

            else:
                print(f"Candles data not available for symbol {symbol}")

        else:
            print(f"Data not available for symbol {symbol}")

    except Exception as e:
        print(f"Exception occurred while plotting for symbol {symbol}: {e}")

# ...



def run_analysis_daily():
    while True:
        current_datetime = datetime.datetime.now().strftime("%m:%d:%Y %H:%M:%S")  # Include time
        print(f"Technical Analysis Date and Time: {current_datetime}")

        analyzed_data.clear()

        # Sleep for a while to avoid excessive resource consumption
        time.sleep(60)  # Sleep for 1 minute

def main():
    
    analysis_type = input("Select analysis type (M for Monthly, W for Weekly, D for Daily,H for Hourly, press Enter for default H): ").upper()
    
    recommendation_options = ["STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL"]
    recommendation_filter = input(f"Select recommendation filter ({', '.join(recommendation_options)}): ").upper()
    while recommendation_filter not in recommendation_options:
        print("Invalid recommendation filter. Please try again.")
        recommendation_filter = input(f"Select recommendation filter ({', '.join(recommendation_options)}): ").upper()
    
    volume_theshold = 1000000  # Filter by this volume threshold
    AO_threshold    = 0  # Filter by this AO threshold
    base_url_charts = "https://www.tradingview.com/chart/ZMYE714n/?symbol=PSX%3A"  # Set the base URL
    base_url_finan = "https://www.tradingview.com/symbols/PSX-"  # Set the base URL
    base_url_tech = "https://www.tradingview.com/symbols/PSX-"  # Set the base URL
    # Set default analysis type to "M" if the user presses Enter without entering a choice
    if not analysis_type:
        analysis_type = "M"
    
    print(f"Selected analysis type: {analysis_type}")
    print()

    if analysis_type not in ["M", "W", "D", "H"]:
        raise ValueError("Invalid analysis type. Please select M, W, D, or H")

    current_datetime = datetime.datetime.now().strftime("%m:%d:%Y %H:%M:%S")  # Include time
    print(f"Technical Analysis Date and Time: {current_datetime}")
    count = 1


    # Create a thread pool
    with ThreadPoolExecutor(max_workers=500) as executor:  # Adjust max_workers as needed
        # Submit tasks to the thread pool
        
        symbol_options = ["KMIALL", "KMI100", "KMI30", "MYLIST", "QSE" ]
        symbol_selection = input(f"Select symbol List ({', '.join(symbol_options)}), press Enter for default KSIALL: ").upper()
        while symbol_selection not in symbol_options:
            print("Invalid symbol selection. Please try again.")
            symbol_selection = input(f"Select symbol ({', '.join(symbol_options)}), press Enter for default KSIALL: ").upper()

        if symbol_selection == "KMI30":
            psx_symbols = psx_symbols_KMI30
        elif symbol_selection == "KMI100":
            psx_symbols = psx_symbols_KMI100
        elif symbol_selection == "MYLIST":
            psx_symbols = psx_symbols_mylist
        elif symbol_selection == "QSE":
            psx_symbols = psx_symbols_QSE
        else:
            psx_symbols = psx_symbols_KMIALL



        futures = [executor.submit(analyze_symbol, symbol, analysis_type, base_url_charts, base_url_finan, base_url_tech) for symbol in psx_symbols]

        # Process completed tasks
        analyzed_data = []
        strong_buy_symbols = []  # List to store symbols with a "STRONG_BUY" recommendation

        for future in futures:
            result = future.result()
            if result:
                symbol, summary,Buy_Signal,Sell_Signal,Neutral_Signal,Close, Volume, RSI, RSI_Last, AO , Change ,base_url_charts,base_url_finan,base_url_tech = result
                print(f"{count}:  Symbol: {symbol}")
                summary= (summary.get('RECOMMENDATION'))
                print(summary)
                print(f"{analysis_type} Buy_Signal:{Buy_Signal},Sell_Signal:{Sell_Signal},Neutral_Signal:{Neutral_Signal},CLOSE: {Close} Volume: {Volume} RSI: {RSI} LAST RSI: {RSI_Last} AO: {AO} %Change(D): {Change} ")
                print()
                count += 1

                # check and Append data to the list for CSV export if volme is greater than 5000
                if Volume > 5000:
                    analyzed_data.append([current_datetime, symbol, summary, Buy_Signal,Sell_Signal,Neutral_Signal,Close, Volume, RSI, RSI_Last, AO, Change,base_url_charts,base_url_finan,base_url_tech])

                # Check if the recommendation is "user defined" and the volume is greater than the threshold
                if summary == recommendation_filter and Volume > volume_theshold:
                    strong_buy_symbols.append([current_datetime, symbol, summary, Buy_Signal,Sell_Signal,Neutral_Signal,Close, Volume, RSI, RSI_Last, AO, Change,base_url_charts,base_url_finan,base_url_tech])

        # Export data to a single Excel file with two sheets

        # Get the current date
        current_date = datetime.datetime.now().strftime("%Y%m%d")

        # Set the file name with the analysis date as a postfix
        excel_file_path = f"Technical_Analysis_{symbol_selection}_{analysis_type}_{recommendation_filter}_{current_date}.xlsx"
        with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
            
             # Create DataFrames from the lists
            df_all = pd.DataFrame(analyzed_data, columns            =['Date and Time', 'Symbol', 'Summary','Buy','Sell','Neutral', f'{analysis_type} Close', 'Volume', 'RSI', 'Last RSI', 'AO', '%Change(D)','Charts','Financials','Technicals'])
            df_strong_buy = pd.DataFrame(strong_buy_symbols, columns=['Date and Time', 'Symbol', 'Summary','Buy','Sell','Neutral',f'{analysis_type} Close', 'Volume', 'RSI', 'Last RSI', 'AO', '%Change(D)','Charts','Financials','Technicals'])


            # Write DataFrames to Excel sheets
            df_all.to_excel(writer, sheet_name='All Symbols', index=True)
            df_strong_buy.to_excel(writer, sheet_name=f'{recommendation_filter}_Symbols', index=True)

            # Get the workbook and the worksheet objects
            workbook = writer.book
            worksheet_all = writer.sheets['All Symbols']
            worksheet_strong_buy = writer.sheets[f'{recommendation_filter}_Symbols']

            # Define the format for highlighting
            highlight_format = workbook.add_format({'bg_color': '#FFC7CE'})

            # Apply conditional formatting to the 'All Symbols' sheet
            worksheet_all.conditional_format('A2:M1000', {'type': 'formula',
                                                          'criteria': 'AND($J2>50, $L2>0)',
                                                          'format': highlight_format})

            # Apply conditional formatting to the '{recommendation_filter}_Symbols' sheet
            worksheet_strong_buy.conditional_format('A2:M1000', {'type': 'formula',
                                                                 'criteria': 'AND($J2>50, $L2>0)',
                                                                 'format': highlight_format})
           
        print(f"Data exported to {excel_file_path}")

        # Sort the Excel file by symbol and date and time
        #sort_excel(excel_file_path)
    
    
            

if __name__ == "__main__":
    analyzed_data = []  # Moved analyzed_data outside the loop to persist data across runs
    # Schedule the daily analysis to run continuously
    Thread(target=run_analysis_daily, daemon=True).start()
    # Run the main analysis
    main()
import pandas as pd
from get_analysis_type import analysis_type
def write_to_excel(df_all, df_strong_buy, df_buy, df_sell, excel_file_path):
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        subset_columns = ['Symbol', 'Summary', f'{analysis_type} Close', 'Sell', 'Neutral', 'Buy', 'Volume', 'ADX', 'RSI', 'Last RSI', 'AO', '%Change(D)', 'Support', 'Resistance']

        for df, sheet_name in zip([df_all, df_strong_buy, df_buy, df_sell], ['All Symbols', 'Recommended_Symbols', 'Buy_Symbols', 'Sell_Symbols']):
            if df is not None:
                df = df.drop_duplicates(subset=subset_columns, keep='last')
                df.to_excel(writer, sheet_name=sheet_name, index=False)

                workbook = writer.book
                worksheet = writer.sheets[sheet_name]

                # Apply conditional formatting
                # ...

    print(f"Data exported to {excel_file_path}")
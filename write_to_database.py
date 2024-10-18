import sqlalchemy

def write_to_database(df_all, df_strong_buy, df_buy, df_sell, database_url):
    engine = sqlalchemy.create_engine(database_url)
    
    if df_all is not None or df_strong_buy is not None or df_buy is not None or df_sell is not None:
        df_all.to_sql('all_symbols', engine, if_exists='append', index=False)
        df_strong_buy.to_sql('recommended_symbols', engine, if_exists='append', index=False)
        df_buy.to_sql('buy_symbols', engine, if_exists='append', index=False)
        df_sell.to_sql('sell_symbols', engine, if_exists='append', index=False)
    else:
        print("df_all is None")
from stock_advisor.api.gpt_interface import interpret_prompt

if __name__ == "__main__":
    query1 = "show me MSTF for the last 1 days, 5 min chart"
    params1 = interpret_prompt(query1)
    print("query1", params1)

    query2 = "show me MSTF vs APPL for the last 1 day"
    params2 = interpret_prompt(query2)
    print("query2", params2)

    ### Output ###
    # query1 {'ticker': 'MSFT', 'timeframe': '1d', 'interval': '5m'}
    # query2 {'ticker': 'MSFT', 'timeframe': '1d'}

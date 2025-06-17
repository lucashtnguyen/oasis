from stock_advisor.api.gpt_interface import interpret_prompt
from stock_advisor.api.query import handle_query

if __name__ == "__main__":
    # query1 = "plot MSTF for the last 1 days, 5 min chart"
    # params1 = interpret_prompt(query1)
    # print(f"Query: {query1}\n", params1)
    # handle_query(query1, output_dir=None, show=True)

    # query2 = "show me MSTF vs APPL for the last 1 days, 5 min chart"
    # params2 = interpret_prompt(query2)
    # print(f"Query: {query2}\n", params2)
    # handle_query(query2, output_dir=None, show=True)

    # query3 = "compare MSTF vs APPL"
    # params3 = interpret_prompt(query3)
    # print(f"Query: {query3}\n", params3)
    # handle_query(query3, output_dir=None, show=True)

    query3 = "Plot the volitility of MSFT for the last year"
    params3 = interpret_prompt(query3)
    print(f"Query: {query3}\n", params3)
    handle_query(query3, output_dir=None, show=True)

    ### Output ###
    # query1 {'ticker': 'MSFT', 'timeframe': '1d', 'interval': '5m'}
    # query2 {'ticker': 'MSFT', 'timeframe': '1d'}

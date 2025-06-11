from stock_advisor.api.gpt_interface import interpret_prompt

if __name__ == "__main__":
    query = "show me MSTF for the last 1 days, 5 min chart"
    params = interpret_prompt(query)
    print(params)

import gradio as gr
from accounts import Account, get_share_price

# Initialize account with $0 (will create a real one when user creates account)
account = None

def create_account(initial_deposit):
    """Create a new account with the specified initial deposit."""
    global account
    try:
        initial_deposit = float(initial_deposit)
        account = Account(initial_deposit)
        return f"Account created with initial deposit of ${initial_deposit:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def deposit_funds(amount):
    """Deposit funds into the account."""
    global account
    if account is None:
        return "Error: Please create an account first."
    
    try:
        amount = float(amount)
        account.deposit(amount)
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    """Withdraw funds from the account."""
    global account
    if account is None:
        return "Error: Please create an account first."
    
    try:
        amount = float(amount)
        if account.withdraw(amount):
            return f"Successfully withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
        else:
            return f"Error: Insufficient funds. Current balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    """Buy shares of the specified stock."""
    global account
    if account is None:
        return "Error: Please create an account first."
    
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        
        price = get_share_price(symbol)
        if price == 0.0:
            return f"Error: Invalid stock symbol '{symbol}'. Available stocks: AAPL, TSLA, GOOGL"
        
        total_cost = price * quantity
        
        if account.buy_shares(symbol, quantity):
            return f"Successfully bought {quantity} shares of {symbol} at ${price:.2f} each. Total cost: ${total_cost:.2f}. New balance: ${account.balance:.2f}"
        else:
            return f"Error: Insufficient funds to buy {quantity} shares of {symbol} at ${price:.2f} each (${total_cost:.2f}). Current balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    """Sell shares of the specified stock."""
    global account
    if account is None:
        return "Error: Please create an account first."
    
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        
        price = get_share_price(symbol)
        if price == 0.0:
            return f"Error: Invalid stock symbol '{symbol}'. Available stocks: AAPL, TSLA, GOOGL"
        
        total_value = price * quantity
        
        if account.sell_shares(symbol, quantity):
            return f"Successfully sold {quantity} shares of {symbol} at ${price:.2f} each. Total value: ${total_value:.2f}. New balance: ${account.balance:.2f}"
        else:
            holdings = account.get_holdings()
            current_quantity = holdings.get(symbol, 0)
            return f"Error: Insufficient shares to sell. You have {current_quantity} shares of {symbol}, but tried to sell {quantity}."
    except ValueError as e:
        return f"Error: {str(e)}"

def get_account_summary():
    """Get a summary of the account including balance, holdings, and profit/loss."""
    global account
    if account is None:
        return "Error: Please create an account first."
    
    summary = []
    summary.append(f"Cash Balance: ${account.balance:.2f}")
    
    portfolio_value = account.get_portfolio_value()
    summary.append(f"Portfolio Value: ${portfolio_value:.2f}")
    
    profit_loss = account.get_profit_or_loss()
    summary.append(f"Profit/Loss: ${profit_loss:.2f} ({profit_loss/account.initial_deposit*100:.2f}%)")
    
    holdings = account.get_holdings()
    if holdings:
        summary.append("\nCurrent Holdings:")
        for symbol, quantity in holdings.items():
            price = get_share_price(symbol)
            value = price * quantity
            summary.append(f"  {symbol}: {quantity} shares at ${price:.2f} = ${value:.2f}")
    else:
        summary.append("\nNo current holdings.")
    
    return "\n".join(summary)

def get_transaction_history():
    """Get the transaction history for the account."""
    global account
    if account is None:
        return "Error: Please create an account first."
    
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions recorded."
    
    history = ["Transaction History:"]
    for i, transaction in enumerate(transactions, 1):
        t_type = transaction["type"]
        amount = transaction["amount"]
        
        if t_type == "DEPOSIT":
            history.append(f"{i}. DEPOSIT: ${amount:.2f}")
        elif t_type == "WITHDRAW":
            history.append(f"{i}. WITHDRAW: ${amount:.2f}")
        elif t_type == "BUY":
            symbol = transaction["symbol"]
            quantity = transaction["quantity"]
            price = amount / quantity
            history.append(f"{i}. BUY: {quantity} shares of {symbol} at ${price:.2f} each, total ${amount:.2f}")
        elif t_type == "SELL":
            symbol = transaction["symbol"]
            quantity = transaction["quantity"]
            price = amount / quantity
            history.append(f"{i}. SELL: {quantity} shares of {symbol} at ${price:.2f} each, total ${amount:.2f}")
    
    return "\n".join(history)

def get_current_prices():
    """Get the current prices of available stocks."""
    stocks = ["AAPL", "TSLA", "GOOGL"]
    prices = [f"{stock}: ${get_share_price(stock):.2f}" for stock in stocks]
    return "Current Stock Prices:\n" + "\n".join(prices)

# Create the Gradio interface
with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Create Account")
                create_account_input = gr.Textbox(label="Initial Deposit ($)")
                create_account_button = gr.Button("Create Account")
                create_account_output = gr.Textbox(label="Result")
                
                create_account_button.click(
                    create_account,
                    inputs=create_account_input,
                    outputs=create_account_output
                )
            
            with gr.Column():
                gr.Markdown("### Deposit Funds")
                deposit_input = gr.Textbox(label="Amount ($)")
                deposit_button = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Result")
                
                deposit_button.click(
                    deposit_funds,
                    inputs=deposit_input,
                    outputs=deposit_output
                )
            
            with gr.Column():
                gr.Markdown("### Withdraw Funds")
                withdraw_input = gr.Textbox(label="Amount ($)")
                withdraw_button = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Result")
                
                withdraw_button.click(
                    withdraw_funds,
                    inputs=withdraw_input,
                    outputs=withdraw_output
                )
    
    with gr.Tab("Trading"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Buy Shares")
                buy_symbol_input = gr.Textbox(label="Stock Symbol (AAPL, TSLA, GOOGL)")
                buy_quantity_input = gr.Textbox(label="Quantity")
                buy_button = gr.Button("Buy Shares")
                buy_output = gr.Textbox(label="Result")
                
                buy_button.click(
                    buy_shares,
                    inputs=[buy_symbol_input, buy_quantity_input],
                    outputs=buy_output
                )
            
            with gr.Column():
                gr.Markdown("### Sell Shares")
                sell_symbol_input = gr.Textbox(label="Stock Symbol (AAPL, TSLA, GOOGL)")
                sell_quantity_input = gr.Textbox(label="Quantity")
                sell_button = gr.Button("Sell Shares")
                sell_output = gr.Textbox(label="Result")
                
                sell_button.click(
                    sell_shares,
                    inputs=[sell_symbol_input, sell_quantity_input],
                    outputs=sell_output
                )
    
    with gr.Tab("Account Summary"):
        with gr.Row():
            with gr.Column():
                summary_button = gr.Button("Get Account Summary")
                summary_output = gr.Textbox(label="Account Summary", lines=10)
                
                summary_button.click(
                    get_account_summary,
                    inputs=[],
                    outputs=summary_output
                )
            
            with gr.Column():
                transactions_button = gr.Button("Get Transaction History")
                transactions_output = gr.Textbox(label="Transaction History", lines=10)
                
                transactions_button.click(
                    get_transaction_history,
                    inputs=[],
                    outputs=transactions_output
                )
    
    with gr.Tab("Stock Prices"):
        prices_button = gr.Button("Get Current Stock Prices")
        prices_output = gr.Textbox(label="Stock Prices")
        
        prices_button.click(
            get_current_prices,
            inputs=[],
            outputs=prices_output
        )

if __name__ == "__main__":
    demo.launch()
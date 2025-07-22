def get_share_price(symbol: str) -> float:
    """Test implementation of get_share_price function that returns fixed prices for certain stocks.
    
    Args:
        symbol: The stock symbol for which to get the price.
        
    Returns:
        The current price of the specified stock.
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 700.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)  # Default to 0 if symbol not found


class Account:
    """Class representing a user account in a trading simulation platform."""

    def __init__(self, initial_deposit: float) -> None:
        """Initializes the account with an initial deposit.

        Args:
            initial_deposit: The amount of initial deposit into the account.
            
        Raises:
            ValueError: If initial deposit is not positive.
        """
        if initial_deposit <= 0:
            raise ValueError("Initial deposit must be positive.")
        
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}  # Dictionary to track number of shares for each symbol
        self.transactions = []  # List to store all transactions
        
        # Record the initial deposit as a transaction
        self._record_transaction("DEPOSIT", None, None, initial_deposit)

    def deposit(self, amount: float) -> None:
        """Increases the account's balance by the specified amount.

        Args:
            amount: The amount to be deposited.
            
        Raises:
            ValueError: If deposit amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        self.balance += amount
        self._record_transaction("DEPOSIT", None, None, amount)

    def withdraw(self, amount: float) -> bool:
        """Decreases the account's balance by the specified amount if it does not result in a negative balance.

        Args:
            amount: The amount to be withdrawn.

        Returns:
            True if the withdrawal was successful, False otherwise.
            
        Raises:
            ValueError: If withdrawal amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        if amount > self.balance:
            return False
        
        self.balance -= amount
        self._record_transaction("WITHDRAW", None, None, amount)
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """Buys a specified quantity of shares of a given stock if there are enough funds.

        Args:
            symbol: The stock symbol.
            quantity: The number of shares to buy.

        Returns:
            True if the transaction was successful, False otherwise.
            
        Raises:
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        
        price = get_share_price(symbol)
        total_cost = price * quantity
        
        if total_cost > self.balance:
            return False
        
        self.balance -= total_cost
        
        # Update holdings
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        self._record_transaction("BUY", symbol, quantity, total_cost)
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """Sells a specified quantity of shares of a given stock if the shares are available in the account.

        Args:
            symbol: The stock symbol.
            quantity: The number of shares to sell.

        Returns:
            True if the transaction was successful, False otherwise.
            
        Raises:
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
        
        price = get_share_price(symbol)
        total_value = price * quantity
        
        self.balance += total_value
        self.holdings[symbol] -= quantity
        
        # Remove the symbol from holdings if there are no shares left
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self._record_transaction("SELL", symbol, quantity, total_value)
        return True

    def get_portfolio_value(self) -> float:
        """Calculates the total portfolio value based on the current share prices and holdings.

        Returns:
            The total value of the portfolio (cash + shares).
        """
        share_value = sum(get_share_price(symbol) * quantity for symbol, quantity in self.holdings.items())
        return self.balance + share_value

    def get_profit_or_loss(self) -> float:
        """Calculates the profit or loss compared to the initial deposit.

        Returns:
            The account's current profit or loss.
        """
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        """Returns the current holdings of the account.

        Returns:
            A dictionary with stock symbols as keys and the number of shares as values.
        """
        return self.holdings.copy()

    def get_transactions(self) -> list:
        """Lists all the transactions that have occurred in the account.

        Returns:
            A list of transactions.
        """
        return self.transactions.copy()

    def _record_transaction(self, transaction_type: str, symbol: str, quantity: int, amount: float) -> None:
        """Records a transaction in the account's transaction history.

        Args:
            transaction_type: The type of transaction (DEPOSIT, WITHDRAW, BUY, SELL).
            symbol: The stock symbol (for BUY and SELL transactions).
            quantity: The number of shares (for BUY and SELL transactions).
            amount: The amount of money involved in the transaction.
        """
        transaction = {
            "type": transaction_type,
            "symbol": symbol,
            "quantity": quantity,
            "amount": amount,
        }
        self.transactions.append(transaction)
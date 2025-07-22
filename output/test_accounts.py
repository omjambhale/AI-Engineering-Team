import unittest
from unittest.mock import patch

# Import the module to be tested
from accounts import get_share_price, Account

class TestGetSharePrice(unittest.TestCase):
    def test_known_symbols(self):
        # Test that known symbols return expected prices
        self.assertEqual(get_share_price('AAPL'), 150.0)
        self.assertEqual(get_share_price('TSLA'), 700.0)
        self.assertEqual(get_share_price('GOOGL'), 2800.0)
    
    def test_unknown_symbol(self):
        # Test that unknown symbols return 0.0
        self.assertEqual(get_share_price('UNKNOWN'), 0.0)

class TestAccount(unittest.TestCase):
    def test_init_valid_deposit(self):
        # Test account initialization with valid deposit
        account = Account(1000.0)
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.initial_deposit, 1000.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0]["type"], "DEPOSIT")
        self.assertEqual(account.transactions[0]["amount"], 1000.0)
    
    def test_init_invalid_deposit(self):
        # Test account initialization with invalid deposit
        with self.assertRaises(ValueError):
            Account(0.0)
        with self.assertRaises(ValueError):
            Account(-100.0)
    
    def test_deposit_valid_amount(self):
        # Test depositing a valid amount
        account = Account(1000.0)
        account.deposit(500.0)
        self.assertEqual(account.balance, 1500.0)
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[1]["type"], "DEPOSIT")
        self.assertEqual(account.transactions[1]["amount"], 500.0)
    
    def test_deposit_invalid_amount(self):
        # Test depositing an invalid amount
        account = Account(1000.0)
        with self.assertRaises(ValueError):
            account.deposit(0.0)
        with self.assertRaises(ValueError):
            account.deposit(-100.0)
    
    def test_withdraw_valid_amount(self):
        # Test withdrawing a valid amount
        account = Account(1000.0)
        result = account.withdraw(500.0)
        self.assertTrue(result)
        self.assertEqual(account.balance, 500.0)
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[1]["type"], "WITHDRAW")
        self.assertEqual(account.transactions[1]["amount"], 500.0)
    
    def test_withdraw_insufficient_funds(self):
        # Test withdrawing more than balance
        account = Account(1000.0)
        result = account.withdraw(1500.0)
        self.assertFalse(result)
        self.assertEqual(account.balance, 1000.0)  # Balance unchanged
        self.assertEqual(len(account.transactions), 1)  # No new transaction
    
    def test_withdraw_invalid_amount(self):
        # Test withdrawing an invalid amount
        account = Account(1000.0)
        with self.assertRaises(ValueError):
            account.withdraw(0.0)
        with self.assertRaises(ValueError):
            account.withdraw(-100.0)

    def test_buy_shares_sufficient_funds(self):
        # Test buying shares with sufficient funds
        account = Account(10000.0)
        result = account.buy_shares("AAPL", 10)
        self.assertTrue(result)
        self.assertEqual(account.balance, 8500.0)  # 10000 - (150 * 10)
        self.assertEqual(account.holdings, {"AAPL": 10})
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[1]["type"], "BUY")
        self.assertEqual(account.transactions[1]["symbol"], "AAPL")
        self.assertEqual(account.transactions[1]["quantity"], 10)
        self.assertEqual(account.transactions[1]["amount"], 1500.0)
    
    def test_buy_shares_insufficient_funds(self):
        # Test buying shares with insufficient funds
        account = Account(1000.0)
        result = account.buy_shares("TSLA", 2)  # Costs 1400, only have 1000
        self.assertFalse(result)
        self.assertEqual(account.balance, 1000.0)  # Balance unchanged
        self.assertEqual(account.holdings, {})  # No shares bought
        self.assertEqual(len(account.transactions), 1)  # No new transaction
    
    def test_buy_shares_invalid_quantity(self):
        # Test buying an invalid quantity of shares
        account = Account(1000.0)
        with self.assertRaises(ValueError):
            account.buy_shares("AAPL", 0)
        with self.assertRaises(ValueError):
            account.buy_shares("AAPL", -5)
    
    def test_buy_shares_unknown_symbol(self):
        # Test buying shares of an unknown symbol
        account = Account(1000.0)
        result = account.buy_shares("UNKNOWN", 10)  # Price will be 0.0
        self.assertTrue(result)  # Should succeed because cost is 0
        self.assertEqual(account.balance, 1000.0)  # No cost
        self.assertEqual(account.holdings, {"UNKNOWN": 10})
    
    def test_sell_shares_available(self):
        # Test selling shares that are available
        account = Account(1000.0)
        account.buy_shares("AAPL", 10)
        initial_balance = account.balance
        result = account.sell_shares("AAPL", 5)
        self.assertTrue(result)
        self.assertEqual(account.balance, initial_balance + 750.0)  # 5 * 150
        self.assertEqual(account.holdings, {"AAPL": 5})
        self.assertEqual(account.transactions[-1]["type"], "SELL")
        self.assertEqual(account.transactions[-1]["symbol"], "AAPL")
        self.assertEqual(account.transactions[-1]["quantity"], 5)
        self.assertEqual(account.transactions[-1]["amount"], 750.0)
    
    def test_sell_shares_not_available(self):
        # Test selling shares that are not available
        account = Account(1000.0)
        # Try to sell without having any shares
        result = account.sell_shares("AAPL", 5)
        self.assertFalse(result)
        # Buy some shares but try to sell more than owned
        account.buy_shares("AAPL", 3)
        result = account.sell_shares("AAPL", 5)
        self.assertFalse(result)
        self.assertEqual(account.holdings, {"AAPL": 3})  # Shares unchanged
    
    def test_sell_shares_invalid_quantity(self):
        # Test selling an invalid quantity of shares
        account = Account(1000.0)
        account.buy_shares("AAPL", 10)
        with self.assertRaises(ValueError):
            account.sell_shares("AAPL", 0)
        with self.assertRaises(ValueError):
            account.sell_shares("AAPL", -5)
    
    def test_sell_all_shares(self):
        # Test selling all shares of a symbol
        account = Account(1000.0)
        account.buy_shares("AAPL", 5)
        account.sell_shares("AAPL", 5)
        self.assertEqual(account.holdings, {})  # Symbol should be removed
    
    def test_get_portfolio_value(self):
        # Test calculating portfolio value
        account = Account(1000.0)
        account.buy_shares("AAPL", 10)  # 1500
        account.buy_shares("TSLA", 2)   # 1400
        # Expected: cash balance + share values
        expected_value = account.balance + (10 * 150.0) + (2 * 700.0)
        self.assertEqual(account.get_portfolio_value(), expected_value)
    
    def test_get_profit_or_loss(self):
        # Test calculating profit/loss
        account = Account(5000.0)
        account.buy_shares("AAPL", 10)  # 1500
        account.buy_shares("TSLA", 2)   # 1400
        # No profit/loss yet since we're just converting cash to shares
        self.assertEqual(account.get_profit_or_loss(), 0.0)
        
        # Simulate price changes by mocking get_share_price
        with patch("accounts.get_share_price") as mock_price:
            # Higher prices should show profit
            mock_price.side_effect = lambda symbol: 200.0 if symbol == "AAPL" else 800.0
            profit = (10 * 200.0) + (2 * 800.0) + account.balance - 5000.0
            self.assertEqual(account.get_profit_or_loss(), profit)
            
            # Lower prices should show loss
            mock_price.side_effect = lambda symbol: 100.0 if symbol == "AAPL" else 600.0
            loss = (10 * 100.0) + (2 * 600.0) + account.balance - 5000.0
            self.assertEqual(account.get_profit_or_loss(), loss)
    
    def test_get_holdings(self):
        # Test getting holdings
        account = Account(1000.0)
        account.buy_shares("AAPL", 10)
        account.buy_shares("TSLA", 2)
        
        holdings = account.get_holdings()
        self.assertEqual(holdings, {"AAPL": 10, "TSLA": 2})
        
        # Verify we get a copy, not the original
        holdings["AAPL"] = 100
        self.assertEqual(account.holdings["AAPL"], 10)  # Original unchanged
    
    def test_get_transactions(self):
        # Test getting transactions
        account = Account(1000.0)
        account.deposit(500.0)
        account.withdraw(200.0)
        account.buy_shares("AAPL", 5)
        account.sell_shares("AAPL", 2)
        
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 5)  # Initial deposit + 4 transactions
        
        # Verify we get a copy, not the original
        transactions.pop()
        self.assertEqual(len(account.transactions), 5)  # Original unchanged

if __name__ == "__main__":
    unittest.main()
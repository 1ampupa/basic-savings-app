from modules.account import Account

account1 : Account = Account.create_account("Finn", 100)

print(Account.accounts)

print(account1)
print(repr(account1))

account1.withdraw(150)
account1.withdraw(50)
account1.deposit(200)

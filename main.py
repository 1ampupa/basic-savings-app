from modules.account import Account

Account.load_accounts()

for account in Account.accounts:
    print(account.name)

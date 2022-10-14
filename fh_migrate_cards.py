import stripe

def migrate_accounts(): 
	us_accounts = get_accounts_from_us_platform()
	copy_accounts_to_eu_platform(us_accounts)
	update_pii_provided_by_stripe()


def get_accounts_from_us_platform():
	stripe.api_key = "sk_test_3fWdu6xut3jXSZr89IrvL3Fu00AcTbQmu5"
	accounts = []
	for account in stripe.Account.list().auto_paging_iter():
		accounts.append(account)
	print(len(accounts))
	return accounts


def copy_accounts_to_eu_platform(accounts):
	stripe.api_key = ""
	for account in accounts: 
		stripe.Account.create(account)

def update_pii_provided_by_stripe(): 
	print("update_pii_provided_by_stripe")

migrate_accounts()
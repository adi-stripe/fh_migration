from multiprocessing.spawn import old_main_modules
import stripe
import csv
from pathlib import Path
from datetime import datetime

def migrate_account():
    old_new_mapping = {}
    old_new_persons_mapping ={}
    #source account
    set_stripe_key("sk_test_51JUA4SJEPmh1uB4OCbpK6bhu4GHiQanPsAm69EBSaHYD5Ra9KQfKit3fJAEVYh3zwBLv0m73yw6ADlyqQKGI0axS00xYIhcij8")
   
    connected_accounts = get_accounts()

    for connected_account in connected_accounts:
        set_stripe_key("sk_test_51JUA4SJEPmh1uB4OCbpK6bhu4GHiQanPsAm69EBSaHYD5Ra9KQfKit3fJAEVYh3zwBLv0m73yw6ADlyqQKGI0axS00xYIhcij8")

        old_persons = get_persons_on_account(connected_account)
        old_account = get_account(connected_account)
        #destination account
        set_stripe_key("sk_test_51LjSreHtLIXarnzfqvbJOyXv1pHgmRILM66UhbvImNjVwzehLqKUQAkV6ueydboFBAx19Py9pDHoj7R67bFaV7nh00TOBryOti")
        new_account = create_account(old_account)
        if (old_account.business_type!='individual'):
            old_new_persons_mapping =old_new_persons_mapping | migrate_persons(old_persons, new_account, old_account)
        else: 
            old_new_persons_mapping[old_account.individual.id] = new_account.individual.id 
        old_new_mapping[old_account.id] = new_account.id
        # old_new_mapping = {
        #     'acct_1LfhTyR2SmBycCuk':'acct_1LgukEQwDQcgY7JK'
        # }
    set_stripe_key("sk_test_51LjSreHtLIXarnzfqvbJOyXv1pHgmRILM66UhbvImNjVwzehLqKUQAkV6ueydboFBAx19Py9pDHoj7R67bFaV7nh00TOBryOti")
    
    migrate_bank_account(old_new_mapping=old_new_mapping)
    # migrate_account_data(old_account, new_account)
    update_account_with_data_from_stripe(old_new_mapping=old_new_mapping,old_new_persons_mapping=old_new_persons_mapping)

def set_stripe_key(key):
	stripe.api_key = key

def get_accounts():
    accounts=[]
    for account in stripe.Account.list(limit=3).auto_paging_iter():
        if account.payouts_enabled and account.type=='custom':
            accounts.append(account.id)
    return accounts


def get_account(account_id):
	return stripe.Account.retrieve(account_id)
	

def get_persons_on_account(account_id):
	return stripe.Account.list_persons(
  		account_id,
  		limit=100,
	)


def create_account(account_data):

    individual=None
    company=None
    if (account_data.business_type=='individual'):
        individual={
            "address": {
                "city":account_data.individual.address.city,
                "country": account_data.individual.address.country,
                "line1":account_data.individual.address.line1,
                "line2": account_data.individual.address.line2,
                "postal_code": account_data.individual.address.postal_code,
                "state":account_data.individual.address.state
            },
            "dob":{
                "day":account_data.individual.dob.day,
                "month":account_data.individual.dob.month,
                "year":account_data.individual.dob.year
            },
            "email":account_data.individual.email,
            "first_name":account_data.individual.first_name,
            "last_name":account_data.individual.last_name,
            "metadata": account_data.individual.metadata,
            "phone":account_data.individual.phone,
        }

        if 'address_kana' in account_data.individual.keys():
            individual.address_kana= {
                "city":account_data.individual.address_kana.city,
                "country": account_data.individual.address_kana.country,
                "line1":account_data.individual.address_kana.line1,
                "line2": account_data.individual.address_kana.line2,
                "postal_code": account_data.individual.address_kana.postal_code,
                "state":account_data.individual.address_kana.state,
                "town":account_data.individual.address_kana.town
            },
        if 'address_kanji' in account_data.individual.keys():
            individual.address_kanji={
                "city":account_data.individual.address_kanji.city,
                "country": account_data.individual.address_kanji.country,
                "line1":account_data.individual.address_kanji.line1,
                "line2": account_data.individual.address_kanji.line2,
                "postal_code": account_data.individual.address_kanji.postal_code,
                "state":account_data.individual.address_kanji.state,
                "town":account_data.individual.address_kanji.town
            },
        if 'first_name_kana' in account_data.individual.keys():
            individual.first_name_kana=account_data.individual.first_name_kana
            individual.last_name_kana=account_data.individual.last_name_kana
        if 'first_name_kanji' in account_data.individual.keys():
            individual.first_name_kanji=account_data.individual.first_name_kanji
            individual.last_name_kanji=account_data.individual.last_name_kanji
        if 'maiden_name' in account_data.individual.keys():
            individual.maiden_name=account_data.individual.maiden_name
        if 'political_exposure' in account_data.individual.keys():
            individual.political_exposure=account_data.individual.political_exposure
        if 'full_name_aliases' in account_data.individual.keys():
            individual.full_name_aliases=account_data.individual.full_name_aliases
        if 'gender' in account_data.individual.keys():
            individual.gender=account_data.individual.gender
        if 'registered_address' in account_data.individual.keys():
            individual.registered_address = {
                "city":account_data.individual.registered_address.city,
                "country": account_data.individual.registered_address.country,
                "line1":account_data.individual.registered_address.line1,
                "line2": account_data.individual.registered_address.line2,
                "postal_code": account_data.individual.registered_address.postal_code,
                "state":account_data.individual.registered_address.state
            }
        if 'ssn_last4' in account_data.individual.keys():
            individual.ssn_last_4 = account_data.individual.ssn_last4
    else:
        company={
            "address": {
                "city":account_data.company.address.city,
                "country": account_data.company.address.country,
                "line1":account_data.company.address.line1,
                "line2": account_data.company.address.line2,
                "postal_code": account_data.company.address.postal_code,
                "state":account_data.company.address.state
            },
            "directors_provided": account_data.company.directors_provided,
            "executives_provided": account_data.company.executives_provided,
            "name":account_data.company.name,
            "owners_provided":account_data.company.owners_provided,
            # "ownership_declaration":{
            #     "date":datetime.now(),
            #     "ip":'127.0.0.1',
            #     "user_agent":None
            # },
            "phone":account_data.company.phone,
            # "registration_number":account_data.company.registration_number,
        }
        if 'address_kana' in account_data.company.keys():
            company.address_kana= {
                "city":account_data.company.address_kana.city,
                "country": account_data.company.address_kana.country,
                "line1":account_data.company.address_kana.line1,
                "line2": account_data.company.address_kana.line2,
                "postal_code": account_data.company.address_kana.postal_code,
                "state":account_data.company.address_kana.state,
                "town":account_data.company.address_kana.town
            }
        if 'address_kanji' in account_data.company.keys():
            company.address_kanji={
                "city":account_data.company.address_kanji.city,
                "country": account_data.company.address_kanji.country,
                "line1":account_data.company.address_kanji.line1,
                "line2": account_data.company.address_kanji.line2,
                "postal_code": account_data.company.address_kanji.postal_code,
                "state":account_data.company.address_kanji.state,
                "town":account_data.company.address_kanji.town
            }
        if 'name_kana' in account_data.company.keys():
            company.name_kana=account_data.company.name_kana
        if 'name_kanji' in account_data.company.keys():
            company.name_kanji=account_data.company.name_kanji
        if 'structure' in account_data.company.keys():
            company.structure=account_data.company.structure
        # if 'tax_id' in account_data.company.keys():
        #     company.tax_id=account_data.company.tax_id
        # if 'tax_id_registrar' in account_data.company.keys():
        #     company.tax_id_registrar=account_data.company.tax_id_registrar
        # if 'vat_id' in account_data.company.keys():
        #     company.vat_id=account_data.company.vat_id    

    acc_support_address=None
    if account_data.business_profile.support_address:
        acc_support_address={
                "city": account_data.business_profile.support_address.city,
                "country": account_data.business_profile.support_address.country,
                "line1":account_data.business_profile.support_address.line1,
                "line2":account_data.business_profile.support_address.line2,
                "postal_code": account_data.business_profile.support_address.postal_code,
                "state": account_data.business_profile.support_address.state
            }
    

    return stripe.Account.create(
  		type="custom",
  		capabilities={
   			"card_payments": {"requested": True},
    		"transfers": {"requested": True},
  		},
        country=account_data.country,
        email=account_data.email,
        business_type=account_data.business_type,
        metadata=account_data.metadata,
        business_profile={
            "mcc": account_data.business_profile.mcc,
            "name": account_data.business_profile.name,
            "product_description":account_data.business_profile.product_description,
            "support_address":acc_support_address,
            "support_email": account_data.business_profile.support_email,
            "support_phone": account_data.business_profile.support_phone,
            "support_url": account_data.business_profile.support_url,
            "url":account_data.business_profile.url
        }, 
        default_currency=account_data.default_currency,
        tos_acceptance = {
            'date': account_data.tos_acceptance.date,
            'ip':account_data.tos_acceptance.ip,
            'user_agent': account_data.tos_acceptance.user_agent
        },
        individual=individual,
        company=company
        
    )

def migrate_persons(old_persons, new_account, old_account):
    old_new_person_map={}
    for person in old_persons:
        new_person = create_new_person(person, new_account.id, old_account)
        old_new_person_map[person.id]=new_person.id
    return old_new_person_map


def migrate_account_data():
	print("migrate_account_data")

def update_account_with_data_from_stripe(old_new_mapping, old_new_persons_mapping):
    with open(Path(__file__).absolute().parent / 'pii_test_file.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(row[0])
                stripe.Account.modify(old_new_mapping[row[0]],
                    company={
                        'tax_id':row[5]  
                    }
                    )
                stripe.Account.modify_person(
                    old_new_mapping[row[0]],
                    old_new_persons_mapping[row[13]],
                    id_number=row[17]
                )
                line_count += 1
        print(f'Processed {line_count} lines.')
    print("id_number on person")
    print("ssn_last_4 on person")

def create_new_person(person_data, account_id, old_account):
    maiden_name=None
    nationality=None
    gender=None
    full_name_aliases=None
    if 'maiden_name' in person_data.keys():
        maiden_name=person_data.maiden_name
    if 'nationality' in person_data.keys():
        nationality=person_data.nationality
    if 'gender' in person_data.keys():
        gender=person_data.gender
    if 'full_name_aliases' in person_data.keys():
        full_name_aliases=person_data.full_name_aliases
    if 'ownership_declaration' in old_account.company.keys():
        stripe.Account.modify(account_id,
            company={
                "ownership_declaration":{
                    "date":old_account.company.ownership_declaration.date,
                    "ip":old_account.company.ownership_declaration.ip,
                    "user_agent":old_account.company.ownership_declaration.user_agent
                }
            }            
        )
    return stripe.Account.create_person(
  		account_id,
  		address={
    		"city":person_data.address.city,
    		"country":person_data.address.country,
    		"line1":person_data.address.line1,
    		"line2":person_data.address.line2,
    		"postal_code":person_data.address.postal_code,
    		"state":person_data.address.state
  		},
  		dob={
    		"day":person_data.dob.day,
    		"month":person_data.dob.month,
    		"year":person_data.dob.year
  		},
  		email=person_data.email,
  		first_name=person_data.first_name,
  		last_name=person_data.last_name,
        maiden_name=maiden_name,
  		metadata=person_data.metadata,
  		phone=person_data.phone,
  		relationship={
    		"director":person_data.relationship.director,
    		"executive":person_data.relationship.executive,
    		"owner":person_data.relationship.owner,
    		"percent_ownership":person_data.relationship.percent_ownership,
    		"representative":person_data.relationship.representative,
    		"title":person_data.relationship.title
  		},
        nationality=nationality,
        gender=gender,
        full_name_aliases=full_name_aliases
    )

def migrate_bank_account(old_new_mapping):
    with open(Path(__file__).absolute().parent / 'minhthule_test_ba.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                existing_account = stripe.Account.retrieve(row[0])
                existing_ba = stripe.Account.retrieve_external_account(row[0],row[1])
                if existing_account.payouts_enabled and existing_ba.default_for_currency:
                    stripe.Account.modify(old_new_mapping[row[0]],
                    external_account={
                        'object': 'bank_account',
                        'country': row[3],
                        'account_number': row[2],
                        'currency': row[4],
                        'account_holder_name': row[5],
                        'account_holder_type': row[6],
                        'routing_number':row[7]
                    })
                line_count += 1
        print(f'Processed {line_count} lines.')
	
def main():
    a = migrate_account()
    # get_account()
    print("done")

if __name__ == "__main__":
    main()
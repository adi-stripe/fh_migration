with ca as (
  select
    pc.connected_merchant as merchant
  from
    mongo.platformconnections_default_locale pc
  where
    pc.merchant = 'acct_1JUA4SJEPmh1uB4O'
)
select
  ca.merchant,
--   mongo.merchants_default_locale.business_name,
  mongo.bankaccounts_default_locale._id as bank_account_id,
--   account_number_token,
  account_number,
  mongo.bankaccounts_default_locale.country as ba_country,
  mongo.bankaccounts_default_locale.currency as ba_currency,
  mongo.bankaccounts_default_locale.account_holder_name as ba_account_holder_name,
  mongo.bankaccounts_default_locale.account_holder_type as ba_account_holder_type,
  mongo.bankaccounts_default_locale.routing_number as ba_routing_number
from
  ca,
  mongo.bankaccounts_default_locale,
  mongo.merchants_default_locale,
  detok.ban_mappings
where
  ca.merchant = mongo.bankaccounts_default_locale.merchant
  and belongs_to_merchant = True
  and payouts_enabled = True
  and ca.merchant = mongo.merchants_default_locale._id
--   and livemode=True
  and account_number_token=token    
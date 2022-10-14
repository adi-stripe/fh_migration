| General field          | Individual          | Company               | Mapped   | PII | Note       | File |
| ---------------------- | ------------------- | --------------------- | -------- | --- | ---------- | ---- |
| type                   |                     |                       | x        |     |            |      |
| country                |                     |                       | x        |     |            |      |
| email                  |                     |                       | x        |     |            |      |
| capabilities           |                     |                       | x        |     |            |      |
| business_type          |                     |                       | x        |     |            |      |
| company                |                     | company.address       | x        |     |            |      |
|                        |                     | address_kana          | x        |     | if exists  |      |
|                        |                     | address_kanji         | x        |     | if exists  |      |
|                        |                     | directors_provided    | x        |     |            |      |
|                        |                     | executives_provided   | x        |     |            |      |
|                        |                     | name                  | x        |     |            |      |
|                        |                     | name_kanji            | x        |     | if exists  |      |
|                        |                     | name_kana             | x        |     | if exists  |      |
|                        |                     | owners_provided       | x        |     |            |      |
|                        |                     | ownership_declaration | x        |     |            |      |
|                        |                     | phone                 | x        |     |            |      |
|                        |                     | registration_number   | -missing | x   |            |      |
|                        |                     | structure             | x        |     |            |      |
|                        |                     | tax_id                | to_test  | x   |            |      |
|                        |                     | tax_id_registrar      |          | x   |            |      |
|                        |                     | vat_id                |          | x   |            |      |
|                        |                     | verification          |          |     |            | x    |
| individual             | address             |                       | x        |     |            |      |
|                        | address_kana        |                       | x        |     | if exists  |      |
|                        | address_kanji       |                       | x        |     | if exists  |      |
|                        | dob                 |                       | x        |     |            |      |
|                        | email               |                       | x        |     |            |      |
|                        | first_name          |                       | x        |     |            |      |
|                        | first_name_kana     |                       | x        |     | if exists  |      |
|                        | first_name_kanji    |                       | x        |     | if exists  |      |
|                        | full_name_aliases   |                       | x        |     | if exists  |      |
|                        | gender              |                       | x        |     |            |      |
|                        | id_number           |                       |          | x   |            |      |
|                        | id_number_secondary |                       |          | x   |            |      |
|                        | last_name           |                       | x        |     |            |      |
|                        | last_name_kanji     |                       | x        |     | if exists  |      |
|                        | last_name_kana      |                       | x        |     | if exists  |      |
|                        | maiden_name         |                       | x        |     |            |      |
|                        | metadata            |                       | x        |     |            |      |
|                        | phone               |                       | x        |     |            |      |
|                        | political_exposure  |                       | x        |     | not tested |      |
|                        | registered_address  |                       | x        |     |            |      |
|                        | ssn_last4           |                       |          | x   |            |      |
|                        | verification        |                       |          |     |            | x    |
| metadata               |                     |                       | x        |     |            |      |
| tos_acceptance         |                     |                       |          |     |            |      |
| account_token          |                     |                       | not_map  |     |            |      |
| business_profile       |                     |                       |          |     |            |      |
| bp.mcc                 |                     |                       | x        |     |            |      |
| bp.name                |                     |                       | x        |     |            |      |
| bp.product_description |                     |                       | x        |     |            |      |
| bp.support_address     |                     |                       | x        |     | if exists  |      |
| bp.support_email       |                     |                       | x        |     | if exists  |      |
| bp.support_phone       |                     |                       | x        |     | if exists  |      |
| bp.support_url         |                     |                       | x        |     | if exists  |      |
| bp.url                 |                     |                       | x        |     |            |      |
| default_currency       |                     |                       | x        |     |            |      |
| documents              |                     |                       |          |     |            | x    |
| external_account       |                     |                       | to_test  | x   |            |      |
| settings               |                     |                       |          |     |            |      |

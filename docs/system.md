## globals

init()

usr_type

usr_id

## utils

class Error(Exception)

class EmptyError(Error)

class LenghtError(Error)

class InvalidCharacterError(Error)

class EmailFormatError(Error)

class DateFormatError(Error)



logged()

logout()

display(dict)

validate(user_input)

validate_email(user_input)

validate_password(user_input)

validate_date(user_input)

login(user_email, password, usr_type)

register(first_name, last_name, gender, birth_date, email, pw, type)

user_type(user_id)

select()

help()

update()

export()

sqlhelper()

day_empty_df(date, gp_id)

week_empty_df(start_date, gp_id)

db_execute(query)

db_read_query(query)


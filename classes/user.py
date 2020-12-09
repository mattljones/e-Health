# user.py


class User:
    '''
    Parent class to Patient and GP subclasses.
    Contains attributes in common to both.
    '''

    def __init__(self, id_, first_name, last_name, gender, birth_date, email, password, registration_date):
        self.id = id_
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = birth_date
        self.email = email
        self.password = password
        self.registration_date = registration_date


### DEVELOPMENT ###

if __name__ == "__main__":
    pass
# appointment.py

# import libraries
# import pandas as pd
import sqlite3


# def db_exec_push(query):
#     import sqlite3
#     conn = sqlite3.connect('config/db_comp0066.db')
#     c = conn.cursor()
#
#     c.execute(query)
#
#     # Commit to db
#     conn.commit()
#     print("Info successfully committed")
#     # Close db
#     conn.close()


class Appointment:
    """
    Class defining all 'appointment' related methods.
    """
    # Book a new appointment with GP as a patient
    def book(self, availability_start_time, availability_agenda, availability_type,gp_id, patient_id):
        self.availability_start_time = availability_start_time
        self.availability_agenda = availability_agenda
        self.availability_type = availability_type
        self.gp_id = gp_id
        self.patient_id = patient_id

        query = """INSERT INTO availability
        (availability_id, availability_start_time, availability_status,availability_status_change_time,
        availability_agenda, availability_type,gp_id,patient_id)
        VALUES ({},'{}','{}','{}','{}','{}',{},{});""".format('NULL', self.availability_start_time,
                                                              'booked', '2020-12-12 10:40:20.000',
                                                              self.availability_agenda,
                                                              self.availability_type, self.gp_id,
                                                              self.patient_id)
        conn = sqlite3.connect('database/db_comp0066.db')
        c = conn.cursor()

        c.execute(query)

        # Commit to db
        conn.commit()
        print("Info successfully committed")
        # Close db
        conn.close()

        # db_exec_push(query)

    # Update an appointment with GP
    def update(self):
        pass

    # Display GPs schedule for a specific date
    def select_gp_upcoming_day(self):
        pass

    #  Display GPs schedule for a specific week
    def select_gp_upcoming_week(self):
        pass

    # Display GP schedule for custom input
    def select_gp_upcoming_custom(self):
        pass

    # TODO Ask Matt what's the purpose of this function
    # Select
    def select_patient_previous_day(self):
        pass

    # TODO Ask Matt what's the purpose of this function
    # Select
    def select_patient_previous_week(self):
        pass

    # TODO Ask Matt what's the purpose of this function
    # Select
    def select_patient_previous_custom(self):
        pass

    # Select the appoint for an upcoming patient
    def select_patient_upcoming(self):
        pass

    # Select the availability of a specific GP for a specific date
    def select_availability_day(self):
        pass

    # Select the availability of a specific GP for a particular week
    def select_availability_week(self):
        pass

    # Select custom availability of a specific GP
    def select_availability_custom(self):
        pass

    # Gets availabilities of a all GPs for specific date except for specified GP
    def select_other_availability_day(self):
        pass

    # Gets availabilities of a all GPs for specific week except for specified GP
    def select_other_availability_week(self):
        pass

    # Gets availabilities of a all GPs for specific interval of time except for specified GP
    def select_other_availability_custom(self):
        pass

    # TODO what is the point of these again, sorry can't wrap my head around it
    #
    def check_availability_day(self):
        pass

    #
    def check_availability_week(self):
        pass

    #
    def check_availability_custom(self):
        pass

    #
    def check_other_availability_day(self):
        pass

    #
    def check_other_availability_week(self):
        pass

    #
    def check_other_availability_custom(self):
        pass

    # Cancel a specific appointment
    def cancel_appointment(self):
        pass


### DEVELOPMENT ###

if __name__ == "__main__":
     Appointment().book('2020-12-08 08:00:00', 'availability agenda test', 'online',2, 3)

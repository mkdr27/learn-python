import mysql.connector

from datetime import datetime, timedelta

class Patient:
    def __init__(self, patientid, name, doctorid, slotid):
        self.patientid = patientid
        self.name = name
        self.doctorid = doctorid
        self.slotid = slotid
    
    def add_patient_appointment(self):
        insert_patient_query = """INSERT INTO appointment.patients (id, name, doctor_id, slot_id) VALUES (%s, %s, %s, %s)"""
        values = (self.patientid, self.name, self.doctorid, self.slotid)
        cursor.execute(insert_patient_query, values)
        connection.commit()
        print("Patient record updated successfully.")


class Doctor:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def add_doctor(self):
        get_doctor_query = "SELECT name FROM appointment.doctors;"
        cursor.execute(get_doctor_query)
        all_doctors = cursor.fetchall()
        print(self.name,all_doctors)
        if self.name in str(all_doctors):
            print(f"Doctor {self.name} already exists")
        else:
            insert_doctor_query = "INSERT INTO doctors (id, name) VALUES (%s, %s);"
            values = (self.id,self.name)
            cursor.execute(insert_doctor_query, values)
            connection.commit()
            print("Doctors database updated successfully.")

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='appointment',
                                         user='root',
                                         password='qwer')
    
    create_doctors_table_query = """CREATE TABLE IF NOT EXISTS doctors (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(255)
                                )"""
    
    create_slots_table_query = """CREATE TABLE IF NOT EXISTS slots (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    time_slot TIME
                                )"""

    create_patients_table_query = """CREATE TABLE IF NOT EXISTS patients (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(255),
                                    doctor_id INT,
                                    slot_id INT,
                                    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
                                    FOREIGN KEY (slot_id) REFERENCES slots(id))"""
    
    cursor = connection.cursor()

    create_doctors_table = cursor.execute(create_doctors_table_query)
    create_slots_table = cursor.execute(create_slots_table_query)
    create_patients_table = cursor.execute(create_patients_table_query)
    

    print("Doctor, patient and timeslots Table created successfully ")

except mysql.connector.Error as error:
    print("Failed to create table in MySQL: {}".format(error))

def define_slot_table():
    slots = []
    for hour in range(8, 16):  
        for minutes in range(0, 60, 30): 
            slots.append(f"{hour:02d}:{minutes:02d}")
    insert_slot_query = "INSERT INTO slots (time_slot) VALUES (%s)"
    for slot in slots:
        cursor.execute(insert_slot_query, (slot,))
    connection.commit()

def display_doctor():
        get_doctor_query = "SELECT name FROM appointment.doctors;"
        cursor.execute(get_doctor_query)
        all_doctors = cursor.fetchall()
        return all_doctors

def display_doctor_id(doctorname):
        get_doctorid_query = """SELECT id FROM appointment.doctors where doctors.name = %s"""
        cursor.execute(get_doctorid_query, (doctorname,))
        doctor_id = cursor.fetchall()
        return doctor_id[0][0]

def get_available_slots(doctor_name):
    query = """SELECT s.time_slot,s.id 
               FROM doctors d 
               JOIN slots s ON NOT EXISTS (SELECT 1 FROM patients p WHERE p.doctor_id = d.id AND p.slot_id = s.id)
               WHERE d.name = %s"""
    cursor.execute(query, (doctor_name,))
    # print(query)
    available_slots = cursor.fetchall()
    # print(available_slots)
    return available_slots

def format_timedelta(timedelta_obj):
    # Get total seconds
    total_seconds = timedelta_obj.total_seconds()
    # Calculate hours and minutes
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    # Create datetime object with current date and time from timedelta
    dt = datetime.combine(datetime.now().date(), datetime.min.time()) + timedelta(seconds=total_seconds)
    # Format datetime as string
    return dt.strftime("%H:%M")

def check_doctor_availabilty(doctor_name):
    available_slots = get_available_slots(doctor_name)
    d={}
    if available_slots:
        print(f"Available time slots for Dr. {doctor_name}:")
        print('Available slotID'+' - '+'Time')
        for slot in available_slots:
            time_slot,time_id = slot[0],slot[1]  
            d[time_id]=format_timedelta(time_slot)
            print(time_id,'-',format_timedelta(time_slot))
    else:
        print(f"No available time slots for Dr. {doctor_name}")
    return d
    # print(d)

def generate_patient_id():
    get_patientid_query = "SELECT id FROM appointment.patients;"
    cursor.execute(get_patientid_query)
    all_patient_id = cursor.fetchall()
    patient_id_list=list()
    for id in all_patient_id:
        patient_id=id[0]
        patient_id_list.append(patient_id)
    new_patient_id = max(patient_id_list)+1
    return new_patient_id

# doctor3 = Doctor('physician_doctor',3)
# doctor4 = Doctor('ent_doctor',4)
# doctor5 = Doctor('ortho_doctor',5)
# doctor5.add_doctor()

list_display_doctor=display_doctor()

def book_appointment():
    get_patient_name = input("Please enter patient Name: ")
    print("Below are the list of doctors in this speciality")
    for i in range(len(list_display_doctor)):
        print(str(list_display_doctor[i][0]))
    get_doctor_name = input("Please enter the doctor name to book: ")
    if get_doctor_name in str(list_display_doctor):
        print("Checking doctor availability!")
        available_slots = check_doctor_availabilty(get_doctor_name)
        # print(available_slots[10])
        available_slots_list = list(available_slots.keys())
        get_slot_id = int(input("Enter the slot id you want to book: "))
        while get_slot_id not in available_slots_list:
            print("Below are the list of available slots",available_slots)
            get_slot_id = int(input("Kindly re-enter the correct slot id you want to book: "))
        else:
            get_slot_time=available_slots[get_slot_id]
            get_patient_id=generate_patient_id()
            get_doctor_id = display_doctor_id(get_doctor_name)
            create_patient=Patient(get_patient_id,get_patient_name,get_doctor_id,get_slot_id)
            create_patient.add_patient_appointment()
        print(f"Booked {get_doctor_name} for {get_patient_name} on {get_slot_time}")
    else:
        print(f"Entered doctor {get_doctor_name} is not in this speciality")

book_appointment()

cursor.close()
connection.close()

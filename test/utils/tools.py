def printPatients(patients):
    for patient in patients:
        printPatient(patient)


def printPatient(patient):
    print(patient.get('extension'))
    print(' server id: {0}\n meta: {1}\n Name: {2} {3}\n Gender: {4}\n tel: {5}\n Identifier: {6}\n'.format(
        patient.get('id'),
        patient.get('meta'),
        patient.get_by_path('name.0.family'),
        patient.get_by_path('name.0.given.0'),
        patient.get('gender'),
        patient.get_by_path('telecom.0.value'),
        patient.get('identifier'),
    ))
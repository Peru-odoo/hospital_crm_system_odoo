{
    "name": "Hospital Service",
    "description":"""Applications for hospital services for clients who value comfort and quality""",
    "version": "1.0",
    "author": "Kostiantyn Kononenko",
    "category": "Human Resources",
    "depends": [],
    "data": [
        "security/ir.model.access.csv",
        "views/hospital_service_view.xml",
        "views/hospital_contact_person_view.xml",
        "views/hospital_doctor_view.xml",
        "views/hospital_patient_view.xml",
        "views/hospital_directory_diseases_view.xml",
        "views/hospital_research_type_view.xml",
        "views/hospital_sample_type_view.xml",
        "views/hospital_doctor_schedule_view.xml",
        "views/hospital_doctor_visit_view.xml",
        "views/hospital_research_view.xml",
        "views/menu_items.xml",
    ],
    "installable": True,
    "application": True,
    'license': 'LGPL-3',
}

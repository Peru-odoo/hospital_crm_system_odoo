from odoo import api, fields, models


class DoctorVisit(models.Model):
    _name = 'hospital.doctor_visit'
    _description = 'Doctor Visit'

    time_slot = fields.Many2one(
        'hospital.schedule.line',
        string='Available Time',
        domain="[('schedule_id.appointment_date', '=', appointment_date)]",
        help='Select Time Slot',
    )
    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Date(string='Appointment Date', required=True)
    research_ids = fields.Many2many('hospital.research', string='Research', copy=False)
    diagnosis_id = fields.Many2many('hospital.diagnosis', string='Diagnosis')
    recommendations = fields.Text(string='Recommendations')
    is_completed = fields.Boolean(string='Visit Completed', default=False)

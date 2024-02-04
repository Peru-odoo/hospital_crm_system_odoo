from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class DoctorVisit(models.Model):
    _name = 'hospital.doctor_visit'
    _description = 'Doctor Visit'

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment = fields.Many2one('hospital.doctor_schedule', string='Doctor Appointment', required=True)
    recommendations = fields.Text(string='Recommendations')
    is_completed = fields.Boolean(string='Visit Completed', default=False)

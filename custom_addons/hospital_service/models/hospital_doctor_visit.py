from odoo import models, fields, api


class DoctorVisit(models.Model):
    _name = 'hospital.doctor_visit'
    _description = 'Doctor Visit'

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Many2one('hospital.doctor_schedule', string='Doctor Appointment Date', required=True)
    research_ids = fields.Many2many('hospital.research', string='Research', copy=False)
    diagnosis_id = fields.Many2one('hospital.diagnosis', string='Diagnosis')
    recommendations = fields.Text(string='Recommendations')
    is_completed = fields.Boolean(string='Visit Completed', default=False)


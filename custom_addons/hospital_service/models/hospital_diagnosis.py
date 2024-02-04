from odoo import models, fields, api


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Diagnosis'

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    disease = fields.Many2one('hospital.disease', string='Disease', required=True)
    treatment = fields.Text(string='Treatment')
    diagnosis_date = fields.Date(string='Diagnosis Date', default=fields.Date.today())
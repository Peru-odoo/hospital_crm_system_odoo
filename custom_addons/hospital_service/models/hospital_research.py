from odoo import models, fields, api


class Research(models.Model):
    _name = 'hospital.research'
    _description = 'Research'

    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    research_type = fields.Many2one('hospital.research_type', string='Research Type', required=True)
    sample_type = fields.Many2one('hospital.sample_type', string='Simple Type', required=True)
    conclusions = fields.Text(string='Conclusions')

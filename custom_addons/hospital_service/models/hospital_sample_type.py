from odoo import models, fields, api


class SampleType(models.Model):
    _name = 'hospital.sample'
    _description = 'Sample Type'

    name = fields.Char(string='Sample Type', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')

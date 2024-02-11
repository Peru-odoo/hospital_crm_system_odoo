from odoo import models, fields, api


class SampleType(models.Model):
    _name = "hospital.sample_type"
    _description = "Sample Type"

    name = fields.Char(string="Sample Type", required=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")

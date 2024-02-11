from odoo import models, fields, api


class SampleType(models.Model):
    _name = "hospital.sample_type"
    _description = "Sample Type"
    _order = "name"

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Sample Type name must be unique."),
        ("unique_code", "UNIQUE(code)", "Sample Type code must be unique."),
    ]

    name = fields.Char(string="Sample Type", required=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")

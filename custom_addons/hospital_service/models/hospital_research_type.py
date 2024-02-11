from odoo import models, fields, api


class ResearchType(models.Model):
    _name = "hospital.research_type"
    _description = "Research Type"

    sql_constraints = [
        ("unique_name", "UNIQUE(name)", "Research Type name must be unique."),
        ("unique_code", "UNIQUE(code)", "Research Type code must be unique."),
    ]

    name = fields.Char(string="Research Type", required=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")
    parent_id = fields.Many2one("hospital.research_type", string="Parent Research Type")
    child_ids = fields.One2many(
        "hospital.research_type", "parent_id", string="Child Research Types"
    )

from odoo import models, fields, api


class ResearchType(models.Model):
    _name = 'hospital.research'
    _description = 'Research Type'

    name = fields.Char(string='Research Type', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('hospital.research', string='Parent Research Type')
    child_ids = fields.One2many('hospital.research', 'parent_id', string='Child Research Types')


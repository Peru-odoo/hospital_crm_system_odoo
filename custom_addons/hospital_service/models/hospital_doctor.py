from odoo import models, fields


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'
    _order = 'name'

    _inherit = 'hospital.abstractperson'

    specialty = fields.Char(string='Speciality')
    is_intern = fields.Boolean(string='Intern')
    mentor_id = fields.Many2one('hospital.doctor', string='Mentor', domain=[('is_intern', '=', False)])
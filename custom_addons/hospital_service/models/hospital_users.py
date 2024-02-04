from odoo import models, fields, api
from datetime import datetime


class PersonAbstract(models.AbstractModel):
    _name = 'hospital.abstractperson'
    _description = 'Abstract Person'

    name = fields.Char(string='Full Name', required=True)
    phone = fields.Char(string='Telephone Number')
    email = fields.Char(string='e-mail')
    photo = fields.Binary(string='Foto')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Femail'),
    ], string='Gender')


class ContactPerson(models.Model):
    _name = 'hospital.contactperson'
    _description = 'Contact person'
    _order = 'name'

    _inherit = 'hospital.abstractperson'


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'
    _order = 'name'

    _inherit = 'hospital.abstractperson'

    specialty = fields.Char(string='Speciality')
    is_intern = fields.Boolean(string='Intern')


class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'
    _order = 'name'

    _inherit = 'hospital.abstractperson'

    birth_date = fields.Date(string='Date of birth')
    age = fields.Integer(string='Age',  compute='_compute_age', store=True)
    passport_data = fields.Char(string='Passport data')
    contact_person = fields.Many2one('hospital.contactperson', string='Contact person')

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                birth_date_str = patient.birth_date.strftime("%Y-%m-%d")
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
                today = datetime.now().date()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                patient.age = age
            else:
                patient.age = 0

from odoo import models


class ContactPerson(models.Model):
    _name = "hospital.contactperson"
    _description = "Contact person"
    _order = "name"

    _inherit = "hospital.abstractperson"

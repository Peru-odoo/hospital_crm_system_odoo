from odoo import models, fields


class PersonAbstract(models.AbstractModel):
    _name = "hospital.abstractperson"
    _description = "Abstract Person"

    name = fields.Char(string="Full Name", required=True)
    phone = fields.Char(string="Telephone Number")
    email = fields.Char(string="e-mail")
    photo = fields.Binary(string="Foto")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Femail"),
        ],
        string="Gender",
    )

from odoo import fields, models, api


class Visit(models.Model):
    _name = "hospital.visit"
    _description = "Hospital Visit"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    date_availability = fields.Date(string="Available From")

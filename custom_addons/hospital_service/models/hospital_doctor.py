from odoo import models, fields


class Doctor(models.Model):
    _name = "hospital.doctor"
    _description = "Doctor"
    _order = "name"

    _inherit = "hospital.abstractperson"

    specialty = fields.Char(string="Speciality")
    is_intern = fields.Boolean(string="Intern")
    mentor_id = fields.Many2one(
        "hospital.doctor", string="Mentor", domain=[("is_intern", "=", False)]
    )
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def print_disease_report(self):
        return {
            "name": "Disease Report",
            "type": "ir.actions.act_window",
            "res_model": "hospital.report.wizard",
            "view_mode": "form",
            "view_id": self.env.ref("hospital_service.view_report_wizard_form").id,
            "target": "new",
        }

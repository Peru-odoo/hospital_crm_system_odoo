from odoo import models, fields, api


class ChangeDoctorWizard(models.TransientModel):
    _name = "hospital.change_doctor_wizard"
    _description = "Change Personal Doctor Wizard"

    new_doctor = fields.Many2one("hospital.doctor", string="New Personal Doctor")

    def change_doctor(self):
        active_ids = self.env.context.get("active_ids", [])
        patients = self.env["hospital.patient"].browse(active_ids)
        for patient in patients:
            patient.write({"personal_doctor": self.new_doctor.id})
        return {"type": "ir.actions.act_window_close"}

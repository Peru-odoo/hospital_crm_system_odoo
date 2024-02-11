from odoo import fields, models, api


class PersonalDoctorHistory(models.Model):
    _name = "hospital.personal_doctor_history"
    _description = "Personal Doctor History"

    name = fields.Char(string="Description", compute="_compute_name")
    patient = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    appointment_date = fields.Date(
        string="Appointment Date", default=fields.Date.today()
    )

    @api.depends("patient", "doctor")
    def _compute_name(self):
        for rec in self:
            if rec.patient.name and rec.doctor.name:
                rec.name = f"{rec.patient.name} - {rec.doctor.name}"
            else:
                rec.name = False

    def create_personal_doctor_history(self, patient_id, doctor_id):
        history_record = self.env["hospital.personal_doctor_history"].create(
            {
                "patient": patient_id,
                "doctor": doctor_id,
                "appointment_date": fields.Date.today(),
            }
        )
        return history_record

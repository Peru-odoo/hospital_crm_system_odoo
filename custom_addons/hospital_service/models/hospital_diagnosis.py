from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Diagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "Diagnosis"
    _order = "diagnosis_date DESC"

    name = fields.Char(string="Description", compute="_compute_name")
    patient = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    disease = fields.Many2one("hospital.disease", string="Disease", required=True)
    treatment = fields.Text(string="Prescribed treatment")
    diagnosis_date = fields.Date(string="Diagnosis Date", default=fields.Date.today())
    research_ids = fields.Many2many(
        "hospital.research",
        string="Research",
        copy=False,
        domain="[('patient', '=', patient)]",
    )
    doctor_visit = fields.Many2one("hospital.doctor_visit", string="Doctor Visit")
    status_diagnosis = fields.Selection(
        [("accepted_diagnosis", "Accepted"), ("reconsider", "Reconsider")],
        string="Status Diagnosis",
    )
    mentor_comment = fields.Text(string="Mentor Comment")

    @api.depends("patient", "doctor")
    def _compute_name(self):
        for rec in self:
            if rec.patient.name and rec.doctor.name and rec.diagnosis_date:
                rec.name = (
                    f"{rec.patient.name} - "
                    f"{rec.doctor.name} -"
                    f" {rec.diagnosis_date}"
                )
            else:
                rec.name = False

    @api.onchange("doctor_visit")
    def _onchange_doctor_visit(self):
        if self.doctor_visit:
            self.doctor = self.doctor_visit.doctor
            self.patient = self.doctor_visit.patient

    @api.model
    def create(self, values):
        diagnosis_record = super(Diagnosis, self).create(values)
        if diagnosis_record:
            doctor_visit = diagnosis_record.doctor_visit
            if doctor_visit and doctor_visit.state == "confirm_research":
                doctor_visit.write({"state": "make_diagnosis"})
        if diagnosis_record:
            doctor_visit = diagnosis_record.doctor_visit
            if doctor_visit and doctor_visit.state in (
                "confirm_research",
                "confirm_diagnosis",
                "make_recommendations",
                "completed",
            ):
                raise UserError(
                    "Cannot create a new research when "
                    "Doctor is in confirm all diagnosis."
                )
        return diagnosis_record

    def action_accept_diagnosis(self):
        self.status_diagnosis = "accepted_diagnosis"

    def action_reconsider_diagnosis(self):
        self.status_diagnosis = "reconsider"

    @api.onchange("doctor")
    def _onchange_doctor(self):
        if self.doctor.is_intern:
            raise ValidationError("Interns cannot be mentors.")

    @api.onchange("is_intern")
    def _onchange_is_intern(self):
        if self.is_intern and self.mentor_id:
            self.mentor_id = False

    @api.constrains("mentor_comment", "doctor", "doctor.is_intern")
    def _check_mentor_comment(self):
        for record in self:
            if record.doctor.is_intern and not record.mentor_comment:
                raise ValidationError(
                    "Mentor Comment is required for intern diagnoses."
                )

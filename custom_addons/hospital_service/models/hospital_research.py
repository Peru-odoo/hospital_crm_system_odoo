from odoo import models, fields, api
from odoo.exceptions import UserError


class Research(models.Model):
    _name = "hospital.research"
    _description = "Research"

    name = fields.Char(string="Name", required=True)
    patient = fields.Many2one("hospital.patient", string="Patient", required=True)
    doctor = fields.Many2one("hospital.doctor", string="Doctor", required=True)
    research_type = fields.Many2one("hospital.research_type", string="Research Type")
    sample_type = fields.Many2one("hospital.sample_type", string="Simple Type")
    conclusions = fields.Text(string="Conclusions")
    status_research = fields.Selection(
        [("accepted_research", "Accepted"), ("re-research", "Re-research")],
        string="Status Research",
    )
    doctor_visit = fields.Many2one("hospital.doctor_visit", string="Doctor Visit")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result

    @api.onchange("doctor_visit")
    def _onchange_doctor_visit(self):
        if self.doctor_visit:
            self.doctor = self.doctor_visit.doctor
            self.patient = self.doctor_visit.patient

    @api.model
    def create(self, values):
        research_record = super(Research, self).create(values)
        if research_record:
            doctor_visit = research_record.doctor_visit
            if doctor_visit and doctor_visit.state == "new":
                doctor_visit.write({"state": "add_research"})
        if research_record:
            doctor_visit = research_record.doctor_visit
            if doctor_visit and doctor_visit.state in (
                "confirm_research",
                "make_diagnosis",
                "confirm_diagnosis",
                "make_recommendations",
                "completed",
            ):
                raise UserError(
                    "Cannot create a new research when "
                    "Doctor is in confirm all research."
                )
        return research_record

    @api.model
    def unlink(self):
        for research_record in self:
            if research_record.status_research == "accepted_research":
                raise UserError("Cannot delete a research with " "status 'accepted'.")
        return super(Research, self).unlink()

    def action_accept_research(self):
        self.status_research = "accepted_research"

    def action_decline_research(self):
        self.status_research = "re-research"

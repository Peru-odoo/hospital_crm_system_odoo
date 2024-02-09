from odoo import models, fields, api
from odoo.exceptions import UserError


class Research(models.Model):
    _name = 'hospital.research'
    _description = 'Research'

    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    research_type = fields.Many2one('hospital.research_type', string='Research Type')
    sample_type = fields.Many2one('hospital.sample_type', string='Simple Type')
    conclusions = fields.Text(string='Conclusions')
    status_research = fields.Selection([('accepted_research', 'Accepted'),
                               ('re-research', 'Re-research')],
                              string='Status Research')
    doctor_visit = fields.Many2one('hospital.doctor_visit', string='Doctor Visit')

    @api.onchange('doctor_visit')
    def _onchange_doctor_visit(self):
        if self.doctor_visit:
            self.doctor = self.doctor_visit.doctor
            self.patient = self.doctor_visit.patient

    @api.model
    def create(self, values):
        if values.get('state') == 'confirm_research':
            raise UserError("Cannot create a new record with status confirm_research.")
        research_record = super(Research, self).create(values)
        if research_record:
            doctor_visit = research_record.doctor_visit
            if doctor_visit and doctor_visit.state == 'new':
                doctor_visit.write({'state': 'add_research'})
        if research_record:
            doctor_visit = research_record.doctor_visit
            if doctor_visit and doctor_visit.state == 'confirm_research':
                raise UserError(
                    "Cannot create a new research when DoctorVisit is in confirm_research state.")
        return research_record

    @api.model
    def unlink(self):
        for research_record in self:
            if research_record.status_research == 'accepted_research':
                raise UserError("Cannot delete a research with status 'accepted'.")
        return super(Research, self).unlink()

    def action_accept_research(self):
        self.status_research = 'accepted_research'

    def action_decline_research(self):
        self.status_research = 're-research'

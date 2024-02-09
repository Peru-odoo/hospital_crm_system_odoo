from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Diagnosis'

    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    disease = fields.Many2one('hospital.disease', string='Disease', required=True)
    treatment = fields.Text(string='Prescribed treatment')
    diagnosis_date = fields.Date(string='Diagnosis Date', default=fields.Date.today())
    research_ids = fields.Many2many('hospital.research', string='Research', copy=False)
    doctor_visit = fields.Many2one('hospital.doctor_visit', string='Doctor Visit')
    status_diagnosis = fields.Selection([('accepted_diagnosis', 'Accepted'),
                               ('reconsider', 'Reconsider')],
                              string='Status Diagnosis')
    mentor_comment = fields.Text(string='Mentor Comment')

    @api.onchange('doctor_visit')
    def _onchange_doctor_visit(self):
        if self.doctor_visit:
            self.doctor = self.doctor_visit.doctor
            self.patient = self.doctor_visit.patient

    @api.model
    def create(self, values):
        if values.get('state') == 'confirm_diagnosis':
            raise UserError("Cannot create a new record with status confirm_research.")
        diagnosis_record = super(Diagnosis, self).create(values)
        if diagnosis_record:
            doctor_visit = diagnosis_record.doctor_visit
            if doctor_visit and doctor_visit.state == 'confirm_research':
                doctor_visit.write({'state': 'make_diagnosis'})
        if diagnosis_record:
            doctor_visit = diagnosis_record.doctor_visit
            if doctor_visit and doctor_visit.state == 'confirm_diagnosis':
                raise UserError(
                    "Cannot create a new diagnosis when all diagnosis are confirmed.")
        return diagnosis_record

    def action_accept_diagnosis(self):
        self.status_diagnosis = 'accepted_diagnosis'

    def action_reconsider_diagnosis(self):
        self.status_diagnosis = 'reconsider'

    # @api.onchange('doctor')
    # def _onchange_doctor(self):
    #     if self.doctor.is_intern:
    #         raise ValidationError("Interns cannot be mentors.")
    #
    # @api.onchange('is_intern')
    # def _onchange_is_intern(self):
    #     if self.is_intern and self.mentor_id:
    #         self.mentor_id = False
    #
    # @api.constrains('mentor_comment', 'doctor', 'doctor.is_intern')
    # def _check_mentor_comment(self):
    #     for record in self:
    #         if record.doctor.is_intern and not record.mentor_comment:
    #             raise ValidationError("Mentor Comment is required for intern diagnoses.")

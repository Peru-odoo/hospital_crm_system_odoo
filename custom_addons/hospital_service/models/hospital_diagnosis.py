from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Diagnosis'

    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    disease = fields.Many2one('hospital.disease', string='Disease', required=True)
    treatment = fields.Text(string='Treatment')
    diagnosis_date = fields.Date(string='Diagnosis Date', default=fields.Date.today())
    research_ids = fields.Many2many('hospital.research', string='Research', copy=False)

    doctor_visit = fields.Many2one('hospital.doctor_visit', string='Doctor Visit')

    status = fields.Selection([('accepted', 'Accepted'),
                               ('re-research', 'Re-research')],
                              string='Status')

    mentor_comment = fields.Text(string='Mentor Comment')

    @api.onchange('doctor_visit')
    def _onchange_doctor_visit(self):
        if self.doctor_visit:
            self.doctor = self.doctor_visit.doctor
            self.patient = self.doctor_visit.patient

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

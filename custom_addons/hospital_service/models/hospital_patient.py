from odoo import models, fields, api
from datetime import datetime



class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'
    _order = 'name'

    _inherit = 'hospital.abstractperson'

    birth_date = fields.Date(string='Date of birth')
    age = fields.Integer(string='Age',  compute='_compute_age', store=True)
    passport_data = fields.Char(string='Passport data')
    contact_person = fields.Many2one('hospital.contactperson', string='Contact person')
    personal_doctor = fields.Many2one('hospital.doctor', string='Personal Doctor', ondelete='restrict')
    history_ids = fields.One2many('hospital.personal_doctor_history', 'patient', string='Doctor History')

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                birth_date_str = patient.birth_date.strftime("%Y-%m-%d")
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
                today = datetime.now().date()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                patient.age = age
            else:
                patient.age = 0

    @api.onchange('personal_doctor')
    def _onchange_personal_doctor(self):
        if self.personal_doctor and self.id:
            last_history = self.env['hospital.personal_doctor_history'].search(
                [('patient', '=', self.id)], order='appointment_date desc', limit=1
            )
            if not last_history or last_history.doctor != self.personal_doctor:
                self.env['hospital.personal_doctor_history'].create({
                    'patient': self.id,
                    'doctor': self.personal_doctor.id,
                    'appointment_date': fields.Date.today(),
                })

    def write(self, values):
        res = super(Patient, self).write(values)
        if 'personal_doctor' in values:
            self._onchange_personal_doctor()
        return res

    def change_personal_doctor(self):
        return {
            'name': 'Change Personal Doctor',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.change_doctor_wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('hospital_service.view_change_doctor_wizard_form').id,
            'target': 'new',
            'context': {'default_new_doctor': self.personal_doctor.id if self.personal_doctor else False},
        }

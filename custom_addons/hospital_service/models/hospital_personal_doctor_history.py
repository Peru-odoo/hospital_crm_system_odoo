from odoo import fields, models, api


class PersonalDoctorHistory(models.Model):
    _name = 'hospital.personal_doctor_history'
    _description = 'Personal Doctor History'

    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    appointment_date = fields.Date(string='Appointment Date', default=fields.Date.today())

    def create_personal_doctor_history(self, patient_id, doctor_id):
        history_record = self.env['hospital.personal_doctor_history'].create({
            'patient': patient_id,
            'doctor': doctor_id,
            'appointment_date': fields.Date.today(),
        })
        return history_record

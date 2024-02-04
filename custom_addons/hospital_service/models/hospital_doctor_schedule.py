from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class DoctorSchedule(models.Model):
    _name = 'hospital.doctor_schedule'
    _description = 'Doctor Schedule'

    _sql_constraints = [
        ('unique_appointment_datetime', 'unique(doctor, appointment_datetime)',
         'Appointment date & time must be unique per doctor.'),
    ]

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_datetime = fields.Datetime(string='Appointment Date & Time', required=True)

    @api.onchange('appointment_datetime')
    def _onchange_appointment_datetime(self):
        if self.appointment_datetime:
            end_datetime = fields.Datetime.from_string(self.appointment_datetime) + timedelta(minutes=30)
            existing_appointment = self.env['hospital.doctor_schedule'].search([
                ('doctor', '=', self.doctor.id),
                ('appointment_datetime', '<', end_datetime),
                ('appointment_datetime', '>=', self.appointment_datetime),
            ])
            if existing_appointment:
                raise ValidationError("Selected date & time is not available. Please choose another.")

    @api.constrains('appointment_datetime')
    def _check_appointment_datetime(self):
        for record in self:
            if record.appointment_datetime <= fields.Datetime.now():
                raise ValidationError("Appointment date & time should be in the future.")

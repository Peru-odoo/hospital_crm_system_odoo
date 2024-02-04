from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DoctorSchedule(models.Model):
    _name = 'hospital.doctor_schedule'
    _description = 'Doctor Schedule'

    _sql_constraints = [
        ('unique_appointment', 'unique(doctor, date, start_time, end_time)', 'Appointment must be unique.'),
    ]

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    date = fields.Date(string='Date', required=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)

    @api.constrains('date', 'start_time', 'end_time')
    def _check_appointment_uniqueness(self):
        for appointment in self:
            overlapping_appointments = self.search([
                ('doctor', '=', appointment.doctor.id),
                ('date', '=', appointment.date),
                ('start_time', '<', appointment.end_time),
                ('end_time', '>', appointment.start_time),
                ('id', '!=', appointment.id),
            ])
            if overlapping_appointments:
                raise ValidationError("Selected appointment overlaps with existing appointments.")

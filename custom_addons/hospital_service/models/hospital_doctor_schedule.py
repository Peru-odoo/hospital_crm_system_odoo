from odoo import models, fields, api


class DoctorSchedule(models.Model):
    _name = 'hospital.schedule'
    _description = 'Doctor Availability'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    appointment_date = fields.Date(string='Appointment Date', required=True)
    time_slots = fields.One2many('hospital.schedule.line', 'schedule_id', string='Time Slots')


class DoctorAvailabilitySlot(models.Model):
    _name = 'hospital.schedule.line'
    _description = 'Doctor Availability Slot'

    schedule_id = fields.Many2one('hospital.schedule', string='Availability', ondelete='cascade')
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)

    @api.constrains('start_time', 'end_time')
    def _check_time_range(self):
        for slot in self:
            if slot.start_time >= slot.end_time:
                raise ValueError("End time must be greater than start time")

            same_day_slots = self.search([
                ('schedule_id.appointment_date', '=', slot.schedule_id.appointment_date),
                ('id', '!=', slot.id),
            ])

            for existing_slot in same_day_slots:
                if (slot.start_time < existing_slot.end_time and
                        slot.end_time > existing_slot.start_time):
                    raise ValueError("Time slot overlaps with existing slots")

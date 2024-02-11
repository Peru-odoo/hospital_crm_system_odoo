from odoo import api, fields, models
from odoo.exceptions import UserError


class DoctorVisit(models.Model):
    _name = 'hospital.doctor_visit'
    _description = 'Doctor Visit'

    state = fields.Selection(
        [
            ('create', 'Create Visit'),
            ('new', 'Visit Doctor'),
            ('add_research', 'Add research'),
            ('confirm_research', 'Confirm research'),
            ('make_diagnosis', 'Make diagnosis'),
            ('confirm_diagnosis', 'Confirm diagnosis'),
            ('make_recommendations', 'Make recommendations'),
            ('completed', 'Visit Completed')
        ],
        default='create',
        string='Status')

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Date(string='Appointment Date', required=True)
    time_slot = fields.Many2one(
        'hospital.schedule.line',
        string='Available Time',
        domain="[('schedule_id.appointment_date', '=', appointment_date), ('is_slot_occupied', '=', False), ('doctor', '=', doctor)]",
        required=True
    )
    recommendations = fields.Text(string='Recommendations')
    research_ids = fields.One2many('hospital.research', 'doctor_visit', string='Research')
    diagnosis_ids = fields.One2many('hospital.diagnosis', 'doctor_visit', string='Diagnosis')

    @api.onchange('time_slot')
    def _onchange_time_slot(self):
        if self.time_slot:
            previous_slot = self._origin.time_slot if self._origin else False
            if previous_slot:
                previous_slot.is_slot_occupied = False
            self.time_slot.is_slot_occupied = True

    def action_finish_research(self):
        if all(research.status_research == 'accepted_research' for research in self.research_ids):
            self.state = 'confirm_research'
        else:
            raise UserError("Not all research are in 'accepted' status.")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Research finish success',
                'type': 'rainbow_man'
            }
        }

    def action_skip_research(self):
        self.state = 'confirm_research'

    def action_finish_diagnosis(self):
        if all(diagnosis.status_diagnosis == 'accepted_diagnosis' for diagnosis in self.diagnosis_ids):
            self.state = 'confirm_diagnosis'
        else:
            raise UserError("Not all diagnosis are in 'accepted' status.")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Diagnosis finish success',
                'type': 'rainbow_man'
            }
        }

    def action_skip_diagnosis(self):
        self.state = 'confirm_diagnosis'

    def action_accept_recommendations(self):
        self.state = 'completed'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Recommendations finish success',
                'type': 'rainbow_man'
            }
        }

    @api.model
    def create(self, values):
        record = super(DoctorVisit, self).create(values)
        if record:
            record.write({'state': 'new'})
        return record

    def unlink(self):
        for record in self:
            if record.state != 'new':
                raise UserError("Cannot delete a record with status other than 'new'.")
        return super(DoctorVisit, self).unlink()

    def write(self, values):
        if 'recommendations' in values:
            self.state = 'make_recommendations'
        return super(DoctorVisit, self).write(values)

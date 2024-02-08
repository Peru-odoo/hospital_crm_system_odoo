from odoo import api, fields, models
from odoo.exceptions import UserError


class DoctorVisit(models.Model):
    _name = 'hospital.doctor_visit'
    _description = 'Doctor Visit'

    time_slot = fields.Many2one(
        'hospital.schedule.line',
        string='Available Time',
        domain="[('schedule_id.appointment_date', '=', appointment_date)]",
        help='Select Time Slot',
    )

    state = fields.Selection(
        [
            ('new', 'New Visit'),
            ('add_research', 'Add research'),
            ('confirm_research', 'Confirm research'),
            ('make_diagnosis', 'Make diagnosis'),
            ('confirm_diagnosis', 'Confirm diagnosis'),
            ('make_recommendations', 'Make recommendations'),
            ('confirm_recommendations', 'Confirm recommendations'),
            ('completed', 'Visit Completed')
        ],
        default='new',
        string='Status')

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Date(string='Appointment Date', required=True)
    diagnosis_id = fields.Many2many('hospital.diagnosis', string='Diagnosis')
    recommendations = fields.Text(string='Recommendations')
    is_completed = fields.Boolean(string='Visit Completed', default=False)
    research_ids = fields.One2many('hospital.research', 'doctor_visit', string='Research')

    def action_finish_research(self):
        if all(research.status == 'accepted' for research in self.research_ids):
            self.state = 'confirm_research'
        else:
            raise UserError("Not all research are in 'accepted' status.")

    @api.model
    def check_access_create(self):
        if self.state == 'confirm_research':
            raise UserError("Cannot add new research to a completed visit.")

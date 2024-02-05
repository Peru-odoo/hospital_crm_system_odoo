from odoo import models, fields, api


class DoctorVisit(models.Model):
    _name = 'hospital.doctor_visit'
    _description = 'Doctor Visit'

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Many2one('hospital.doctor_schedule', string='Doctor Appointment Date', required=True)
    appointment_time = fields.Float(string='Doctor Appointment Time', required=True)
    recommendations = fields.Text(string='Recommendations')
    is_completed = fields.Boolean(string='Visit Completed', default=False)
    research_ids = fields.Many2many('hospital.research', string='Research', copy=False)
    diagnosis_id = fields.Many2one('hospital.diagnosis', string='Diagnosis')

    @api.onchange('doctor', 'appointment_date')
    def _onchange_doctor(self):
        if self.doctor and self.appointment_date:
            # Отримання доступного часу для прийому відповідно до обраного лікаря і дати
            available_times = self.doctor.get_available_times(self.appointment_date)
            # Встановлення доступних часів для вибору
            self.appointment_time = False  # Забезпечте відсутність значення перед обчисленням нового значення
            return {'domain': {'appointment_time': [('id', 'in', available_times)]}}


from odoo import models, fields, api


class ReportWizard(models.TransientModel):
    _name = 'hospital.report.wizard'
    _description = 'Disease Report Wizard'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def print_disease_report(self):
        diseases = self.env['hospital.disease'].search([])
        report_data = {}
        for disease in diseases:
            diagnoses_count = self.env['hospital.diagnosis'].search_count([
                ('disease', '=', disease.id),
                ('diagnosis_date', '>=', self.start_date),
                ('diagnosis_date', '<=', self.end_date),
            ])
            report_data[disease.name] = diagnoses_count

        print(report_data)
        # self.env['your.report.model'].create({'data': report_data}) # Todo aбо зберегти результат у модель звіту(доробити)

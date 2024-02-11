from odoo import models, fields, api


class ReportWizard(models.TransientModel):
    _name = 'hospital.report.wizard'
    _description = 'Disease Report Wizard'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def print_disease_report(self):
        existing_reports = self.env['hospital.report.disease'].search([])
        existing_reports.unlink()
        diseases = self.env['hospital.disease'].search([])
        report_data = []
        for disease in diseases:
            diagnoses_count = self.env['hospital.diagnosis'].search_count([
                ('disease', '=', disease.id),
                ('diagnosis_date', '>=', self.start_date),
                ('diagnosis_date', '<=', self.end_date),
            ])
            report_data.append({
                'disease': disease.name,
                'diagnoses_count': diagnoses_count
            })
        self.env['hospital.report.disease'].create(report_data)
        return {
            'name': 'Disease Report',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.report.disease',
            'view_mode': 'tree',
            'view_id': self.env.ref('hospital_service.view_report_wizard_tree').id,
            'target': 'new',
        }

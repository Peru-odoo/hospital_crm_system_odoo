from odoo import models, fields


class ReportDiseaseModel(models.Model):
    _name = "hospital.report.disease"
    _description = "Report Disease Model"

    disease = fields.Char(string="Disease")
    diagnoses_count = fields.Integer(string="Diagnoses Count")

from odoo import models, fields, api


class Disease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease Directory'
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(string='Disease Name', required=True)
    code = fields.Char(string='Disease Code')
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('hospital.disease', string='Parent Category', index=True, ondelete='cascade')
    child_ids = fields.One2many('hospital.disease', 'parent_id', string='Subcategories')
    parent_path = fields.Char(index=True)

    # Цей метод встановлює шлях до батьківської категорії для ієрархічної моделі
    @api.depends('parent_id.parent_path')
    def _compute_parent_path(self):
        for record in self:
            if record.parent_id:
                record.parent_path = '%s/%s' % (record.parent_id.parent_path, record.parent_id.id)
            else:
                record.parent_path = ''

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class ExportHistory(models.Model):

    _name = "export.history"
    _description = "导出履歴"

    journal_number = fields.Many2one('journal.number',  string='刊期', compute='_compute_concurrent')
    name = fields.Many2one('customer.info',  string='顧客', required=True)
    company_abbreviation = fields.Char('会社略称', related='name.company_abbreviation', store=False)
    affiliation_abbreviation = fields.Char('所属略称', related='name.affiliation_abbreviation', store=False)
    position = fields.Char('役職', related='name.position', store=False)
    work_email = fields.Char('勤務先の電子メール', related='name.work_email', store=False)
    office_name = fields.Char('オフィス', related='name.office_name', store=False)
    propose_department = fields.Char('対応部門', related='name.propose_department', store=False)
    fnst_member = fields.Char('FNST担当者名', related='name.fnst_member', store=False)
    company_name = fields.Char('会社名', related='name.account_name', store=False)
    department_name = fields.Char('所属1', related='name.department_name', store=False)
    abbreviated = fields.Char('所属2', related='name.department_name', store=False)
    sender_postal_address = fields.Char('住所', related='name.account_name', store=False)
    postal_address = fields.Char('郵便先', related='name.account_name', store=False)
    sender_postal_code = fields.Char('郵便番号', related='name.sender_postal_code', store=False)
    sender_department = fields.Char('送信元', related='name.sender_department', store=False)
    is_active = fields.Boolean('Is Active', related='name.is_active', store=False)
    flag = fields.Boolean('是否最新', default=False)

    @api.model
    def _compute_concurrent(self):
        self.env.cr.execute("select max(id) from journal_number")
        dicts = self.env.cr.dictfetchall()
        for record in self:
            record.journal_number = dicts[0]['max']
        print("0", str(dicts[0]['max']))

    @api.model
    def create(self, values):
        self.env.cr.execute("select max(id) from journal_number")
        dicts = self.env.cr.dictfetchall()
        print(values)
        if values['journal_number'] == dicts[0]['max']:
            values['flag'] = 'True'
        new_record = super(ExportHistory, self.with_context(mail_create_nosubscribe=True)).create(values)
        return new_record




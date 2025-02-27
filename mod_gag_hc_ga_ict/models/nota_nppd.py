from odoo import api, models, fields, _
import logging

class NotaNppd(models.Model):
    _logger = logging.getLogger(__name__)
    _name = "hc.nppd"
    _description = "Model for Nota NPPD"

    no_nota = fields.Char(string="No. Nota", required=True)
    tanggal = fields.Date(string="Tanggal", required=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.user.company_id.currency_id.id
    )
    total = fields.Monetary(string="Total", compute="_compute_total_nominal", store=True, currency_field='currency_id')

    nppd_item = fields.One2many("hc.nppd.items", "id_nppd", string="Item")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.no_nota}"  # Custom display
            result.append((record.id, display_name))
        return result

    @api.depends('nppd_item.nominal')
    def _compute_total_nominal(self):
        for record in self:
            # Sum the nominal field from related hc.nppd.items
            total = sum(item.nominal for item in record.nppd_item)
            record.total = total

    @api.model
    def create(self, vals):
        # Create the hc.nppd record
        record = super(NotaNppd, self).create(vals)

        # Update state in related spplk_id (from hc.nppd.items)
        record._update_spplk_state()

        return record

    def write(self, vals):
        # Create the hc.nppd record
        record = super(NotaNppd, self).write(vals)

        # Update state in related spplk_id (from hc.nppd.items)
        self._update_spplk_state()

        return record


    def unlink(self):
        # First, delete all related hc.nppd.items records
        for record in self:
            for item in record.nppd_item:
                spplk = self.env['hc.surat.perintah.pembelian.langsung'].browse(item.spplk_id.id)
                if spplk:
                    # Update the state of the related spplk_id
                    spplk.write({'state': 'pending'})  # Set the state you need here
            # Search for all hc.nppd.items that are related to this hc.nppd record
            related_items = self.env['hc.nppd.items'].search([('id_nppd', '=', record.id)])
            related_items.unlink()  # This deletes the related hc.nppd.items records

        # Proceed with deleting the hc.nppd record
        return super(NotaNppd, self).unlink()

    def _update_spplk_state(self):
        # Iterate through the related nppd_item records and update the spplk_id state
        for item in self.nppd_item:
            spplk = self.env['hc.surat.perintah.pembelian.langsung'].browse(item.spplk_id.id)
            if spplk:
                # Update the state of the related spplk_id
                spplk.write({'state': 'submitted'})  # Set the state you need here

    @api.model
    def _get_report_values(self, docids, data=None):
        _logger.error("====== Report is being called ======")  # Debug line

        res = super(NotaNppd, self)._get_report_values(docids, data)
        appr_list = self.env['hc.master.approval.ndpp'].search([])
        _logger.error(f"Approval data found: {appr_list}")  # Debug line

        res.update({
            'doc_ids': docids,
            'doc_model': 'your.model.name',  # Replace with your actual model
            'appr_list': appr_list,
        })
        return res

class NotaNppdItem(models.Model):
    _name = "hc.nppd.items"
    _description = "Model for Nota NPPD Items"

    spplk_id = fields.Many2one("hc.surat.perintah.pembelian.langsung", string="SPPLK", required=True, domain="[('state', '=', 'pending')]")
    tanggal = fields.Date(string="Tanggal", related="spplk_id.tanggal", readonly=True)
    jam = fields.Float(string="Jam Waktu Pembelian", related="spplk_id.jam", readonly=True)
    nama_kios = fields.Char(string="Nama Kios Pengambilan", related="spplk_id.nama_kios", readonly=True)
    nama_barang = fields.Char(string="Nama Barang", related="spplk_id.nama_barang", readonly=True)
    keterangan = fields.Text(string="Keterangan Pemerintah Atasan", related="spplk_id.keterangan", readonly=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True, related="spplk_id.currency_id", readonly=True)
    nominal = fields.Monetary(string="Nominal Pembelian", related="spplk_id.nominal", readonly=True)

    id_nppd = fields.Many2one("hc.nppd", string="ID Nota")

    @api.model
    def unlink(self):
        # First, delete all related hc.nppd.items records
        for record in self:
            spplk = self.env['hc.surat.perintah.pembelian.langsung'].browse(record.spplk_id.id)
            if spplk:
                # Update the state of the related spplk_id
                spplk.write({'state': 'pending'})  # Set the state you need here

        # Proceed with deleting the hc.nppd record
        return super(NotaNppdItem, self).unlink()

class NotaNppdReport(models.AbstractModel):
    _name = 'report.mod_gag_hc_ga_ict.nppd'  # Must match the 'name' in your XML
    _description = 'Report NDPP'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hc.nppd'].browse(docids)  # Get the requested records
        appr_list = self.env['hc.master.approval.ndpp'].search([])  # Fetch approval list

        return {
            'doc_ids': docids,
            'doc_model': 'hc.nppd',
            'docs': docs,
            'appr_list': appr_list,  # Approval list for signatures
        }
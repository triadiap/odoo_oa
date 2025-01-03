from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HSERekapBibit(models.Model):
    _name = "gag.oa.hse.rekap.bibit"
    _description = "REKAP DATA BIBIT KELUAR - MASUK"

    jenis = fields.Char('Jenis', required=True)
    kelompok = fields.Selection([
        ('Lokal','Lokal'),
        ('non Lokal','non Lokal')
        ],"kelompok bibit")
    tipe = fields.Selection([
        ('Fastgrowing','Fastgrowing'),
        ('Daur Panjang','Daur Panjang')
        ],"Tipe")
    sumber = fields.Selection([
        ('Benih/biji','Benih/biji'),
        ('anakan alami','anakan alami'),
        ('Puteran','Puteran'),
        ('Cangkokan','Cangkokan'),
        ('Stek','Stek'),
        ('Kultur Jaringan','Kultur Jaringan'),
        ('Sambung Pucuk','Sambung Pucuk'),
        ('Okulasi','Okulasi'),
        ],"Sumber Biji")
    pasokan = fields.Selection([
        ('Kelompok Fanuntilari','Kelompok Fanuntilari'),
        ('Nursery Gag Nikel','Nursery Gag Nikel'),
        ('Mitra Kerja Lain','Mitra Kerja Lain')
        ],"Sumber Pasokan")
    tahun = fields.Char('Tahun', required=True)
    jumlah_masuk = fields.Integer('Jumlah bibit masuk')
    tanggal_masuk = fields.Date('Tanggal bibit masuk')
    jumlah_keluar = fields.Integer('Jumlah bibit keluar')
    tanggal_keluar = fields.Date('Tanggal bibit keluar')
    stok = fields.Integer('Stok Bibit',compute="_calculate_stok", store = True)
    keterangan = fields.Char('Keterangan')

    @api.depends("jumlah_masuk","jumlah_keluar")
    def _calculate_stok(self):
        for rec in self:
            total_awal = 0
            #total_awal = float(sum(self.env['gag.oa.hse.rekap.bibit'].search([('id','<',rec.id)]).mapped('jumlah_masuk')))-float(sum(self.env['gag.oa.hse.rekap.bibit'].search([('id','<',rec.id)]).mapped('jumlah_keluar')))
            rec.stok = total_awal + rec.jumlah_masuk - rec.jumlah_keluar

    @api.model
    def retrieve_dashboard(self):
        self.check_access_rights('read')
        result = {
            'total_masuk': 0,
            'total_keluar': 0,
            'total_stok': 0,
        }
        result["total_masuk"] = float(sum(self.env['gag.oa.hse.rekap.bibit'].search([('id','!=',False)]).mapped('jumlah_masuk')))
        result["total_keluar"] = float(sum(self.env['gag.oa.hse.rekap.bibit'].search([('id','!=',False)]).mapped('jumlah_keluar')))
        result["total_stok"] = float(sum(self.env['gag.oa.hse.rekap.bibit'].search([('id','!=',False)]).mapped('jumlah_masuk'))) - float(sum(self.env['gag.oa.hse.rekap.bibit'].search([('id','!=',False)]).mapped('jumlah_keluar')))
        return result
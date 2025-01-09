from odoo import api, models, fields, _


class CorsecDocRequest(models.Model):
    _name = "corsec.doc.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "CORSEC & Legal Document Request"

    requester_user_id = fields.Many2one("res.users", string="Nama Pemohon", readonly=True,
                                        default=lambda self: self.env.user.id)
    department_id = fields.Many2one("hr.department", string="Satker", readonly=True,
                                    default=lambda self: self.env.user.department_id.id)
    req_doc = fields.Text(string="Dokumen Yang Diminta", required=True)
    keperluan = fields.Text(string="Keperluan", required=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("approved", "Approved"),
        ("rejected", "Rejected")
    ], string="Status", default="draft")

    list_akta = fields.One2many("corsec.doc.request.akta.notaris", "id_req", string="List Akta Notaris")
    list_bod_boc = fields.One2many("corsec.doc.request.bod.boc", "id_req", string="List BOD - BOC")
    list_did = fields.One2many("corsec.doc.request.daftar.izin", "id_req", string="Dokumen Izin")
    list_risalah_direksi = fields.One2many("corsec.doc.request.risalah.direksi", "id_req", string="Risalah Rapat Direksi")
    list_risalah_komisaris = fields.One2many("corsec.doc.request.risalah.komisaris", "id_req",
                                           string="Risalah Rapat Komisaris")

    def name_get(self):
        result = []
        for record in self:
            display_name = f"{record.requester_user_id.display_name} - {record.department_id.display_name}"  # Custom display
            result.append((record.id, display_name))
        return result

    @api.model
    def create(self, vals):
        record = super(CorsecDocRequest, self).create(vals)
        model_id = self.env['ir.model']._get('corsec.doc.request')  # Retrieve the model's ID
        if not model_id:
            raise ValueError("The model 'corsec.doc.request' could not be found. Ensure it is defined correctly.")
        # Step 3: Create a mail activity linked to the created record
        self.env['mail.activity'].sudo().create({
            'res_model_id': model_id.id,  # Use the retrieved model ID
            'res_id': record.id,  # Use the ID of the created maintenance task
            'activity_type_id': 4,  # Replace with the correct activity type ID
            'summary': "Permintaan Dokumen Baru",
            'note': f"{record.requester_user_id.display_name} dari Satker {record.department_id.display_name} meminta beberapa dokumen",
            'user_id': self.env.user.id,  # Assigned user
        })
        return record

    def action_approve(self):
        self.state = 'approved'
        print(self.requester_user_id.id)
        self.env['bus.bus'].sendone(
            (self.requester_user_id.id,),  # Target the requester's partner
            {
                'title': 'Document Approved',
                'message': 'Dokumen yang anda minta sudah tersedia!',
                'type': 'success',  # Success type for approval
            }
        )

    def action_reject(self):
        self.state = 'rejected'
        print(self.requester_user_id.id)
        self.env['bus.bus'].sendone(
            (self.requester_user_id.id,),  # Target the requester's partner
            'simple_notification',  # Type of notification
            {
                'title': 'Permintaan Dokumen Ditolak',
                'message': 'Dokumen yang anda minta ditolak',
                'type': 'danger',  # Success type for approval
            }
        )

class CorsecDocAktaNotaris(models.Model):
    _name = "corsec.doc.request.akta.notaris"
    _description = "CORSEC Doc Request Akta Notaris"

    name = fields.Many2one("corsec.list.akta.notaris", string="List Akta Notaris")
    id_req = fields.Many2one("corsec.doc.request", string="ID Doc Req")

class CorsecDocBodBoc(models.Model):
    _name = "corsec.doc.request.bod.boc"
    _description = "CORSEC Doc Request Dokumen BOD - BOC"

    name = fields.Many2one("corsec.daftar.bod.boc", string="Daftar BOD - BOC")
    id_req = fields.Many2one("corsec.doc.request", string="ID Doc Req")

class CorsecDocDaftarIzin(models.Model):
    _name = "corsec.doc.request.daftar.izin"
    _description = "CORSEC Doc Request Daftar Izin"

    name = fields.Many2one("corsec.daftar.izin", string="Dokumen Izin")
    id_req = fields.Many2one("corsec.doc.request", string="ID Doc Req")

class CorsecDocRisalahDireksi(models.Model):
    _name = "corsec.doc.request.risalah.direksi"
    _description = "CORSEC Doc Request Risalah Rapat Direksi"

    name = fields.Many2one("corsec.risalah.rapat.direksi", string="Risalah Rapat Direksi")
    id_req = fields.Many2one("corsec.doc.request", string="ID Doc Req")

class CorsecDocRisalahKomisaris(models.Model):
    _name = "corsec.doc.request.risalah.komisaris"
    _description = "CORSEC Doc Request Risalah Rapat Komisaris"

    name = fields.Many2one("corsec.risalah.rapat.komisaris")
    id_req = fields.Many2one("corsec.doc.request", string="ID Doc Req")
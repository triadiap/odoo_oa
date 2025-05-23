{
    'name': 'PTGN MO',
    'version': '1.0.0',
    'summary': 'This module has been build for PT GAG Nikel MO Team',
    'sequence': -100,
    'description': """This module has been build for PT GAG Nikel MO team""",
    'category': 'Productivity',
    'author': 'Internusa Cipta Solusi Perdana (ICSP)',
    'maintainer': 'Internusa Cipta Solusi Perdana (ICSP)',
    'website': 'https://icsp.co.id',
    'depends': ['mail', 'mod_gag_uac'],
    'data': [
        'security/ir.model.access.csv',
        'views/mo_purchase_req.xml',
        'views/mo_rekapan_lembur.xml',
        'views/mo_ijin_keluar.xml',
        'views/mo_cuti_roster.xml',
        'views/mo_job_pending.xml',
        'views/mo_minutes_meeting.xml',
        'views/mo_absensi_weekly_meeting.xml',
        'views/mo_cuti_roster_struktural.xml',
        'views/mo_cuti_tahunan.xml',
        'views/mo_lkh.xml',
        'views/mo_barging_mm.xml',
        'views/mo_production_mm.xml',
        'views/mo_daftar_hadir.xml',
        'views/mo_lkh_minedev.xml',
        'views/mo_safety_talk.xml',
        'views/mo_inspeksi_harian.xml',
        'views/mo_permintaan_apd.xml',
        'views/mo_surat_keterangan_sakit.xml',
        'views/mo_permintaan_pengeluaran_barang.xml',
        'views/mo_work_request.xml',
        'views/mo_master_equipment.xml',
        'views/mo_master_apd.xml',
        'views/mo_master_lokasi.xml',
        'views/menulist.xml',
        'report/report_minutes_meeting.xml',
        'views/assets.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
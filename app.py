# app.py (Versi yang sudah dimodifikasi)

from flask import Flask, render_template, request, jsonify, session
from collections import defaultdict
import datetime
import os
import time 
import atexit  # <<< DITAMBAHKAN: Untuk menjalankan fungsi saat aplikasi berhenti

# <<< DITAMBAHKAN: Impor fungsi dari file data_manager.py
from data_manager import save_app_data, load_app_data

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'financial_accounting_secret_key_2024')

# <<< DITAMBAHKAN: Tentukan nama file untuk menyimpan data
DATA_FILE = "financial_data.json"

# Translation dictionary (tidak ada perubahan di sini)
translations = {
    "en": {
        "title": "Adrien's Financial",
        "home": "Home",
        "language": "Language",
        "financial_statement": "FINANCIAL STATEMENT OF COMPANY",
        "income": "Income",
        "expenses": "Expenses",
        "beginning_balance": "Beginning Balance",
        "product_list": "Product List",
        "share_capital": "Share Capital",
        "payables_receivables": "Payables and Receivables",
        "equipment_purchase": "Equipment Purchase",
        "charity": "Charity",
        "investment": "Investment",
        "journal_entry": "Journal Entry",
        "general_ledger": "General Ledger",
        "trial_balance": "Trial Balance",
        "income_statement": "Income Statement",
        "balance_sheet": "Balance Sheet",
        "closing_entry": "Closing Entry",
        "product_stocking": "Product Stocking",
        "date": "Date",
        "product_name": "Product's Name",
        "initial_quantity": "Initial Quantity",
        "purchase_price": "Purchase Price",
        "total_purchase_price": "Total Purchase Price",
        "selling_price": "Selling Price",
        "save": "Save",
        "quantity_update": "Quantity Update",
        "total_price": "Total Price",
        "add": "Add",
        "quantity_addition": "Quantity Addition",
        "add_quantity": "Add Quantity",
        "sales": "Sales",
        "customer": "Customer",
        "price": "Price",
        "quantity": "Quantity",
        "payment": "Payment",
        "cash": "Cash",
        "receivable": "Receivable",
        "record": "Record",
        "sales_return": "Sales Return",
        "settlement": "Settlement",
        "transaction_date": "Transaction Date",
        "return": "Return",
        "settlement_amount": "Settlement Amount",
        "lending": "Lending",
        "borrowing": "Borrowing",
        "form_filling": "Form Filling",
        "borrower_name": "Borrower's Name",
        "nominal": "Nominal",
        "receivables_payment": "Receivables Payment",
        "debtors_list": "Debtors List",
        "debt_payment": "Debt Payment",
        "creditors_list": "Creditors List",
        "lender": "Lender",
        "option": "Option",
        "equipment": "Equipment",
        "building": "Building",
        "vehicle": "Vehicle",
        "depreciation_entry": "Depreciation Entry (End Period)",
        "price_at_purchase": "Price at Purchase",
        "useful_life": "Useful Life (years)",
        "current_year_depreciation": "Current Year Depreciation",
        "expense_entry": "Expense Entry",
        "expense": "Expense",
        "destination": "Destination",
        "type_of_investment": "Type of Investment",
        "buy": "Buy",
        "sell": "Sell",
        "investment_selling": "Investment Selling",
        "company_name": "Company's Name",
        "sell_date": "Sell Date",
        "final_value": "Final Value",
        "gain_loss": "Gain/Loss",
        "submit_update": "Submit Update",
        "paid_up_capital": "Paid-up Capital",
        "account_title": "Account Title",
        "debit": "Debit",
        "credit": "Credit",
        "total": "Total",
        "account": "Account",
        "balance": "Balance",
        "revenue": "REVENUE",
        "gross_profit": "GROSS PROFIT",
        "operating_expenses": "OPERATING EXPENSES",
        "total_expenses": "TOTAL EXPENSES",
        "other_income_expenses": "OTHER INCOME AND EXPENSES",
        "net_income": "NET INCOME",
        "assets": "ASSETS",
        "liabilities": "LIABILITIES",
        "equity": "EQUITY",
        "total_assets": "TOTAL ASSETS",
        "total_liabilities_equity": "TOTAL LIABILITIES AND EQUITY",
        "warn_no_selection": "No item selected.",
        "warn_fill_fields": "Please fill all fields correctly.",
        "success_add": "Data added successfully!",
        "success_update": "Data updated successfully!",
    },
    "id": {
        "title": "Aplikasi Akuntansi Keuangan",
        "home": "Beranda",
        "language": "Bahasa",
        "financial_statement": "LAPORAN KEUANGAN PERUSAHAAN",
        "income": "Pendapatan",
        "expenses": "Beban",
        "beginning_balance": "Saldo Awal",
        "product_list": "Daftar Produk",
        "share_capital": "Modal Saham",
        "payables_receivables": "Utang dan Piutang",
        "equipment_purchase": "Pembelian Aset Tetap",
        "charity": "Amal",
        "investment": "Investasi",
        "journal_entry": "Jurnal Umum",
        "general_ledger": "Buku Besar",
        "trial_balance": "Neraca Saldo",
        "income_statement": "Laporan Laba Rugi",
        "balance_sheet": "Laporan Posisi Keuangan (Neraca)",
        "closing_entry": "Jurnal Penutup",
        "product_stocking": "Stok Produk Awal",
        "date": "Tanggal",
        "product_name": "Nama Produk",
        "initial_quantity": "Kuantitas Awal",
        "purchase_price": "Harga Beli",
        "total_purchase_price": "Total Harga Beli",
        "selling_price": "Harga Jual",
        "save": "Simpan",
        "quantity_update": "Kuantitas Terbaru",
        "total_price": "Total Harga",
        "add": "Tambah",
        "quantity_addition": "Penambahan Kuantitas",
        "add_quantity": "Jumlah Tambahan",
        "sales": "Penjualan",
        "customer": "Pelanggan",
        "price": "Harga",
        "quantity": "Kuantitas",
        "payment": "Pembayaran",
        "cash": "Tunai",
        "receivable": "Piutang",
        "record": "Catat",
        "sales_return": "Retur Penjualan",
        "settlement": "Pelunasan",
        "transaction_date": "Tanggal Transaksi",
        "return": "Retur",
        "settlement_amount": "Jumlah Pelunasan",
        "lending": "Pemberian Pinjaman",
        "borrowing": "Penerimaan Pinjaman",
        "form_filling": "Formulir Isian",
        "borrower_name": "Nama Peminjam",
        "nominal": "Nominal",
        "receivables_payment": "Pembayaran Piutang",
        "debtors_list": "Daftar Debitur",
        "debt_payment": "Pembayaran Utang",
        "creditors_list": "Daftar Kreditur",
        "lender": "Pemberi Pinjaman",
        "option": "Pilihan",
        "equipment": "Peralatan",
        "building": "Gedung",
        "vehicle": "Kendaraan",
        "depreciation_entry": "Entri Penyusutan (Akhir Periode)",
        "price_at_purchase": "Harga Beli",
        "useful_life": "Masa Manfaat (tahun)",
        "current_year_depreciation": "Penyusutan Tahun Berjalan",
        "expense_entry": "Entri Beban",
        "expense": "Beban",
        "destination": "Tujuan",
        "type_of_investment": "Jenis Investasi",
        "buy": "Beli",
        "sell": "Jual",
        "investment_selling": "Penjualan Investasi",
        "company_name": "Nama Perusahaan",
        "sell_date": "Tanggal Jual",
        "final_value": "Nilai Akhir",
        "gain_loss": "Laba/Rugi",
        "submit_update": "Kirim Pembaruan",
        "paid_up_capital": "Modal Disetor",
        "account_title": "Nama Akun",
        "debit": "Debit",
        "credit": "Kredit",
        "total": "Total",
        "account": "Akun",
        "balance": "Saldo",
        "revenue": "PENDAPATAN",
        "gross_profit": "LABA KOTOR",
        "operating_expenses": "BEBAN OPERASIONAL",
        "total_expenses": "TOTAL BEBAN",
        "other_income_expenses": "PENDAPATAN DAN BEBAN LAIN-LAIN",
        "net_income": "LABA BERSIH",
        "assets": "ASET",
        "liabilities": "LIABILITAS",
        "equity": "EKUITAS",
        "total_assets": "TOTAL ASET",
        "total_liabilities_equity": "TOTAL LIABILITAS DAN EKUITAS",
        "warn_no_selection": "Tidak ada item yang dipilih.",
        "warn_fill_fields": "Harap isi semua kolom dengan benar.",
        "success_add": "Data berhasil ditambahkan!",
        "success_update": "Data berhasil diperbarui!",
    }
}

# Expense types (tidak ada perubahan di sini)
expense_types = {
    "en": [
        "Freight-in (Purchase Shipping Cost)", "Employee Salaries", "Sales/Marketing Salaries",
        "Sales Commission", "Advertising and Promotion", "Freight-out (Sales Shipping Cost)",
        "Building/Store/Warehouse Rent", "Electricity", "Water", "Telephone and Internet",
        "Office Stationery", "Bank Administration Fees", "Loan Interest",
        "Consultant/Accountant/Legal Fees", "Business Taxes (Property Tax, Income Tax, etc.)",
        "Transportation and Fuel", "Cleaning", "Security", "Damaged or Lost Goods",
        "Late Penalty Fees", "Business Insurance", "Employee Training and Development",
        "Software/Application Subscription Fees", "Maintenance and Repair Costs",
        "Donations or CSR (Corporate Social Responsibility)", "Office Refreshments",
        "Business Guest Entertainment", "Miscellaneous Daily Operational", "Prive"
    ],
    "id": [
        "Beban Angkut Pembelian", "Gaji Karyawan", "Gaji Pemasaran/Penjualan",
        "Komisi Penjualan", "Iklan dan Promosi", "Beban Angkut Penjualan",
        "Sewa Gedung/Toko/Gudang", "Listrik", "Air", "Telepon dan Internet",
        "Alat Tulis Kantor", "Biaya Administrasi Bank", "Bunga Pinjaman",
        "Jasa Konsultan/Akuntan/Hukum", "Pajak Usaha (PBB, PPh, dll.)",
        "Transportasi dan Bahan Bakar", "Kebersihan", "Keamanan", "Barang Rusak atau Hilang",
        "Denda Keterlambatan", "Asuransi Usaha", "Pelatihan dan Pengembangan Karyawan",
        "Langganan Perangkat Lunak/Aplikasi", "Biaya Pemeliharaan dan Perbaikan",
        "Sumbangan atau CSR", "Konsumsi Kantor", "Hiburan Tamu Bisnis",
        "Operasional Harian Lain-lain", "Prive"
    ]
}


# <<< DITAMBAHKAN: Logika untuk memuat data saat start
app_data = load_app_data(DATA_FILE)

if app_data is None:
    # Jika tidak ada file save, gunakan data default
    app_data = {
        "product_list": [],
        "journal_entries": [],
        "sales_records": [],
        "debtor_list": [],
        "creditor_list": [],
        "fixed_assets": [],
        "investments": [],
        "share_capital": 0,
        "general_ledger": defaultdict(list),
        "account_balances": defaultdict(float),
    }

# <<< DITAMBAHKAN: Mendaftarkan fungsi save untuk dijalankan otomatis saat aplikasi berhenti
atexit.register(save_app_data, app_data, DATA_FILE)
def create_journal_entry(date, description, debit_account, debit_amount, credit_account, credit_amount):
    """Membuat entri jurnal dan memperbarui buku besar serta saldo akun dengan andal."""
    entry = {
        "date": date,
        "description": description,
        "debit_account": debit_account,
        "debit_amount": float(debit_amount),
        "credit_account": credit_account,
        "credit_amount": float(credit_amount)
    }
    app_data["journal_entries"].append(entry)

    # Update buku besar
    app_data["general_ledger"][debit_account].append({"date": date, "description": description, "debit": float(debit_amount), "credit": 0})
    app_data["general_ledger"][credit_account].append({"date": date, "description": description, "debit": 0, "credit": float(credit_amount)})

    # Daftar akun yang saldo normalnya ada di sisi DEBIT
    debit_side_accounts = [
        "Asset", "Cash", "Inventory", "Accounts Receivable", "Equipment", 
        "Building", "Vehicle", "Investment", "Expense", "Cost of Goods Sold", 
        "Prive", "Charity", "Loss", "Accumulated Depreciation"
    ]
    
    # --- LOGIKA KALKULASI SALDO YANG SUDAH DIPERBAIKI ---

    # 1. Proses Akun Sisi Debit Jurnal
    if any(keyword in debit_account for keyword in debit_side_accounts):
        # Jika akun normal DEBIT di-debit, saldo BERTAMBAH.
        app_data["account_balances"][debit_account] += float(debit_amount)
    else: # Ini adalah akun normal KREDIT (Pendapatan, Utang, Modal)
        # Jika akun normal KREDIT di-debit, saldo (kredit) BERKURANG.
        # Contoh: Retur penjualan mengurangi saldo Sales Revenue.
        # Saldo kredit kita negatif, jadi untuk menguranginya kita TAMBAH.
        app_data["account_balances"][debit_account] += float(debit_amount) # <<< INI PERBAIKANNYA

    # 2. Proses Akun Sisi Kredit Jurnal
    if any(keyword in credit_account for keyword in debit_side_accounts):
        # Jika akun normal DEBIT di-kredit, saldo BERKURANG.
        # Contoh: Kas berkurang saat bayar beban.
        app_data["account_balances"][credit_account] -= float(credit_amount)
    else: # Ini adalah akun normal KREDIT
        # Jika akun normal KREDIT di-kredit, saldo (kredit) BERTAMBAH.
        # Contoh: Penjualan menambah saldo Sales Revenue.
        app_data["account_balances"][credit_account] -= float(credit_amount)

    return entry


def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# ... Sisa kode Anda dari baris 248 hingga akhir (TIDAK ADA PERUBAHAN) ...
# ... Cukup salin dan tempel semua fungsi Anda yang ada di sini ...
# ... mulai dari 'def create_journal_entry(...)' sampai 'if __name__ == '__main__': ...

# --- Tambahkan kode ini di file app.py ---

# GANTI FUNGSI create_closing_entry YANG SEBELUMNYA DENGAN VERSI FINAL INI

@app.route('/create_closing_entry', methods=['POST'])
def create_closing_entry():
    """Menangani seluruh proses jurnal penutup dengan identifikasi akun yang lengkap."""
    try:
        closing_date = get_current_date()
        generated_entries = []
        revenue_accounts = {}
        expense_accounts = {}

        # --- LOGIKA IDENTIFIKASI AKUN YANG DISEMPURNAKAN ---
        # Daftar kata kunci yang lebih lengkap
        revenue_keywords = ["Revenue", "Sales", "Gain", "Other Income"]
        expense_keywords = ["Expense", "Cost of Goods Sold", "Loss", "Prive"]

        for account, balance in app_data["account_balances"].items():
            balance = float(balance or 0)
            if balance == 0:
                continue

            # Cek apakah akun ini termasuk akun pendapatan
            if any(keyword in account for keyword in revenue_keywords):
                if balance < 0:  # Saldo normal pendapatan adalah kredit (negatif di sistem)
                    revenue_accounts[account] = abs(balance)
            
            # Cek apakah akun ini termasuk akun beban
            elif any(keyword in account for keyword in expense_keywords):
                if balance > 0:  # Saldo normal beban adalah debit (positif di sistem)
                    expense_accounts[account] = balance

        # --- Proses Jurnal Penutup (tidak ada perubahan di sini, tapi sekarang datanya benar) ---
        total_revenue = sum(revenue_accounts.values())
        total_expenses = sum(expense_accounts.values())
        net_income = total_revenue - total_expenses

        # 1. Menutup Akun Pendapatan
        for account, balance in revenue_accounts.items():
            entry = create_journal_entry(closing_date, "To close revenue accounts", account, balance, "Income Summary", balance)
            generated_entries.append(entry)

        # 2. Menutup Akun Beban
        for account, balance in expense_accounts.items():
            entry = create_journal_entry(closing_date, "To close expense accounts", "Income Summary", balance, account, balance)
            generated_entries.append(entry)
        
        # 3. Menutup Akun Ikhtisar Laba Rugi ke Laba Ditahan
        if net_income != 0:
            if net_income > 0: # Laba
                entry = create_journal_entry(closing_date, "To transfer net income to Retained Earnings", "Income Summary", net_income, "Retained Earnings", net_income)
            else: # Rugi
                entry = create_journal_entry(closing_date, "To transfer net loss to Retained Earnings", "Retained Earnings", abs(net_income), "Income Summary", abs(net_income))
            generated_entries.append(entry)

        return jsonify({"success": True, "message": "Closing entries created successfully.", "closing_entries": generated_entries})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
        
@app.route('/')
def home():
    language = session.get('language', 'id')
    return render_template('index.html', translations=translations[language], language=language)

# app.py
# ... (kode Anda yang lain)

# app.py

# ... (Pastikan semua import yang ada tetap di atas)
import math

# ... (Di bawah definisi app_data, pastikan ada key baru untuk PPE)
if 'ppe_assets' not in app_data:
    app_data['ppe_assets'] = []
if 'depreciation_history' not in app_data:
    app_data['depreciation_history'] = []

# --- Endpoint untuk Mengelola Aset Tetap (PPE) ---

@app.route('/get_ppe_assets', methods=['GET'])
def get_ppe_assets():
    """Mengirim daftar semua aset tetap dengan perhitungan nilai buku terkini."""
    current_year = datetime.datetime.now().year
    
    # Hitung nilai buku untuk setiap aset sebelum mengirim
    for asset in app_data['ppe_assets']:
        purchase_year = datetime.datetime.strptime(asset['purchase_date'], '%Y-%m-%d').year
        
        # Cari total depresiasi yang sudah dicatat untuk aset ini
        total_recorded_depreciation = sum(
            d['amount'] for d in app_data.get('depreciation_history', []) 
            if d['asset_id'] == asset['id']
        )
        asset['accumulated_depreciation'] = total_recorded_depreciation
        asset['book_value'] = float(asset['cost']) - total_recorded_depreciation

    return jsonify(app_data['ppe_assets'])

# app.py

# app.py

# app.py

@app.route('/add_ppe', methods=['POST'])
def add_ppe():
    """Menambah atau mengedit aset tetap."""
    try:
        data = request.json
        asset_id = data.get('id')

        asset_data = {
            'name': data['name'],
            'category': data['category'],
            'purchase_date': data['purchase_date'],
            'cost': float(data['cost']),
            'useful_life': int(data['useful_life']),
            'salvage_value': float(data['salvage_value']),
            'depreciation_method': data['depreciation_method'],
            'uop_details': data.get('uop_details', {})
        }

        if asset_id:
            # Logika untuk Edit (jika Anda kembangkan nanti)
            # ...
            pass
        else: # Logika untuk Tambah Baru
            asset_data['id'] = int(time.time() * 1000)
            app_data['ppe_assets'].append(asset_data)
            
            create_journal_entry(
                date=asset_data['purchase_date'],
                description=f"Pembelian Aset: {asset_data['name']}",
                debit_account=f"PPE - {asset_data['category']}",
                debit_amount=asset_data['cost'],
                credit_account="Cash",
                credit_amount=asset_data['cost']
            )
            
            # Perintah penting untuk menyimpan data ke file SECARA LANGSUNG
            save_app_data(app_data, DATA_FILE)
            
            return jsonify({"success": True, "message": "Aset berhasil ditambahkan!"})

    except Exception as e:
        return jsonify({"success": False, "message": f"Server Error: {str(e)}"}), 400
        
@app.route('/get_depreciation_schedule/<int:asset_id>', methods=['GET'])
def get_depreciation_schedule(asset_id):
    """Menghitung dan mengembalikan jadwal depresiasi lengkap untuk satu aset."""
    asset = next((a for a in app_data['ppe_assets'] if a['id'] == asset_id), None)
    if not asset:
        return jsonify({"success": False, "message": "Aset tidak ditemukan"}), 404

    schedule = []
    book_value = float(asset['cost'])
    cost = float(asset['cost'])
    salvage = float(asset['salvage_value'])
    life = int(asset['useful_life'])
    
    # Ambil riwayat depresiasi yang sudah dicatat
    recorded_depreciation = {d['period']: d['amount'] for d in app_data.get('depreciation_history', []) if d['asset_id'] == asset_id}

    for year_num in range(1, life + 1):
        depreciation_expense = 0
        current_period = datetime.datetime.strptime(asset['purchase_date'], '%Y-%m-%d').year + year_num -1

        if book_value <= salvage:
             schedule.append({
                "period": current_period,
                "beginning_book_value": book_value,
                "depreciation_expense": 0,
                "accumulated_depreciation": cost - book_value,
                "ending_book_value": book_value,
                "status": "Fully Depreciated"
            })
             continue


        # --- LOGIKA PERHITUNGAN DEPRESIASI ---
        if asset['depreciation_method'] == 'straight_line':
            depreciation_expense = (cost - salvage) / life
        
        elif asset['depreciation_method'] == 'double_declining':
            depreciation_expense = (book_value * 2) / life
        
        # Logika untuk UoP butuh input `units_this_period`
        # Untuk jadwal, kita bisa asumsikan rata-rata atau tampilkan 0
        # elif asset['depreciation_method'] == 'uop':
        #     # Membutuhkan data penggunaan aktual per tahun untuk perhitungan akurat
        #     depreciation_expense = 0 # Placeholder

        # Pastikan depresiasi tidak membuat nilai buku di bawah nilai residu
        if (book_value - depreciation_expense) < salvage:
            depreciation_expense = book_value - salvage

        accumulated_depreciation = (cost - book_value) + depreciation_expense
        ending_book_value = book_value - depreciation_expense

        status = "Recorded" if current_period in recorded_depreciation else "Not Recorded"

        schedule.append({
            "period": current_period,
            "beginning_book_value": book_value,
            "depreciation_expense": depreciation_expense,
            "accumulated_depreciation": accumulated_depreciation,
            "ending_book_value": ending_book_value,
            "status": status
        })
        
        book_value = ending_book_value # Update nilai buku untuk tahun berikutnya

    return jsonify({"success": True, "schedule": schedule, "asset": asset})

@app.route('/preview_period_depreciation', methods=['POST'])
def preview_period_depreciation():
    """Menghitung dan mengembalikan preview aset yang akan didepresiasi tanpa mencatatnya."""
    try:
        data = request.json
        period = int(data['period'])
        
        assets_to_depreciate = []
        
        for asset in app_data['ppe_assets']:
            purchase_year = datetime.datetime.strptime(asset['purchase_date'], '%Y-%m-%d').year
            if period < purchase_year or (period >= purchase_year + asset['useful_life']):
                continue

            already_recorded = any(
                d['asset_id'] == asset['id'] and d['period'] == period 
                for d in app_data.get('depreciation_history', [])
            )
            if already_recorded:
                continue
                
            book_value = float(asset['cost']) - sum(d['amount'] for d in app_data.get('depreciation_history', []) if d['asset_id'] == asset['id'])
            
            depreciation_expense = 0
            if asset['depreciation_method'] == 'straight_line':
                depreciation_expense = (float(asset['cost']) - float(asset['salvage_value'])) / int(asset['useful_life'])
            elif asset['depreciation_method'] == 'double_declining':
                depreciation_expense = (book_value * 2) / int(asset['useful_life'])
            
            if (book_value - depreciation_expense) < float(asset['salvage_value']):
                depreciation_expense = book_value - float(asset['salvage_value'])
                
            if depreciation_expense > 0:
                assets_to_depreciate.append({
                    "id": asset['id'],
                    "name": asset['name'],
                    "category": asset['category'],
                    "depreciation_expense": depreciation_expense
                })

        return jsonify({"success": True, "preview_data": assets_to_depreciate})
    except Exception as e:
        print(f"Error in preview: {e}")
        return jsonify({"success": False, "message": f"Server Error: {str(e)}"}), 500

@app.route('/record_period_depreciation', methods=['POST'])
def record_period_depreciation():
    """Mencatat beban depresiasi untuk semua aset pada periode yang dipilih."""
    data = request.json
    period = int(data['period']) # cth: 2024
    
    # Ambil jadwal depresiasi untuk semua aset pada periode ini
    total_depreciation_by_category = defaultdict(float)
    journal_entries_preview = []
    
    for asset in app_data['ppe_assets']:
        purchase_year = datetime.datetime.strptime(asset['purchase_date'], '%Y-%m-%d').year
        if period < purchase_year or (period >= purchase_year + asset['useful_life']):
            continue # Lewati jika aset belum dibeli atau sudah habis masa manfaat

        # Cek apakah sudah pernah dicatat untuk periode ini
        already_recorded = any(
            d['asset_id'] == asset['id'] and d['period'] == period 
            for d in app_data.get('depreciation_history', [])
        )
        if already_recorded:
            continue
            
        # Hitung depresiasi untuk periode ini
        # Ini adalah simplifikasi, idealnya memanggil fungsi yang sama dengan get_depreciation_schedule
        book_value = float(asset['cost']) - sum(d['amount'] for d in app_data.get('depreciation_history', []) if d['asset_id'] == asset['id'])
        
        depreciation_expense = 0
        if asset['depreciation_method'] == 'straight_line':
            depreciation_expense = (float(asset['cost']) - float(asset['salvage_value'])) / int(asset['useful_life'])
        elif asset['depreciation_method'] == 'double_declining':
            depreciation_expense = (book_value * 2) / int(asset['useful_life'])
        
        if (book_value - depreciation_expense) < float(asset['salvage_value']):
            depreciation_expense = book_value - float(asset['salvage_value'])
            
        if depreciation_expense > 0:
            total_depreciation_by_category[asset['category']] += depreciation_expense
            # Simpan riwayat pencatatan
            app_data['depreciation_history'].append({
                "id": int(time.time() * 1000),
                "asset_id": asset['id'],
                "asset_name": asset['name'],
                "period": period,
                "amount": depreciation_expense,
                "date_recorded": get_current_date()
            })

    # Buat jurnal entri gabungan per kategori
    for category, total_amount in total_depreciation_by_category.items():
        if total_amount > 0:
            entry = create_journal_entry(
                date=f"{period}-12-31", # Selalu di akhir tahun
                description=f"Pencatatan Beban Depresiasi Thn. {period} - {category}",
                debit_account=f"Depreciation Expense - {category}",
                debit_amount=total_amount,
                credit_account=f"Accumulated Depreciation - {category}",
                credit_amount=total_amount
            )
            journal_entries_preview.append(entry)
            
    if not journal_entries_preview:
        return jsonify({"success": False, "message": "Tidak ada depresiasi untuk dicatat pada periode ini."})

    return jsonify({"success": True, "message": f"Depresiasi untuk periode {period} berhasil dicatat!", "entries": journal_entries_preview})

@app.route('/get_depreciation_history')
def get_depreciation_history():
    return jsonify(app_data.get('depreciation_history', []))

@app.route('/setup', methods=['POST'])
def handle_setup():
    """Menerima dan menyimpan data penyiapan awal."""
    try:
        data = request.json
        # Simpan nama perusahaan dan info mata uang ke dalam data aplikasi
        app_data['company_name'] = data.get('company_name', 'My Company')
        app_data['currency_info'] = data.get('currency_info', {'code': 'IDR', 'symbol': 'Rp', 'flag': 'id'})
        
        # Fungsi save_app_data() akan dipanggil otomatis saat aplikasi berhenti,
        # jadi data ini akan tersimpan permanen di financial_data.json
        
        return jsonify({'success': True, 'message': 'Setup data saved successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ... (sisa kode Anda)

# <<< DITAMBAHKAN: Endpoint untuk menyimpan data secara manual
@app.route('/save_data', methods=['POST'])
def manual_save():
    if save_app_data(app_data, DATA_FILE):
        return jsonify({"success": True, "message": "Data saved successfully!"})
    else:
        return jsonify({"success": False, "message": "Failed to save data."}), 500

@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form.get('language', 'id')
    session['language'] = language
    return jsonify({"success": True, "language": language})

@app.route('/get_translations')
def get_translations():
    language = session.get('language', 'id')
    return jsonify(translations[language])

@app.route('/get_expense_types')
def get_expense_types():
    language = session.get('language', 'id')
    return jsonify(expense_types[language])

@app.route('/product_stocking', methods=['POST'])
def product_stocking():
    try:
        data = request.json
        
        product = {
            "date": data.get('date', get_current_date()),
            "name": data['product_name'],
            "initial_quantity": int(data['initial_quantity']),
            "current_quantity": int(data['initial_quantity']),
            "purchase_price": float(data['purchase_price']),
            "selling_price": float(data['selling_price']),
            "total_purchase_price": float(data['purchase_price']) * int(data['initial_quantity'])
        }
        
        app_data["product_list"].append(product)
        
        # Create journal entry for inventory purchase
        create_journal_entry(
            product["date"],
            f"Purchase of {product['name']}",
            "Inventory",
            product["total_purchase_price"],
            "Cash",
            product["total_purchase_price"]
        )
        
        return jsonify({"success": True, "message": "Product added successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/get_products')
def get_products():
    return jsonify(app_data["product_list"])

@app.route('/add_quantity', methods=['POST'])
def add_quantity():
    try:
        data = request.json
        product_name = data['product_name']
        additional_quantity = int(data['additional_quantity'])
        
        # Find and update product
        for product in app_data["product_list"]:
            if product['name'] == product_name:
                product['current_quantity'] += additional_quantity
                
                # Create journal entry for additional inventory
                total_cost = additional_quantity * product['purchase_price']
                create_journal_entry(
                    get_current_date(),
                    f"Additional inventory for {product_name}",
                    "Inventory",
                    total_cost,
                    "Cash",
                    total_cost
                )
                break
        
        return jsonify({"success": True, "message": "Quantity updated successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/record_sale', methods=['POST'])
def record_sale():
    try:
        data = request.json
        sale_id = int(time.time() * 1000) # Membuat ID unik berdasarkan timestamp
        sale = {
            "id": sale_id, # <<< Tambahkan ID
            "date": data.get('date', get_current_date()),
            "customer": data['customer'],
            "product_name": data['product_name'],
            "quantity": int(data['quantity']),
            "price": float(data['price']),
            "total": float(data['price']) * int(data['quantity']),
            "payment_type": data['payment_type']
        }
        app_data["sales_records"].append(sale)

        cost_of_goods_sold = 0
        for product in app_data["product_list"]:
            if product['name'] == sale['product_name']:
                if product['current_quantity'] < sale['quantity']:
                    return jsonify({"success": False, "message": "Not enough stock for this sale."}), 400
                product['current_quantity'] -= sale['quantity']
                cost_of_goods_sold = product['purchase_price'] * sale['quantity']
                break
        
        if sale['payment_type'] == 'cash':
            create_journal_entry(
                sale["date"], f"Sale to {sale['customer']}",
                "Cash", sale["total"], "Sales Revenue", sale["total"]
            )
        else:  # receivable
            receivable_account = f"Accounts Receivable - {sale['customer']}"
            create_journal_entry(
                sale["date"], f"Sale to {sale['customer']} (on account)",
                receivable_account, sale["total"], "Sales Revenue", sale["total"]
            )
            # Menambahkan piutang ke daftar debitur dengan ID unik
            app_data["debtor_list"].append({
                "id": sale_id, # <<< Tambahkan ID
                "name": sale['customer'],
                "amount": sale["total"],
                "date": sale["date"],
                "type": "sales",
                "description": f"Sale of {sale['product_name']} ({sale['quantity']} pcs)"
            })

        if cost_of_goods_sold > 0:
            create_journal_entry(
                sale["date"], f"Cost of goods sold for sale to {sale['customer']}",
                "Cost of Goods Sold", cost_of_goods_sold, "Inventory", cost_of_goods_sold
            )
        
        return jsonify({"success": True, "message": "Sale recorded successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

# app.py

# Route untuk memproses pembayaran piutang penjualan
@app.route('/record_sales_receivable_payment', methods=['POST'])
def record_sales_receivable_payment():
    try:
        data = request.json
        receivable_id = int(data['receivable_id'])
        payment_amount = float(data['payment_amount'])
        date = get_current_date()

        # Cari piutang yang sesuai di dalam debtor_list
        receivable_to_pay = None
        for debtor in app_data["debtor_list"]:
            if debtor.get("id") == receivable_id:
                receivable_to_pay = debtor
                break
        
        if not receivable_to_pay:
            return jsonify({"success": False, "message": "Receivable not found."}), 404

        if payment_amount > receivable_to_pay['amount']:
            return jsonify({"success": False, "message": "Payment amount exceeds receivable balance."}), 400

        # Buat Jurnal: Debit Kas, Kredit Piutang Usaha
        receivable_account = f"Accounts Receivable - {receivable_to_pay['name']}"
        create_journal_entry(
            date,
            f"Payment from {receivable_to_pay['name']} for sale",
            "Cash",
            payment_amount,
            receivable_account,
            payment_amount
        )

        # Kurangi saldo piutang
        receivable_to_pay['amount'] -= payment_amount
        
        return jsonify({"success": True, "message": "Payment recorded successfully."})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/get_sales')
def get_sales():
    return jsonify(app_data["sales_records"])

@app.route('/get_debtors')
def get_debtors():
    return jsonify(app_data["debtor_list"])

@app.route('/get_creditors')
def get_creditors():
    return jsonify(app_data["creditor_list"])

# Ganti fungsi record_expense yang lama dengan yang ini di app.py

@app.route('/record_expense', methods=['POST'])
def record_expense():
    try:
        data = request.json
        
        expense_amount = float(data['amount'])
        expense_type = data['expense_type']
        destination = data.get('destination', '')

        # Logika untuk menentukan nama akun debit
        debit_account_name = ""
        if expense_type == "Prive":
            debit_account_name = "Prive"
        else:
            debit_account_name = f"{expense_type} Expense"
        
        create_journal_entry(
            get_current_date(),
            f"{expense_type} - {destination}",
            debit_account_name,  # Gunakan nama akun yang sudah ditentukan
            expense_amount,
            "Cash",
            expense_amount
        )
        
        return jsonify({"success": True, "message": "Expense recorded successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/record_charity', methods=['POST'])
def record_charity():
    try:
        data = request.json
        
        charity_amount = float(data['amount'])
        destination = data.get('destination', '')
        
        create_journal_entry(
            get_current_date(),
            f"Charity donation - {destination}",
            "Charity",
            charity_amount,
            "Cash",
            charity_amount
        )
        
        return jsonify({"success": True, "message": "Charity recorded successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/record_investment', methods=['POST'])
def record_investment():
    try:
        data = request.json
        
        investment_amount = float(data['amount'])
        investment_type = data['investment_type']
        company_name = data.get('company_name', '')
        
        investment = {
            "date": get_current_date(),
            "type": investment_type,
            "company": company_name,
            "amount": investment_amount,
            "current_value": investment_amount
        }
        
        app_data["investments"].append(investment)
        
        create_journal_entry(
            get_current_date(),
            f"Investment in {company_name} - {investment_type}",
            "Investment",
            investment_amount,
            "Cash",
            investment_amount
        )
        
        return jsonify({"success": True, "message": "Investment recorded successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/sell_investment', methods=['POST'])
def sell_investment():
    try:
        data = request.json
        
        investment_id = int(data['investment_id'])
        sell_amount = float(data['sell_amount'])
        
        if investment_id < len(app_data["investments"]):
            investment = app_data["investments"][investment_id]
            original_amount = investment["amount"]
            gain_loss = sell_amount - original_amount
            
            # Record sale
            create_journal_entry(
                get_current_date(),
                f"Sale of investment in {investment['company']}",
                "Cash",
                sell_amount,
                "Investment",
                original_amount
            )
            
            # Record gain or loss
            if gain_loss > 0:
                create_journal_entry(
                    get_current_date(),
                    f"Gain on sale of investment",
                    "Cash",
                    0,
                    "Investment Gain",
                    gain_loss
                )
            elif gain_loss < 0:
                create_journal_entry(
                    get_current_date(),
                    f"Loss on sale of investment",
                    "Investment Loss",
                    abs(gain_loss),
                    "Cash",
                    0
                )
            
            # Remove investment from list
            app_data["investments"].pop(investment_id)
            
            return jsonify({"success": True, "message": "Investment sold successfully!", "gain_loss": gain_loss})
        else:
            return jsonify({"success": False, "message": "Investment not found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/record_receivable_payment', methods=['POST'])
def record_receivable_payment():
    try:
        data = request.json
        
        debtor_name = data['debtor_name']
        payment_amount = float(data['payment_amount'])
        
        # Find and update debtor
        for i, debtor in enumerate(app_data["debtor_list"]):
            if debtor['name'] == debtor_name:
                if payment_amount <= debtor['amount']:
                    create_journal_entry(
                        get_current_date(),
                        f"Payment received from {debtor_name}",
                        "Cash",
                        payment_amount,
                        "Accounts Receivable",
                        payment_amount
                    )
                    
                    debtor['amount'] -= payment_amount
                    if debtor['amount'] == 0:
                        app_data["debtor_list"].pop(i)
                    
                    return jsonify({"success": True, "message": "Receivable payment recorded successfully!"})
                else:
                    return jsonify({"success": False, "message": "Payment amount exceeds receivable balance"}), 400
        
        return jsonify({"success": False, "message": "Debtor not found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/record_payable_payment', methods=['POST'])
def record_payable_payment():
    try:
        data = request.json
        
        creditor_name = data['creditor_name']
        payment_amount = float(data['payment_amount'])
        
        # Find and update creditor
        for i, creditor in enumerate(app_data["creditor_list"]):
            if creditor['name'] == creditor_name:
                if payment_amount <= creditor['amount']:
                    create_journal_entry(
                        get_current_date(),
                        f"Payment made to {creditor_name}",
                        "Accounts Payable",
                        payment_amount,
                        "Cash",
                        payment_amount
                    )
                    
                    creditor['amount'] -= payment_amount
                    if creditor['amount'] == 0:
                        app_data["creditor_list"].pop(i)
                    
                    return jsonify({"success": True, "message": "Payable payment recorded successfully!"})
                else:
                    return jsonify({"success": False, "message": "Payment amount exceeds payable balance"}), 400
        
        return jsonify({"success": False, "message": "Creditor not found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/create_receivable', methods=['POST'])
def create_receivable():
    try:
        data = request.json
        
        debtor_name = data['debtor_name']
        amount = float(data['amount'])
        description = data.get('description', 'Other receivable')
        
        receivable = {
            "name": debtor_name,
            "amount": amount,
            "date": get_current_date(),
            "description": description
        }
        
        app_data["debtor_list"].append(receivable)
        
        create_journal_entry(
            get_current_date(),
            f"Receivable from {debtor_name} - {description}",
            "Accounts Receivable",
            amount,
            "Other Income",
            amount
        )
        
        return jsonify({"success": True, "message": "Receivable created successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/create_payable', methods=['POST'])
def create_payable():
    try:
        data = request.json
        
        creditor_name = data['creditor_name']
        amount = float(data['amount'])
        description = data.get('description', 'Other payable')
        
        payable = {
            "name": creditor_name,
            "amount": amount,
            "date": get_current_date(),
            "description": description
        }
        
        app_data["creditor_list"].append(payable)
        
        create_journal_entry(
            get_current_date(),
            f"Payable to {creditor_name} - {description}",
            "Equipment" if "equipment" in description.lower() else "Other Expense",
            amount,
            "Accounts Payable",
            amount
        )
        
        return jsonify({"success": True, "message": "Payable created successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/get_investments')
def get_investments():
    return jsonify(app_data["investments"])

@app.route('/set_share_capital', methods=['POST'])
def set_share_capital():
    try:
        data = request.json
        capital_amount = float(data['amount'])
        
        app_data["share_capital"] = capital_amount
        
        create_journal_entry(
            get_current_date(),
            "Initial share capital investment",
            "Cash",
            capital_amount,
            "Share Capital - Ordinary",
            capital_amount
        )
        
        return jsonify({"success": True, "message": "Share capital set successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/get_journal_entries')
def get_journal_entries():
    return jsonify(app_data["journal_entries"])

@app.route('/get_general_ledger')
def get_general_ledger():
    consolidated_ledger = defaultdict(lambda: {"entries": [], "balance": 0.0})

    for account, entries in app_data["general_ledger"].items():
        consolidated_key = account # Default key
        
        # Logika Konsolidasi
        if account.startswith("Accounts Receivable"):
            consolidated_key = "Accounts Receivable"
        elif account.startswith("Accounts Payable"):
            consolidated_key = "Accounts Payable"
        # JANGAN GABUNGKAN LOANS RECEIVABLE/PAYABLE KE DALAMNYA, BIARKAN SEBAGAI AKUN TERPISAH
        # elif account.startswith("Loans Receivable"):
        #     consolidated_key = "Loans Receivable"
        # elif account.startswith("Loans Payable"):
        #     consolidated_key = "Loans Payable"

        consolidated_ledger[consolidated_key]["entries"].extend(entries)
        
        balance = app_data["account_balances"].get(account, 0)
        consolidated_ledger[consolidated_key]["balance"] += balance

    final_ledger_data = {}
    for account, data in consolidated_ledger.items():
        if data["entries"]:
            sorted_entries = sorted(data["entries"], key=lambda x: x.get('date', '1970-01-01'))
            data["entries"] = sorted_entries
            final_ledger_data[account] = data

    return jsonify(final_ledger_data)

@app.route('/get_trial_balance')
def get_trial_balance():
    # Define all account categories with specific accounts
    all_accounts = {
        "assets": [
            "Cash", "Inventory", "Accounts Receivable", "Charity", "Equipment", 
            "Building", "Vehicle", "Accumulated Depreciation - Equipment", 
            "Accumulated Depreciation - Building", "Accumulated Depreciation - Vehicle", "Investment"
        ],
        "liabilities": ["Accounts Payable"],
        "equity": ["Share Capital - Ordinary", "Prive"]
    }
    
    trial_balance = []
    total_debit = 0
    total_credit = 0
    
    # Process all predefined accounts
    for category, accounts in all_accounts.items():
        for account in accounts:
            balance = app_data["account_balances"].get(account, 0)
            
            # Determine normal balance side for each account type
            if category == "assets":
                # Assets have normal debit balance (except accumulated depreciation which is credit)
                if "Accumulated Depreciation" in account:
                    # Accumulated depreciation accounts have credit normal balance
                    trial_balance.append({
                        "account": account,
                        "debit": 0,
                        "credit": abs(balance) if balance != 0 else 0
                    })
                    if balance != 0:
                        total_credit += abs(balance)
                else:
                    # Regular assets
                    if balance >= 0:
                        trial_balance.append({
                            "account": account,
                            "debit": balance,
                            "credit": 0
                        })
                        total_debit += balance
                    else:
                        trial_balance.append({
                            "account": account,
                            "debit": 0,
                            "credit": abs(balance)
                        })
                        total_credit += abs(balance)
            
            elif category == "liabilities":
                # Liabilities have normal credit balance
                trial_balance.append({
                    "account": account,
                    "debit": 0,
                    "credit": abs(balance) if balance != 0 else 0
                })
                if balance != 0:
                    total_credit += abs(balance)
            
            elif category == "equity":
                # Equity has normal credit balance (except Prive which is debit)
                if account == "Prive":
                    trial_balance.append({
                        "account": account,
                        "debit": abs(balance) if balance != 0 else 0,
                        "credit": 0
                    })
                    if balance != 0:
                        total_debit += abs(balance)
                else:
                    # Share Capital
                    trial_balance.append({
                        "account": account,
                        "debit": 0,
                        "credit": abs(balance) if balance != 0 else 0
                    })
                    if balance != 0:
                        total_credit += abs(balance)
    
    # Add any other accounts that exist in the system but not in our predefined list
    for account, balance in app_data["account_balances"].items():
        # Check if this account is already included
        account_exists = False
        for category_accounts in all_accounts.values():
            if account in category_accounts:
                account_exists = True
                break
        
        if not account_exists and balance != 0:
            if balance > 0:
                trial_balance.append({
                    "account": account,
                    "debit": balance,
                    "credit": 0
                })
                total_debit += balance
            else:
                trial_balance.append({
                    "account": account,
                    "debit": 0,
                    "credit": abs(balance)
                })
                total_credit += abs(balance)
    
    return jsonify({
        "accounts": trial_balance,
        "total_debit": total_debit,
        "total_credit": total_credit
    })

# GANTI SELURUH FUNGSI get_income_statement ANDA DENGAN VERSI DI BAWAH INI

@app.route('/get_income_statement')
def get_income_statement():
    revenue_details = {}
    operating_expense_details = {}
    other_income_and_expense_details = {}
    
    # Ambil saldo HPP secara spesifik
    cogs_balance = abs(app_data["account_balances"].get("Cost of Goods Sold", 0))

    for account, balance in app_data["account_balances"].items():
        balance_val = abs(float(balance or 0))
        if balance_val == 0 or account == "Cost of Goods Sold" or account.startswith("Prive"):
            continue

        if any(k in account for k in ["Expense", "Loss"]):
            if any(k in account for k in ["Loss"]):
                other_income_and_expense_details[account] = -balance_val
            else:
                operating_expense_details[account] = balance_val
        elif any(k in account for k in ["Revenue", "Sales", "Gain"]):
            if any(k in account for k in ["Gain"]):
                other_income_and_expense_details[account] = balance_val
            else:
                revenue_details[account] = balance_val

    # Kalkulasi Laba Rugi dengan Laba Kotor
    total_revenue = sum(revenue_details.values())
    gross_profit = total_revenue - cogs_balance
    total_operating_expenses = sum(operating_expense_details.values())
    operating_income = gross_profit - total_operating_expenses
    total_other_income_and_expenses = sum(other_income_and_expense_details.values())
    net_income = operating_income + total_other_income_and_expenses
    
    return jsonify({
        "revenue_details": revenue_details,
        "cogs": cogs_balance,
        "gross_profit": gross_profit,
        "operating_expense_details": operating_expense_details,
        "other_income_and_expense_details": other_income_and_expense_details,
        "total_revenue": total_revenue,
        "total_operating_expenses": total_operating_expenses,
        "total_other_income_and_expenses": total_other_income_and_expenses,
        "operating_income": operating_income,
        "net_income": net_income
    })
    
# GANTI FUNGSI LAMA get_balance_sheet DENGAN YANG INI

@app.route('/get_balance_sheet')
def get_balance_sheet():
    # Tahap 1: Klasifikasi Akun (Sama seperti sebelumnya)
    asset_accounts = {}
    liability_accounts = {}
    equity_accounts = {}

    income_statement_data = get_income_statement().get_json()
    net_income_for_period = income_statement_data.get('net_income', 0)

    for account, balance in app_data["account_balances"].items():
        if any(k in account for k in ["Revenue", "Sales", "Gain", "Expense", "Loss", "Cost of Goods Sold", "Income Summary"]):
            continue
        
        if any(acc_type in account for acc_type in ["Cash", "Inventory", "Accounts Receivable", "Charity", "Equipment", "Building", "Vehicle", "Investment", "Accumulated Depreciation"]):
            asset_accounts[account] = balance
        elif "Payable" in account:
            liability_accounts[account] = balance
        elif any(acc_type in account for acc_type in ["Share Capital", "Prive", "Retained Earnings"]):
            equity_accounts[account] = balance

    # Tahap 2: Hitung Total (Sama seperti sebelumnya, menggunakan data rinci)
    total_assets = 0
    for account_name, balance_val in asset_accounts.items():
        if "Accumulated Depreciation" in account_name:
            total_assets += balance_val
        else:
            total_assets += balance_val

    total_liabilities = abs(sum(liability_accounts.values()))
    
    share_capital = abs(equity_accounts.get("Share Capital - Ordinary", 0))
    retained_earnings_balance = equity_accounts.get("Retained Earnings", 0)
    prive = abs(equity_accounts.get("Prive", 0))
    total_equity = share_capital + retained_earnings_balance + net_income_for_period - prive
    total_liabilities_equity = total_liabilities + total_equity

    # --- TAHAP 3: KONSOLIDASI DATA UNTUK TAMPILAN (INI BAGIAN BARUNYA) ---
    consolidated_asset_accounts = defaultdict(float)
    for account, balance in asset_accounts.items():
        if 'Accounts Receivable' in account:
            consolidated_asset_accounts['Accounts Receivable'] += balance
        # Tambahkan logika serupa untuk akun lain jika perlu dikonsolidasi
        # Contoh: elif 'Inventory' in account: consolidated_asset_accounts['Inventory'] += balance
        else:
            consolidated_asset_accounts[account] = balance
            
    consolidated_liability_accounts = defaultdict(float)
    for account, balance in liability_accounts.items():
        if 'Accounts Payable' in account:
            consolidated_liability_accounts['Accounts Payable'] += balance
        else:
            consolidated_liability_accounts[account] = balance
    
    # Akun Ekuitas biasanya sudah unik, tidak perlu konsolidasi
    if net_income_for_period != 0:
        equity_accounts["Retained Earnings"] = net_income_for_period

    # Tahap 4: Kirim data yang SUDAH DIKONSOLIDASI ke frontend
    return jsonify({
        # Mengirim akun yang sudah digabung
        "asset_accounts": consolidated_asset_accounts,
        "liability_accounts": consolidated_liability_accounts,
        "equity_accounts": equity_accounts,
        # Total tetap sama, tidak berubah
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "total_liabilities_equity": total_liabilities_equity
    })

@app.route('/record_lending', methods=['POST'])
def record_lending():
    try:
        data = request.json
        borrower_name = data['borrower_name']
        amount = float(data['amount'])
        description = data.get('description', 'Loan Given')
        date = get_current_date()
        
        # Menggunakan Akun: Accounts Receivable - Nama Peminjam
        create_journal_entry(
            date=date,
            description=f"Loan given to {borrower_name}",
            debit_account=f"Accounts Receivable - {borrower_name}", # KEMBALI KE ACCOUNTS RECEIVABLE
            debit_amount=amount,
            credit_account="Cash",
            credit_amount=amount
        )
        
        app_data["debtor_list"].append({
            'name': borrower_name, 'amount': amount, 'date': date,
            'type': 'loan', 'description': description
        })
        
        return jsonify({'success': True, 'message': f'Loan to {borrower_name} recorded successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/record_borrowing', methods=['POST'])
def record_borrowing():
    try:
        data = request.json
        lender_name = data['lender_name']
        amount = float(data['amount'])
        description = data.get('description', 'Loan Received')
        date = get_current_date()
        
        # Menggunakan Akun: Accounts Payable - Nama Pemberi Pinjaman
        create_journal_entry(
            date=date,
            description=f"Loan received from {lender_name}",
            debit_account="Cash",
            debit_amount=amount,
            credit_account=f"Accounts Payable - {lender_name}", # KEMBALI KE ACCOUNTS PAYABLE
            credit_amount=amount
        )
        
        app_data["creditor_list"].append({
            'name': lender_name, 'amount': amount, 'date': date,
            'type': 'loan', 'description': description
        })
        
        return jsonify({'success': True, 'message': f'Loan from {lender_name} recorded successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/record_loan_payment', methods=['POST'])
def record_loan_payment():
    try:
        data = request.json
        borrower_name = data['borrower_name']
        payment_amount = float(data['payment_amount'])
        date = get_current_date()
        
        borrower = next((d for d in app_data["debtor_list"] if d['name'] == borrower_name and d.get('type') == 'loan'), None)
        if not borrower: return jsonify({'success': False, 'message': 'Borrower not found'})
        if payment_amount > borrower['amount']: return jsonify({'success': False, 'message': 'Payment exceeds balance'})
        
        # Menggunakan Akun: Accounts Receivable - Nama Peminjam
        create_journal_entry(
            date=date,
            description=f"Loan payment from {borrower_name}",
            debit_account="Cash",
            debit_amount=payment_amount,
            credit_account=f"Accounts Receivable - {borrower_name}", # KEMBALI KE ACCOUNTS RECEIVABLE
            credit_amount=payment_amount
        )
        
        borrower['amount'] -= payment_amount
        if borrower['amount'] < 0.01: app_data["debtor_list"].remove(borrower)
        
        return jsonify({'success': True, 'message': f'Payment from {borrower_name} recorded successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/record_debt_repayment', methods=['POST'])
def record_debt_repayment():
    try:
        data = request.json
        lender_name = data['lender_name']
        payment_amount = float(data['payment_amount'])
        date = get_current_date()
        
        lender = next((c for c in app_data["creditor_list"] if c['name'] == lender_name and c.get('type') == 'loan'), None)
        if not lender: return jsonify({'success': False, 'message': 'Lender not found'})
        if payment_amount > lender['amount']: return jsonify({'success': False, 'message': 'Payment exceeds balance'})
        
        # Menggunakan Akun: Accounts Payable - Nama Pemberi Pinjaman
        create_journal_entry(
            date=date,
            description=f"Debt payment to {lender_name}",
            debit_account=f"Accounts Payable - {lender_name}", # KEMBALI KE ACCOUNTS PAYABLE
            debit_amount=payment_amount,
            credit_account="Cash",
            credit_amount=payment_amount
        )
        
        lender['amount'] -= payment_amount
        if lender['amount'] < 0.01: app_data["creditor_list"].remove(lender)
        
        return jsonify({'success': True, 'message': f'Payment to {lender_name} recorded successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/get_loans_given')
def get_loans_given():
    loans_given = [debtor for debtor in app_data["debtor_list"] if debtor.get('type') == 'loan']
    return jsonify(loans_given)

@app.route('/get_loans_received')
def get_loans_received():
    loans_received = [creditor for creditor in app_data["creditor_list"] if creditor.get('type') == 'loan']
    return jsonify(loans_received)

@app.route('/get_sales_receivables')
def get_sales_receivables():
    sales_receivables = [debtor for debtor in app_data["debtor_list"] if debtor.get('type') == 'sales']
    return jsonify(sales_receivables)

# app.py

@app.route('/undo_last_transaction', methods=['POST'])
def undo_last_transaction():
    """
    Membatalkan transaksi terakhir. Dibuat lebih pintar untuk menangani
    transaksi penjualan yang terdiri dari 2 jurnal (Revenue & COGS).
    """
    if not app_data["journal_entries"]:
        return jsonify({"success": False, "message": "No transaction to undo."}), 400

    last_entry = app_data["journal_entries"][-1]

    # Mencegah pembatalan ganda
    if last_entry.get("description", "").startswith("Undo of:"):
        return jsonify({"success": False, "message": "Cannot undo an undo action."}), 400

    entries_to_reverse = []
    final_message = ""

    # --- LOGIKA BARU UNTUK MENDETEKSI TRANSAKSI PENJUALAN ---
    # Cek apakah entri terakhir adalah entri COGS dari penjualan
    is_cogs_entry = "Cost of goods sold for sale to" in last_entry.get("description", "")
    
    # Jika ya, dan ada lebih dari 1 entri di jurnal
    if is_cogs_entry and len(app_data["journal_entries"]) > 1:
        previous_entry = app_data["journal_entries"][-2]
        # Cek apakah entri sebelumnya adalah entri penjualan
        is_sales_entry = "Sale to" in previous_entry.get("description", "")
        
        # Jika kedua kondisi terpenuhi, kita batalkan keduanya
        if is_sales_entry:
            entries_to_reverse.append(previous_entry)
            entries_to_reverse.append(last_entry)
            final_message = f"Successfully undone the entire sale transaction: {previous_entry['description']}"
    
    # Jika bukan transaksi penjualan ganda, atau jika hanya ada 1 entri
    if not entries_to_reverse:
        entries_to_reverse.append(last_entry)
        final_message = f"Successfully undone transaction: {last_entry['description']}"

    # Lakukan proses jurnal pembalik untuk semua entri yang telah diidentifikasi
    for entry in reversed(entries_to_reverse): # Dibalik agar urutan pembatalan logis
        create_journal_entry(
            date=get_current_date(),
            description=f"Undo of: {entry['description']}",
            debit_account=entry['credit_account'],
            debit_amount=entry['credit_amount'],
            credit_account=entry['debit_account'],
            credit_amount=entry['debit_amount']
        )

    return jsonify({
        "success": True, 
        "message": final_message
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

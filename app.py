from flask import Flask, render_template, request, jsonify, session
from collections import defaultdict
import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'financial_accounting_secret_key_2024')

# Translation dictionary
translations = {
    "en": {
        "title": "Financial Accounting Application",
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

# Expense types
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

# Global data storage
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
    "account_balances": defaultdict(float)
}

def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def create_journal_entry(date, description, debit_account, debit_amount, credit_account, credit_amount):
    """Create a journal entry and update general ledger"""
    entry = {
        "date": date,
        "description": description,
        "debit_account": debit_account,
        "debit_amount": float(debit_amount),
        "credit_account": credit_account,
        "credit_amount": float(credit_amount)
    }
    
    app_data["journal_entries"].append(entry)
    
    # Update general ledger
    app_data["general_ledger"][debit_account].append({
        "date": date,
        "description": description,
        "debit": float(debit_amount),
        "credit": 0
    })
    
    app_data["general_ledger"][credit_account].append({
        "date": date,
        "description": description,
        "debit": 0,
        "credit": float(credit_amount)
    })
    
    # Update account balances
    app_data["account_balances"][debit_account] += float(debit_amount)
    app_data["account_balances"][credit_account] -= float(credit_amount)
    
    return entry

@app.route('/')
def home():
    language = session.get('language', 'id')
    return render_template('index.html', translations=translations[language], language=language)

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
        
        sale = {
            "date": data.get('date', get_current_date()),
            "customer": data['customer'],
            "product_name": data['product_name'],
            "quantity": int(data['quantity']),
            "price": float(data['price']),
            "total": float(data['price']) * int(data['quantity']),
            "payment_type": data['payment_type']
        }
        
        app_data["sales_records"].append(sale)
        
        # Update product inventory
        for product in app_data["product_list"]:
            if product['name'] == sale['product_name']:
                product['current_quantity'] -= sale['quantity']
                break
        
        # Create journal entries
        if sale['payment_type'] == 'cash':
            create_journal_entry(
                sale["date"],
                f"Sale to {sale['customer']}",
                "Cash",
                sale["total"],
                "Sales Revenue",
                sale["total"]
            )
        else:  # receivable
            create_journal_entry(
                sale["date"],
                f"Sale to {sale['customer']} (on account)",
                "Accounts Receivable",
                sale["total"],
                "Sales Revenue",
                sale["total"]
            )
            
            # Add to debtor list if not cash
            app_data["debtor_list"].append({
                "name": sale['customer'],
                "amount": sale["total"],
                "date": sale["date"]
            })
        
        return jsonify({"success": True, "message": "Sale recorded successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/get_sales')
def get_sales():
    return jsonify(app_data["sales_records"])

@app.route('/get_debtors')
def get_debtors():
    return jsonify(app_data["debtor_list"])

@app.route('/get_creditors')
def get_creditors():
    return jsonify(app_data["creditor_list"])

@app.route('/record_expense', methods=['POST'])
def record_expense():
    try:
        data = request.json
        
        expense_amount = float(data['amount'])
        expense_type = data['expense_type']
        destination = data.get('destination', '')
        
        create_journal_entry(
            get_current_date(),
            f"{expense_type} - {destination}",
            expense_type,
            expense_amount,
            "Cash",
            expense_amount
        )
        
        return jsonify({"success": True, "message": "Expense recorded successfully!"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

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
            "Share Capital",
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
    ledger_data = {}
    for account, entries in app_data["general_ledger"].items():
        ledger_data[account] = {
            "entries": entries,
            "balance": app_data["account_balances"][account]
        }
    return jsonify(ledger_data)

@app.route('/get_trial_balance')
def get_trial_balance():
    # Define all account categories with specific accounts
    all_accounts = {
        "assets": [
            "Cash", "Inventory", "Accounts Receivable", "Equipment", 
            "Building", "Vehicle", "Accumulated Depreciation - Equipment", 
            "Accumulated Depreciation - Building", "Accumulated Depreciation - Vehicle",
            "Charity", "Investment"
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

@app.route('/get_income_statement')
def get_income_statement():
    revenue = 0
    expenses = 0
    
    for account, balance in app_data["account_balances"].items():
        if "Revenue" in account or "Sales" in account:
            revenue += abs(balance)
        elif "Expense" in account or any(expense in account for expense in expense_types["en"]):
            expenses += abs(balance)
    
    net_income = revenue - expenses
    
    return jsonify({
        "revenue": revenue,
        "expenses": expenses,
        "net_income": net_income
    })

@app.route('/get_balance_sheet')
def get_balance_sheet():
    assets = 0
    liabilities = 0
    equity = app_data["share_capital"]
    
    for account, balance in app_data["account_balances"].items():
        if account in ["Cash", "Accounts Receivable", "Inventory"]:
            assets += abs(balance)
        elif account in ["Accounts Payable"]:
            liabilities += abs(balance)
        elif account == "Share Capital":
            equity = abs(balance)
    
    return jsonify({
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
        "total_assets": assets,
        "total_liabilities_equity": liabilities + equity
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

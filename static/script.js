// Global variables
let currentLanguage = 'id';
let translations = {};
let expenseTypes = [];

// Initialize application
function initializeApp() {
    // Set current date for date inputs
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(input => {
        if (!input.value) {
            input.value = today;
        }
    });
}

// Setup event listeners
// GANTI FUNGSI setupEventListeners ANDA DENGAN VERSI LENGKAP INI

function setupEventListeners() {
    // Language selector
    document.getElementById('language-select').addEventListener('change', function() {
        changeLanguage(this.value);
    });
    
    document.getElementById('refresh-btn').addEventListener('click', refreshCurrentPage);
    document.getElementById('create-closing-entry-btn').addEventListener('click', createClosingEntry);
    document.getElementById('undo-btn').addEventListener('click', undoLastTransaction);

    // Form submissions utama
    setupFormListeners();
    
    // ▼▼▼ BAGIAN YANG DIPINDAHKAN ADA DI SINI ▼▼▼
    // Event listener untuk form PPE
    const ppeForm = document.getElementById('ppe-form');
    if (ppeForm) {
        ppeForm.addEventListener('submit', handlePpeFormSubmit);
    }

    // Tampilkan/sembunyikan field khusus UoP
    const ppeMethod = document.getElementById('ppe-depreciation-method');
    if (ppeMethod) {
        ppeMethod.addEventListener('change', function() {
            document.getElementById('uop-fields').style.display = this.value === 'uop' ? 'flex' : 'none';
        });
    }

    // Event listener untuk tombol rekam depresiasi
    const recordBtn = document.getElementById('record-depreciation-btn');
    if (recordBtn) {
        recordBtn.addEventListener('click', recordPeriodDepreciation); // Langsung catat, atau ganti ke previewPeriodDepreciation jika Anda ingin preview dulu
    }

    // Event listener untuk modal history
    const historyModal = document.getElementById('depreciation-history-modal');
    if (historyModal) {
        historyModal.addEventListener('show.bs.modal', loadDepreciationHistory);
    }
    // ▲▲▲ AKHIR DARI BAGIAN YANG DIPINDAHKAN ▲▲▲
}

function refreshCurrentPage() {
    const activePage = document.querySelector('.page.active');
    
    // Pengaman jika tidak ada halaman yang aktif
    if (!activePage) {
        console.error("No active page found to refresh.");
        return;
    }

    // Memberi feedback visual ke pengguna
    const refreshButton = document.getElementById('refresh-btn');
    const icon = refreshButton.querySelector('i');
    
    icon.classList.add('fa-spin'); // Membuat ikon berputar
    refreshButton.disabled = true;  // Mencegah klik ganda

    // Mengambil ID halaman (misal: 'sales-page' menjadi 'sales')
    const pageId = activePage.id.replace('-page', '');

    console.log(`Refreshing data for page: ${pageId}`);
    
    // Memanggil fungsi pemuat data yang sudah ada
    loadPageData(pageId);

    // Hentikan feedback visual setelah jeda singkat
    setTimeout(() => {
        icon.classList.remove('fa-spin');
        refreshButton.disabled = false;
        showMessage('Page data has been refreshed!', 'success');
    }, 1000); // Jeda 1 detik
}

// script.js

// GANTI SELURUH FUNGSI INI
function setupFormListeners() {
    // Product stocking form
    document.getElementById('product-stocking-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitProductStocking();
    });

    // Share capital form
    document.getElementById('share-capital-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitShareCapital();
    });

    // Sales receivable payment form
    document.getElementById('sales-receivable-payment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitSalesReceivablePayment();
    });

    // Quantity addition form
    document.getElementById('quantity-addition-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitQuantityAddition();
    });

    // Sales form
    document.getElementById('sales-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitSales();
    });

    // Expense form
    document.getElementById('expense-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitExpense();
    });

    // Charity form
    document.getElementById('charity-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitCharity();
    });

    // Investment forms
    document.getElementById('investment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitInvestment();
    });

    document.getElementById('sell-investment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitSellInvestment();
    });

    /* // DIHAPUS/DIKOMENTARI KARENA FORM DENGAN ID INI TIDAK ADA DI HTML ANDA
    // INILAH PENYEBAB UTAMA ERROR YANG MENGHENTIKAN SCRIPT
    document.getElementById('receivable-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitReceivable();
    });

    document.getElementById('payable-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitPayable();
    });

    document.getElementById('receivable-payment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitReceivablePayment();
    });

    document.getElementById('payable-payment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitPayablePayment();
    });
    
    document.getElementById('sales-receivable-payment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitSalesReceivablePayment();
    });
    */


    // Lending/Borrowing forms
    document.getElementById('lending-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitLending();
    });

    document.getElementById('borrowing-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitBorrowing();
    });

    document.getElementById('loan-payment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitLoanPayment();
    });

    document.getElementById('debt-repayment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        submitDebtRepayment();
    });
}

// script.js

function loadSalesReceivablesForPayment() {
    const select = document.getElementById('sales-receivable-select');
    select.innerHTML = '<option value="">Loading unpaid sales...</option>';

    fetch('/get_sales_receivables')
    .then(response => response.json())
    .then(data => {
        select.innerHTML = '<option value="">Select a receivable to pay...</option>';
        if (data.length === 0) {
            select.innerHTML = '<option value="">No unpaid sales found</option>';
            return;
        }

        data.forEach(receivable => {
            const option = document.createElement('option');
            option.value = receivable.id;
            // Tampilkan info: Pelanggan - Deskripsi - Sisa Tagihan
            option.textContent = `${receivable.name} - ${receivable.description} - [${formatCurrency(receivable.amount)}]`;
            select.appendChild(option);
        });
    });
}

function submitSalesReceivablePayment() {
    const form = document.getElementById('sales-receivable-payment-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    if (!data.receivable_id || !data.payment_amount) {
        showMessage('Please select a receivable and enter a payment amount.', 'error');
        return;
    }

    fetch('/record_sales_receivable_payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showMessage(result.message, 'success');
            form.reset();
            // Muat ulang daftar piutang agar yang sudah lunas/berkurang terupdate
            loadSalesReceivablesForPayment();
        } else {
            showMessage(result.message, 'error');
        }
    })
    .catch(error => showMessage('An error occurred: ' + error, 'error'));
}

// Language management
function changeLanguage(language) {
    currentLanguage = language;
    
    fetch('/set_language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `language=${language}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Reload to get new translations
        }
    });
}

function loadTranslations() {
    fetch('/get_translations')
    .then(response => response.json())
    .then(data => {
        translations = data;
    });
}

function loadExpenseTypes() {
    fetch('/get_expense_types')
    .then(response => response.json())
    .then(data => {
        expenseTypes = data;
        populateExpenseSelect();
    });
}

function populateExpenseSelect() {
    const select = document.querySelector('select[name="expense_type"]');
    select.innerHTML = '<option value="">Select Expense Type</option>';
    
    expenseTypes.forEach(expense => {
        const option = document.createElement('option');
        option.value = expense;
        option.textContent = expense;
        select.appendChild(option);
    });
}

// Page navigation
function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    const targetPage = document.getElementById(pageId + '-page');
    if (targetPage) {
        targetPage.classList.add('active');
        
        // Load page-specific data
        loadPageData(pageId);
    }
}

// Load page-specific data
// Ganti fungsi loadPageData yang lama dengan yang ini di script.js

function loadPageData(pageId) {
    switch(pageId) {
        case 'product-list':
            loadProducts();
            break;
        case 'quantity-addition':
            loadProductsForSelection();
            break;
        case 'sales':
            loadProductsForSales();
            loadSalesReceivablesForPayment();
            break;
        case 'payables-receivables':
            loadDebtorsAndCreditors();
            loadDebtorCreditorSelects();
            loadSalesReceivables();
            loadSalesReceivableSelects();
            break;
        case 'charity':
            // No specific data to load
            break;
        // --- TAMBAHKAN CASE BARU DI BAWAH INI ---
        case 'expense-entry':
            loadExpenseTypes(); // Ini akan memastikan dropdown diisi setiap kali halaman dibuka
            break;
        // -----------------------------------------
        case 'investment':
            loadInvestments();
            loadInvestmentSelects();
            break;
        case 'lending-borrowing':
            loadLoansGiven();
            loadLoansReceived();
            loadLoanSelects();
            break;
        case 'journal-entry':
            loadJournalEntries();
            break;
        case 'general-ledger':
            loadGeneralLedger();
            break;
        case 'trial-balance':
            loadTrialBalance();
            break;
        case 'income-statement':
            loadIncomeStatement();
            break;
        case 'balance-sheet':
            loadBalanceSheet();
            break;
    }
}

// Form submission functions
function submitProductStocking() {
    const formData = new FormData(document.getElementById('product-stocking-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/product_stocking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('product-stocking-form').reset();
            // Set current date
            document.querySelector('#product-stocking-form input[name="date"]').value = new Date().toISOString().split('T')[0];
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitShareCapital() {
    const formData = new FormData(document.getElementById('share-capital-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/set_share_capital', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('share-capital-form').reset();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitQuantityAddition() {
    const formData = new FormData(document.getElementById('quantity-addition-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/add_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('quantity-addition-form').reset();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitSales() {
    const formData = new FormData(document.getElementById('sales-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/record_sale', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('sales-form').reset();
            // Set current date
            document.querySelector('#sales-form input[name="date"]').value = new Date().toISOString().split('T')[0];
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitExpense() {
    const formData = new FormData(document.getElementById('expense-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/record_expense', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('expense-form').reset();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitCharity() {
    const formData = new FormData(document.getElementById('charity-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/record_charity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('charity-form').reset();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitInvestment() {
    const formData = new FormData(document.getElementById('investment-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/record_investment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('investment-form').reset();
            loadInvestments();
            loadInvestmentSelects();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitSellInvestment() {
    const formData = new FormData(document.getElementById('sell-investment-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/sell_investment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const gainLossText = data.gain_loss >= 0 ? `Gain: ${formatCurrency(data.gain_loss)}` : `Loss: ${formatCurrency(Math.abs(data.gain_loss))}`;
            showMessage(`${data.message} ${gainLossText}`, 'success');
            document.getElementById('sell-investment-form').reset();
            loadInvestments();
            loadInvestmentSelects();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitReceivable() {
    const formData = new FormData(document.getElementById('receivable-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/create_receivable', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('receivable-form').reset();
            loadDebtorsAndCreditors();
            loadDebtorCreditorSelects();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitPayable() {
    const formData = new FormData(document.getElementById('payable-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/create_payable', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('payable-form').reset();
            loadDebtorsAndCreditors();
            loadDebtorCreditorSelects();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitReceivablePayment() {
    const formData = new FormData(document.getElementById('receivable-payment-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/record_receivable_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('receivable-payment-form').reset();
            loadDebtorsAndCreditors();
            loadDebtorCreditorSelects();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitPayablePayment() {
    const formData = new FormData(document.getElementById('payable-payment-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/record_payable_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('payable-payment-form').reset();
            loadDebtorsAndCreditors();
            loadDebtorCreditorSelects();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

// Data loading functions
function loadProducts() {
    fetch('/get_products')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('product-list-tbody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No products found</td></tr>';
            return;
        }
        
        data.forEach(product => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.name}</td>
                <td>${product.initial_quantity}</td>
                <td>${product.current_quantity}</td>
                <td>${formatCurrency(product.purchase_price)}</td>
                <td>${formatCurrency(product.selling_price)}</td>
                <td>${formatCurrency(product.total_purchase_price)}</td>
            `;
            tbody.appendChild(row);
        });
    });
}

function loadProductsForSelection() {
    fetch('/get_products')
    .then(response => response.json())
    .then(data => {
        const select = document.querySelector('#quantity-addition-form select[name="product_name"]');
        select.innerHTML = '<option value="">Select Product</option>';
        
        data.forEach(product => {
            const option = document.createElement('option');
            option.value = product.name;
            option.textContent = product.name;
            select.appendChild(option);
        });
    });
}

// script.js

function loadProductsForSales() {
    fetch('/get_products')
    .then(response => response.json())
    .then(data => {
        // Targetkan dropdown di dalam form penjualan
        const select = document.querySelector('#sales-form select[name="product_name"]');
        select.innerHTML = '<option value="">Select Product</option>';
        
        data.forEach(product => {
            // Hanya tampilkan produk yang stoknya lebih dari 0
            if (product.current_quantity > 0) {
                const option = document.createElement('option');
                option.value = product.name;
                option.textContent = `${product.name} (Stock: ${product.current_quantity})`;
                option.setAttribute('data-price', product.selling_price); // Simpan harga jual di data-attribute
                select.appendChild(option);
            }
        });
        
        // Event listener untuk mengisi harga secara otomatis saat produk dipilih
        select.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const priceInput = document.querySelector('#sales-form input[name="price"]');
            if (selectedOption.dataset.price) {
                priceInput.value = selectedOption.dataset.price;
            } else {
                priceInput.value = '';
            }
        });
    });
}

function loadDebtorsAndCreditors() {
    // Memuat daftar Piutang (Debitur)
    fetch('/get_debtors')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('debtors-tbody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">Tidak ada piutang.</td></tr>';
            return;
        }
        
        data.forEach(debtor => {
            const row = document.createElement('tr');
            let description = debtor.description || (debtor.type === 'loan' ? 'Pinjaman Diberikan' : (debtor.type === 'sales' ? 'Penjualan' : 'Lain-lain'));
            
            row.innerHTML = `
                <td>${debtor.name}</td>
                <td>${formatCurrency(debtor.amount)}</td>
                <td><span class="badge bg-secondary">${description}</span></td>
                <td>${debtor.date}</td>
            `;
            tbody.appendChild(row);
        });
    });

    // Memuat daftar Utang (Kreditur)
    fetch('/get_creditors')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('creditors-tbody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">Tidak ada utang.</td></tr>';
            return;
        }
        
        data.forEach(creditor => {
            const row = document.createElement('tr');
            let description = creditor.description || (creditor.type === 'loan' ? 'Pinjaman Diterima' : 'Lain-lain');

            row.innerHTML = `
                <td>${creditor.name}</td>
                <td>${formatCurrency(creditor.amount)}</td>
                <td><span class="badge bg-dark">${description}</span></td>
                <td>${creditor.date}</td>
            `;
            tbody.appendChild(row);
        });
    });
}

function loadJournalEntries() {
    fetch('/get_journal_entries')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('journal-entries-tbody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">No journal entries found</td></tr>';
            return;
        }
        
        data.forEach(entry => {
            // Debit entry row
            const debitRow = document.createElement('tr');
            debitRow.innerHTML = `
                <td>${entry.date}</td>
                <td>${entry.debit_account}</td>
                <td>${formatCurrency(entry.debit_amount)}</td>
                <td>-</td>
            `;
            tbody.appendChild(debitRow);
            
            const creditRow = document.createElement('tr');
            creditRow.innerHTML = `
                <td></td>
                <td>&nbsp;&nbsp;&nbsp;&nbsp;${entry.credit_account}</td>
                <td>-</td>
                <td>${formatCurrency(entry.credit_amount)}</td>
            `;
            tbody.appendChild(creditRow);
            
            // Description row
            const descRow = document.createElement('tr');
            descRow.innerHTML = `
                <td></td>
                <td colspan="3"><em>${entry.description}</em></td>
            `;
            tbody.appendChild(descRow);
            
            // Empty row for spacing
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = '<td colspan="4">&nbsp;</td>';
            tbody.appendChild(emptyRow);
        });
    });
}

function loadGeneralLedger() {
    fetch('/get_general_ledger')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('general-ledger-content');
        container.innerHTML = '';
        
        if (Object.keys(data).length === 0) {
            container.innerHTML = '<p class="text-center">No ledger entries found</p>';
            return;
        }
        
        Object.entries(data).forEach(([account, accountData]) => {
            const accountDiv = document.createElement('div');
            accountDiv.className = 'ledger-account';
            
            let entriesHtml = '';
            accountData.entries.forEach(entry => {
                entriesHtml += `
                    <div class="statement-item">
                        <span>${entry.date} - ${entry.description}</span>
                        <span>
                            ${entry.debit > 0 ? formatCurrency(entry.debit) + ' DR' : ''}
                            ${entry.credit > 0 ? formatCurrency(entry.credit) + ' CR' : ''}
                        </span>
                    </div>
                `;
            });
            
            accountDiv.innerHTML = `
                <h5>${account}</h5>
                ${entriesHtml}
                <div class="balance">
                    Balance: ${formatCurrency(Math.abs(accountData.balance))} 
                    ${accountData.balance >= 0 ? 'DR' : 'CR'}
                </div>
            `;
            
            container.appendChild(accountDiv);
        });
    });
}

function loadTrialBalance() {
    fetch('/get_trial_balance')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('trial-balance-tbody');
        tbody.innerHTML = '';
        
        if (data.accounts.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center">No trial balance data found</td></tr>';
            return;
        }
        
        data.accounts.forEach(account => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${account.account}</td>
                <td>${account.debit > 0 ? formatCurrency(account.debit) : '-'}</td>
                <td>${account.credit > 0 ? formatCurrency(account.credit) : '-'}</td>
            `;
            tbody.appendChild(row);
        });
        
        // Add total row
        const totalRow = document.createElement('tr');
        totalRow.className = 'table-success fw-bold';
        totalRow.innerHTML = `
            <td><strong>TOTAL</strong></td>
            <td><strong>${formatCurrency(data.total_debit)}</strong></td>
            <td><strong>${formatCurrency(data.total_credit)}</strong></td>
        `;
        tbody.appendChild(totalRow);
    });
}

function loadIncomeStatement() {
    fetch('/get_income_statement')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('income-statement-content');

        // Bagian Pendapatan
        let revenueHtml = '';
        if (Object.keys(data.revenue_details).length > 0) {
            for (const [account, amount] of Object.entries(data.revenue_details)) {
                revenueHtml += `<div class="statement-item"><span>${account}</span><span>${formatCurrency(amount)}</span></div>`;
            }
        } else {
            revenueHtml = `<div class="statement-item"><span>No revenue recorded</span><span>${formatCurrency(0)}</span></div>`;
        }

        // Bagian Beban Operasional
        let expensesHtml = '';
        if (Object.keys(data.operating_expense_details).length > 0) {
            for (const [account, amount] of Object.entries(data.operating_expense_details)) {
                expensesHtml += `<div class="statement-item"><span>${account}</span><span>${formatCurrency(amount)}</span></div>`;
            }
        }

        // Bagian Pendapatan/Beban Lain-lain
        let otherHtml = '';
        if (Object.keys(data.other_income_and_expense_details).length > 0) {
            for (const [account, amount] of Object.entries(data.other_income_and_expense_details)) {
                 otherHtml += `<div class="statement-item"><span>${account}</span><span>${formatCurrency(amount)}</span></div>`;
            }
        }

        // Rakit semua menjadi Laporan Laba Rugi yang utuh
        container.innerHTML = `
            <div class="financial-statement">
                <h4>INCOME STATEMENT</h4>
                
                <div class="statement-section">
                    <div class="statement-title">REVENUE</div>
                    ${revenueHtml}
                    <div class="statement-item">
                        <span>Less: Cost of Goods Sold</span>
                        <span>(${formatCurrency(data.cogs)})</span>
                    </div>
                    <div class="statement-total mt-2">
                        <div class="statement-item">
                            <span><strong>GROSS PROFIT</strong></span>
                            <span><strong>${formatCurrency(data.gross_profit)}</strong></span>
                        </div>
                    </div>
                </div>
                
                <div class="statement-section">
                    <div class="statement-title">OPERATING EXPENSES</div>
                    ${expensesHtml}
                    <div class="statement-total">
                        <div class="statement-item">
                            <span>Total Operating Expenses</span>
                            <span>(${formatCurrency(data.total_operating_expenses)})</span>
                        </div>
                    </div>
                     <div class="statement-total">
                        <div class="statement-item">
                            <span><strong>OPERATING INCOME</strong></span>
                            <span><strong>${formatCurrency(data.operating_income)}</strong></span>
                        </div>
                    </div>
                </div>
                
                <div class="statement-section">
                    <div class="statement-title">OTHER INCOME AND EXPENSES</div>
                    ${otherHtml}
                </div>
                
                <div class="statement-total final-total">
                    <div class="statement-item">
                        <span><strong>NET INCOME</strong></span>
                        <span><strong>${formatCurrency(data.net_income)}</strong></span>
                    </div>
                </div>
            </div>
        `;
    })
    .catch(error => {
        console.error('Error loading income statement:', error);
        document.getElementById('income-statement-content').innerHTML = '<p class="text-danger text-center">Failed to load income statement data.</p>';
    });
}

function loadBalanceSheet() {
    fetch('/get_balance_sheet')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('balance-sheet-content');
        
        // Build assets section
        let assetsHtml = '';
        Object.entries(data.asset_accounts).forEach(([account, balance]) => {
            const isContraAsset = account.includes('Accumulated Depreciation');
            
            // INI PERBAIKANNYA:
            // Tampilkan nilai absolut untuk semua aset. Jika ini akun kontra, bungkus dengan kurung.
            const displayBalance = isContraAsset 
                ? `(${formatCurrency(Math.abs(balance))})` 
                : formatCurrency(Math.abs(balance)); // Gunakan Math.abs() untuk semua aset
            
            assetsHtml += `
                <div class="statement-item">
                    <span>${isContraAsset ? `&nbsp;&nbsp;&nbsp;&nbsp;${account}` : account}</span>
                    <span>${displayBalance}</span>
                </div>
            `;
        });
        
        // Build liabilities section
        let liabilitiesHtml = '';
        Object.entries(data.liability_accounts).forEach(([account, balance]) => {
            // Liabilitas juga selalu ditampilkan sebagai nilai positif (absolut)
            liabilitiesHtml += `
                <div class="statement-item">
                    <span>${account}</span>
                    <span>${formatCurrency(Math.abs(balance))}</span>
                </div>
            `;
        });
        
        // Build equity section
        let equityHtml = '';
        Object.entries(data.equity_accounts).forEach(([account, balance]) => {
            // Prive (pengambilan pribadi) adalah kontra ekuitas, ditampilkan sebagai pengurang.
            const isContraEquity = account.includes('Prive');
            if (isContraEquity) {
                if (balance !== 0) {
                    equityHtml += `
                        <div class="statement-item">
                            <span>&nbsp;&nbsp;&nbsp;&nbsp;${account}</span>
                            <span>(${formatCurrency(Math.abs(balance))})</span>
                        </div>
                    `;
                }
            } else {
                equityHtml += `
                    <div class="statement-item">
                        <span>${account}</span>
                        <span>${formatCurrency(Math.abs(balance))}</span>
                    </div>
                `;
            }
        });
        
        // Rakit semua menjadi HTML (tidak ada perubahan di bagian ini)
        container.innerHTML = `
            <div class="financial-statement">
                <h4>BALANCE SHEET</h4>
                <div class="row">
                    <div class="col-md-6">
                        <div class="statement-section">
                            <div class="statement-title">ASSETS</div>
                            ${assetsHtml}
                            <div class="statement-total">
                                <div class="statement-item">
                                    <span><strong>TOTAL ASSETS</strong></span>
                                    <span><strong>${formatCurrency(data.total_assets)}</strong></span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="statement-section">
                            <div class="statement-title">LIABILITIES</div>
                            ${liabilitiesHtml}
                            <div class="statement-total">
                                <div class="statement-item">
                                    <span><strong>TOTAL LIABILITIES</strong></span>
                                    <span><strong>${formatCurrency(data.total_liabilities)}</strong></span>
                                </div>
                            </div>
                        </div>
                        <div class="statement-section">
                            <div class="statement-title">EQUITY</div>
                            ${equityHtml}
                            <div class="statement-total">
                                <div class="statement-item">
                                    <span><strong>TOTAL EQUITY</strong></span>
                                    <span><strong>${formatCurrency(data.total_equity)}</strong></span>
                                </div>
                            </div>
                        </div>
                        <div class="statement-total final-total">
                            <div class="statement-item">
                                <span><strong>TOTAL LIABILITIES & EQUITY</strong></span>
                                <span><strong>${formatCurrency(data.total_liabilities_equity)}</strong></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}


function submitLending() {
    const form = document.getElementById('lending-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    fetch('/record_lending', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showMessage(result.message, 'success');
            form.reset();
            // PANGGILAN FUNGSI YANG DIPERLUKAN
            loadLoansGiven();      // Muat ulang tabel pinjaman yang diberikan
            loadLoanSelects();     // Perbarui dropdown untuk pembayaran
        } else {
            showMessage(result.message, 'error');
        }
    })
    .catch(error => {
        showMessage('Terjadi kesalahan jaringan: ' + error.message, 'error');
    });
}

function submitBorrowing() {
    const formData = new FormData(document.getElementById('borrowing-form'));
    const data = Object.fromEntries(formData.entries());

    fetch('/record_borrowing', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('borrowing-form').reset();
            // PASTIKAN FUNGSI INI DIPANGGIL
            loadLoansReceived(); // Muat ulang tabel pinjaman yang diterima
            loadLoanSelects();   // Perbarui dropdown untuk pembayaran utang
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitLoanPayment() {
    const formData = new FormData(document.getElementById('loan-payment-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/record_loan_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('loan-payment-form').reset();
            loadLoansGiven();
            loadLoanSelects();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

function submitDebtRepayment() {
    const formData = new FormData(document.getElementById('debt-repayment-form'));
    const data = Object.fromEntries(formData.entries());
    
    fetch('/record_debt_repayment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            document.getElementById('debt-repayment-form').reset();
            loadLoansReceived();
            loadLoanSelects();
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('An error occurred: ' + error.message, 'error');
    });
}

// Investment functions
function loadInvestments() {
    fetch('/get_investments')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('investments-tbody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center">No investments found</td></tr>';
            return;
        }
        
        data.forEach(investment => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${investment.company}</td>
                <td>${investment.type}</td>
                <td>${investment.date}</td>
                <td>${formatCurrency(investment.amount)}</td>
            `;
            tbody.appendChild(row);
        });
    });
}

function loadInvestmentSelects() {
    fetch('/get_investments')
    .then(response => response.json())
    .then(data => {
        const select = document.querySelector('#sell-investment-form select[name="investment_id"]');
        select.innerHTML = '<option value="">Select Investment</option>';
        
        data.forEach((investment, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${investment.company} - ${investment.type} (${formatCurrency(investment.amount)})`;
            select.appendChild(option);
        });
    });
}

function loadDebtorCreditorSelects() {
    // Load debtors for payment form
    fetch('/get_debtors')
    .then(response => response.json())
    .then(data => {
        const select = document.querySelector('#receivable-payment-form select[name="debtor_name"]');
        select.innerHTML = '<option value="">Select Debtor</option>';
        
        // Filter out sales and loan receivables
        const otherDebtors = data.filter(debtor => debtor.type !== 'sales' && debtor.type !== 'loan');
        
        otherDebtors.forEach(debtor => {
            const option = document.createElement('option');
            option.value = debtor.name;
            option.textContent = `${debtor.name} (${formatCurrency(debtor.amount)})`;
            select.appendChild(option);
        });
    });

    // Load creditors for payment form
    fetch('/get_creditors')
    .then(response => response.json())
    .then(data => {
        const select = document.querySelector('#payable-payment-form select[name="creditor_name"]');
        select.innerHTML = '<option value="">Select Creditor</option>';
        
        data.forEach(creditor => {
            const option = document.createElement('option');
            option.value = creditor.name;
            option.textContent = `${creditor.name} (${formatCurrency(creditor.amount)})`;
            select.appendChild(option);
        });
    });
}

// script.js

function submitSalesReceivablePayment() {
    const form = document.getElementById('sales-receivable-payment-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    if (!data.receivable_id || !data.payment_amount) {
        showMessage('Please select a receivable and enter a payment amount.', 'error');
        return;
    }

    fetch('/record_sales_receivable_payment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showMessage(result.message, 'success');
            form.reset();
            loadSalesReceivablesForPayment(); // Muat ulang daftar piutang

            // --- BARIS BARU: Menutup Modal setelah berhasil ---
            const settlementModalEl = document.getElementById('settlementModal');
            const settlementModal = bootstrap.Modal.getInstance(settlementModalEl);
            if (settlementModal) {
                settlementModal.hide();
            }
            // ----------------------------------------------------

        } else {
            showMessage(result.message, 'error');
        }
    })
    .catch(error => showMessage('An error occurred: ' + error, 'error'));
}

// Lending/Borrowing functions
function loadLoansGiven() {
    fetch('/get_loans_given')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('loans-given-tbody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center">No loans given</td></tr>';
            return;
        }
        
        data.forEach(loan => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${loan.name}</td>
                <td>${formatCurrency(loan.amount)}</td>
                <td>${loan.date}</td>
            `;
            tbody.appendChild(row);
        });
    });
}

function loadLoansReceived() {
    fetch('/get_loans_received')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('loans-received-tbody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center">No loans received</td></tr>';
            return;
        }
        
        data.forEach(loan => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${loan.name}</td>
                <td>${formatCurrency(loan.amount)}</td>
                <td>${loan.date}</td>
            `;
            tbody.appendChild(row);
        });
    });
}

function loadLoanSelects() {
    // Load borrowers for loan payment form
    fetch('/get_loans_given')
    .then(response => response.json())
    .then(data => {
        const select = document.querySelector('#loan-payment-form select[name="borrower_name"]');
        select.innerHTML = '<option value="">Select Borrower</option>';
        
        data.forEach(loan => {
            const option = document.createElement('option');
            option.value = loan.name;
            option.textContent = `${loan.name} (${formatCurrency(loan.amount)})`;
            select.appendChild(option);
        });
    });

    // Load lenders for debt repayment form
    fetch('/get_loans_received')
    .then(response => response.json())
    .then(data => {
        const select = document.querySelector('#debt-repayment-form select[name="lender_name"]');
        select.innerHTML = '<option value="">Select Lender</option>';
        
        data.forEach(loan => {
            const option = document.createElement('option');
            option.value = loan.name;
            option.textContent = `${loan.name} (${formatCurrency(loan.amount)})`;
            select.appendChild(option);
        });
    });
}

function loadSalesReceivables() {
    fetch('/get_sales_receivables')
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('sales-receivables-tbody');
        tbody.innerHTML = '';
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No sales receivables</td></tr>';
            return;
        }
        
        data.forEach(receivable => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${receivable.name}</td>
                <td>${formatCurrency(receivable.amount)}</td>
                <td>${receivable.product || '-'}</td>
                <td>${receivable.quantity || '-'}</td>
                <td>${receivable.date}</td>
            `;
            tbody.appendChild(row);
        });
    });
}

function loadSalesReceivableSelects() {
    fetch('/get_sales_receivables')
    .then(response => response.json())
    .then(data => {
        const select = document.querySelector('#sales-receivable-payment-form select[name="customer_name"]');
        select.innerHTML = '<option value="">Select Customer</option>';
        
        data.forEach(receivable => {
            const option = document.createElement('option');
            option.value = receivable.name;
            option.textContent = `${receivable.name} (${formatCurrency(receivable.amount)}) - ${receivable.product}`;
            select.appendChild(option);
        });
    });
}

// Utility functions
// script.js
// GANTI FUNGSI LAMA DENGAN YANG INI
function formatCurrency(amount) {
    // Ambil info mata uang dari localStorage, atau gunakan Rupiah sebagai default
    const currencyInfo = JSON.parse(localStorage.getItem('currencyInfo')) || { code: 'IDR', symbol: 'Rp' };
    
    // Intl.NumberFormat adalah cara modern dan terbaik untuk format mata uang
    return new Intl.NumberFormat('id-ID', { // Anda bisa membuat 'id-ID' dinamis jika perlu
        style: 'currency',
        currency: currencyInfo.code, // Kode ISO 4217, misal: 'USD', 'IDR', 'JPY'
        minimumFractionDigits: 0,
        maximumFractionDigits: 2 // Beberapa mata uang butuh desimal
    }).format(amount);
}

function showMessage(message, type) {
    const container = document.getElementById('message-container');
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle';
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    alertDiv.innerHTML = `
        <i class="${icon}"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Helper function to validate forms
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// --- Tambahkan fungsi ini di file script.js ---

// HAPUS fungsi createClosingEntry yang lama di script.js dan GANTI dengan yang ini.

function createClosingEntry() {
    const button = document.getElementById('create-closing-entry-btn');
    button.disabled = true;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Memproses...';

    fetch('/create_closing_entry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            const tbody = document.getElementById('closing-entry-tbody');
            tbody.innerHTML = ''; // Bersihkan tabel dari hasil sebelumnya

            if (data.closing_entries.length === 0) {
                 tbody.innerHTML = `<tr><td colspan="4" class="text-center">Tidak ada data untuk ditutup.</td></tr>`;
            } else {
                data.closing_entries.forEach(entry => {
                    // Baris untuk akun DEBIT
                    const row1 = document.createElement('tr');
                    row1.innerHTML = `
                        <td>${entry.date}</td>
                        <td>${entry.debit_account}</td>
                        <td>${formatCurrency(entry.debit_amount)}</td>
                        <td></td>
                    `;
                    tbody.appendChild(row1);

                    // Baris untuk akun KREDIT (dengan indentasi)
                    const row2 = document.createElement('tr');
                    row2.innerHTML = `
                        <td></td>
                        <td style="padding-left: 2.5em;">${entry.credit_account}</td>
                        <td></td>
                        <td>${formatCurrency(entry.credit_amount)}</td>
                    `;
                    tbody.appendChild(row2);

                    // Baris untuk KETERANGAN (dengan indentasi)
                    const row3 = document.createElement('tr');
                    row3.style.fontStyle = 'italic';
                    row3.style.color = '#6c757d'; // Warna abu-abu
                    row3.innerHTML = `
                        <td></td>
                        <td colspan="3" style="padding-left: 2.5em;">(${entry.description})</td>
                    `;
                    tbody.appendChild(row3);
                });
            }

            document.getElementById('closing-entry-result').style.display = 'block';
            button.innerHTML = '<i class="fas fa-check"></i> Proses Selesai';
        } else {
            showMessage(`Error: ${data.message}`, 'error');
            button.disabled = false;
            button.innerHTML = originalText;
        }
    })
    .catch(error => {
        showMessage('Terjadi kesalahan jaringan: ' + error.message, 'error');
        button.disabled = false;
        button.innerHTML = originalText;
    });
}

// script.js

/**
 * Menangani permintaan untuk membatalkan transaksi terakhir.
 */
function undoLastTransaction() {
    // Minta konfirmasi dari pengguna sebelum melanjutkan
    const originalDescription = document.querySelector('#journal-entries-tbody tr:last-child td em')?.textContent || "last transaction";
    if (!confirm(`Are you sure you want to undo the following transaction?\n\n${originalDescription}`)) {
        return; // Batalkan jika pengguna menekan 'Cancel'
    }

    fetch('/undo_last_transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            // Muat ulang halaman untuk memastikan semua data (laporan, dll) diperbarui
            setTimeout(() => {
                location.reload();
            }, 1500); // Beri jeda 1.5 detik agar pengguna sempat membaca pesan
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Undo Error:', error);
        showMessage('An error occurred while trying to undo.', 'error');
    });
}

// script.js
// TAMBAHKAN SELURUH BLOK KODE INI DI AKHIR FILE ANDA

// --- BAGIAN PENYIAPAN AWAL (VERSI STABIL TANPA BENDERA) ---

// script.js
// TAMBAHKAN SELURUH BLOK KODE INI DI AKHIR FILE ANDA

// --- BAGIAN PENYIAPAN AWAL (VERSI STABIL TANPA BENDERA) ---

let selectedCurrency = null;

// Daftar mata uang (tanpa properti 'flag')
const currencyData = [
    { country: 'Afghanistan', symbol: 'Af', code: 'AFN' },
    { country: 'Albania', symbol: 'L', code: 'ALL' },
    { country: 'Algeria', symbol: 'DA', code: 'DZD' },
    { country: 'Andorra', symbol: '€', code: 'EUR' },
    { country: 'Angola', symbol: 'Kz', code: 'AOA' },
    { country: 'Antigua and Barbuda', symbol: 'EC$', code: 'XCD' },
    { country: 'Argentina', symbol: '$AR', code: 'ARS' },
    { country: 'Armenia', symbol: '֏', code: 'AMD' },
    { country: 'Australia', symbol: 'A$', code: 'AUD' },
    { country: 'Austria', symbol: '€', code: 'EUR' },
    { country: 'Azerbaijan', symbol: '₼', code: 'AZN' },
    { country: 'Bahamas', symbol: 'B$', code: 'BSD' },
    { country: 'Bahrain', symbol: 'BD', code: 'BHD' },
    { country: 'Bangladesh', symbol: '৳', code: 'BDT' },
    { country: 'Barbados', symbol: 'Bds$', code: 'BBD' },
    { country: 'Belarus', symbol: 'Br', code: 'BYN' },
    { country: 'Belgium', symbol: '€', code: 'EUR' },
    { country: 'Belize', symbol: 'BZ$', code: 'BZD' },
    { country: 'Benin', symbol: 'CFA', code: 'XOF' },
    { country: 'Bhutan', symbol: 'Nu.', code: 'BTN' },
    { country: 'Bolivia', symbol: 'Bs', code: 'BOB' },
    { country: 'Bosnia and Herzegovina', symbol: 'KM', code: 'BAM' },
    { country: 'Botswana', symbol: 'P', code: 'BWP' },
    { country: 'Brazil', symbol: 'R$', code: 'BRL' },
    { country: 'Brunei', symbol: 'B$', code: 'BND' },
    { country: 'Bulgaria', symbol: 'лв', code: 'BGN' },
    { country: 'Burkina Faso', symbol: 'CFA', code: 'XOF' },
    { country: 'Burundi', symbol: 'FBu', code: 'BIF' },
    { country: 'Cabo Verde', symbol: 'Esc', code: 'CVE' },
    { country: 'Cambodia', symbol: '៛', code: 'KHR' },
    { country: 'Cameroon', symbol: 'CFA', code: 'XAF' },
    { country: 'Canada', symbol: 'C$', code: 'CAD' },
    { country: 'Central African Republic', symbol: 'CFA', code: 'XAF' },
    { country: 'Chad', symbol: 'CFA', code: 'XAF' },
    { country: 'Chile', symbol: 'CLP$', code: 'CLP' },
    { country: 'China', symbol: '¥', code: 'CNY' },
    { country: 'Colombia', symbol: 'COL$', code: 'COP' },
    { country: 'Comoros', symbol: 'CF', code: 'KMF' },
    { country: 'Congo (Brazzaville)', symbol: 'CFA', code: 'XAF' },
    { country: 'Congo (Kinshasa)', symbol: 'CDF', code: 'CDF' },
    { country: 'Costa Rica', symbol: '₡', code: 'CRC' },
    { country: 'Croatia', symbol: '€', code: 'EUR' },
    { country: 'Cuba', symbol: 'CUP', code: 'CUP' },
    { country: 'Cyprus', symbol: '€', code: 'EUR' },
    { country: 'Czech Republic', symbol: 'Kč', code: 'CZK' },
    { country: 'Denmark', symbol: 'kr', code: 'DKK' },
    { country: 'Djibouti', symbol: 'Fdj', code: 'DJF' },
    { country: 'Dominica', symbol: 'EC$', code: 'XCD' },
    { country: 'Dominican Republic', symbol: 'RD$', code: 'DOP' },
    { country: 'Ecuador', symbol: 'US$', code: 'USD' },
    { country: 'Egypt', symbol: 'E£', code: 'EGP' },
    { country: 'El Salvador', symbol: 'US$', code: 'USD' },
    { country: 'Equatorial Guinea', symbol: 'CFA', code: 'XAF' },
    { country: 'Eritrea', symbol: 'Nkf', code: 'ERN' },
    { country: 'Estonia', symbol: '€', code: 'EUR' },
    { country: 'Eswatini', symbol: 'SZL', code: 'SZL' },
    { country: 'Ethiopia', symbol: 'Br', code: 'ETB' },
    { country: 'Fiji', symbol: 'FJ$', code: 'FJD' },
    { country: 'Finland', symbol: '€', code: 'EUR' },
    { country: 'France', symbol: '€', code: 'EUR' },
    { country: 'Gabon', symbol: 'CFA', code: 'XAF' },
    { country: 'Gambia', symbol: 'D', code: 'GMD' },
    { country: 'Georgia', symbol: '₾', code: 'GEL' },
    { country: 'Germany', symbol: '€', code: 'EUR' },
    { country: 'Ghana', symbol: '₵', code: 'GHS' },
    { country: 'Greece', symbol: '€', code: 'EUR' },
    { country: 'Grenada', symbol: 'EC$', code: 'XCD' },
    { country: 'Guatemala', symbol: 'Q', code: 'GTQ' },
    { country: 'Guinea', symbol: 'GNF', code: 'GNF' },
    { country: 'Guinea-Bissau', symbol: 'CFA', code: 'XOF' },
    { country: 'Guyana', symbol: 'GY$', code: 'GYD' },
    { country: 'Haiti', symbol: 'G', code: 'HTG' },
    { country: 'Honduras', symbol: 'L', code: 'HNL' },
    { country: 'Hungary', symbol: 'Ft', code: 'HUF' },
    { country: 'Iceland', symbol: 'ISK', code: 'ISK' },
    { country: 'India', symbol: '₹', code: 'INR' },
    { country: 'Indonesia', symbol: 'Rp', code: 'IDR' },
    { country: 'Iran', symbol: '﷼', code: 'IRR' },
    { country: 'Iraq', symbol: 'ع.د', code: 'IQD' },
    { country: 'Ireland', symbol: '€', code: 'EUR' },
    { country: 'Israel', symbol: '₪', code: 'ILS' },
    { country: 'Italy', symbol: '€', code: 'EUR' },
    { country: 'Jamaica', symbol: 'J$', code: 'JMD' },
    { country: 'Japan', symbol: '¥', code: 'JPY' },
    { country: 'Jordan', symbol: 'JD', code: 'JOD' },
    { country: 'Kazakhstan', symbol: '₸', code: 'KZT' },
    { country: 'Kenya', symbol: 'KSh', code: 'KES' },
    { country: 'Kiribati', symbol: 'AU$', code: 'AUD' },
    { country: 'Korea Selatan', symbol: '₩', code: 'KRW' },
    { country: 'Kuwait', symbol: 'KD', code: 'KWD' },
    { country: 'Kyrgyzstan', symbol: 'лв', code: 'KGS' },
    { country: 'Laos', symbol: '₭', code: 'LAK' },
    { country: 'Latvia', symbol: '€', code: 'EUR' },
    { country: 'Lebanon', symbol: 'ل.ل', code: 'LBP' },
    { country: 'Lesotho', symbol: 'LSL', code: 'LSL' },
    { country: 'Liberia', symbol: 'L$', code: 'LRD' },
    { country: 'Libya', symbol: 'LD', code: 'LYD' },
    { country: 'Liechtenstein', symbol: 'CHF', code: 'CHF' },
    { country: 'Lithuania', symbol: '€', code: 'EUR' },
    { country: 'Luxembourg', symbol: '€', code: 'EUR' },
    { country: 'Madagascar', symbol: 'Ar', code: 'MGA' },
    { country: 'Malawi', symbol: 'MK', code: 'MWK' },
    { country: 'Malaysia', symbol: 'RM', code: 'MYR' },
    { country: 'Maldives', symbol: 'Rf', code: 'MVR' },
    { country: 'Mali', symbol: 'CFA', code: 'XOF' },
    { country: 'Malta', symbol: '€', code: 'EUR' },
    { country: 'Marshall Islands', symbol: 'US$', code: 'USD' },
    { country: 'Mauritania', symbol: 'UM', code: 'MRU' },
    { country: 'Mauritius', symbol: '₨', code: 'MUR' },
    { country: 'Mexico', symbol: 'Mex$', code: 'MXN' },
    { country: 'Micronesia', symbol: 'US$', code: 'USD' },
    { country: 'Moldova', symbol: 'L', code: 'MDL' },
    { country: 'Monaco', symbol: '€', code: 'EUR' },
    { country: 'Mongolia', symbol: '₮', code: 'MNT' },
    { country: 'Montenegro', symbol: '€', code: 'EUR' },
    { country: 'Morocco', symbol: 'MAD', code: 'MAD' },
    { country: 'Mozambique', symbol: 'MT', code: 'MZN' },
    { country: 'Namibia', symbol: 'N$', code: 'NAD' },
    { country: 'Nauru', symbol: 'AU$', code: 'AUD' },
    { country: 'Nepal', symbol: '₨', code: 'NPR' },
    { country: 'Netherlands', symbol: '€', code: 'EUR' },
    { country: 'New Zealand', symbol: 'NZ$', code: 'NZD' },
    { country: 'Nicaragua', symbol: 'C$', code: 'NIO' },
    { country: 'Niger', symbol: 'CFA', code: 'XOF' },
    { country: 'Nigeria', symbol: '₦', code: 'NGN' },
    { country: 'North Korea', symbol: '₩', code: 'KPW' },
    { country: 'North Macedonia', symbol: 'ден', code: 'MKD' },
    { country: 'Norway', symbol: 'kr', code: 'NOK' },
    { country: 'Oman', symbol: 'OMR', code: 'OMR' },
    { country: 'Pakistan', symbol: '₨', code: 'PKR' },
    { country: 'Palau', symbol: 'US$', code: 'USD' },
    { country: 'Panama', symbol: 'B/.', code: 'PAB' },
    { country: 'Papua New Guinea', symbol: 'K', code: 'PGK' },
    { country: 'Paraguay', symbol: '₲', code: 'PYG' },
    { country: 'Peru', symbol: 'S/', code: 'PEN' },
    { country: 'Philippines', symbol: '₱', code: 'PHP' },
    { country: 'Poland', symbol: 'zł', code: 'PLN' },
    { country: 'Portugal', symbol: '€', code: 'EUR' },
    { country: 'Qatar', symbol: 'QR', code: 'QAR' },
    { country: 'Romania', symbol: 'lei', code: 'RON' },
    { country: 'Russia', symbol: '₽', code: 'RUB' },
    { country: 'Rwanda', symbol: 'FRw', code: 'RWF' },
    { country: 'Saint Kitts and Nevis', symbol: 'EC$', code: 'XCD' },
    { country: 'Saint Lucia', symbol: 'EC$', code: 'XCD' },
    { country: 'Saint Vincent and the Grenadines', symbol: 'EC$', code: 'XCD' },
    { country: 'Samoa', symbol: 'WS$', code: 'WST' },
    { country: 'San Marino', symbol: '€', code: 'EUR' },
    { country: 'Sao Tome and Principe', symbol: 'Db', code: 'STN' },
    { country: 'Saudi Arabia', symbol: 'SR', code: 'SAR' },
    { country: 'Senegal', symbol: 'CFA', code: 'XOF' },
    { country: 'Serbia', symbol: 'дин', code: 'RSD' },
    { country: 'Seychelles', symbol: 'SR', code: 'SCR' },
    { country: 'Sierra Leone', symbol: 'Le', code: 'SLE' },
    { country: 'Singapore', symbol: 'S$', code: 'SGD' },
    { country: 'Slovakia', symbol: '€', code: 'EUR' },
    { country: 'Slovenia', symbol: '€', code: 'EUR' },
    { country: 'Solomon Islands', symbol: 'SI$', code: 'SBD' },
    { country: 'Somalia', symbol: 'Sh.so', code: 'SOS' },
    { country: 'South Africa', symbol: 'R', code: 'ZAR' },
    { country: 'South Sudan', symbol: 'SSP', code: 'SSP' },
    { country: 'Spain', symbol: '€', code: 'EUR' },
    { country: 'Sri Lanka', symbol: 'Rs', code: 'LKR' },
    { country: 'Sudan', symbol: 'SDG', code: 'SDG' },
    { country: 'Suriname', symbol: 'SRD', code: 'SRD' },
    { country: 'Sweden', symbol: 'kr', code: 'SEK' },
    { country: 'Switzerland', symbol: 'CHF', code: 'CHF' },
    { country: 'Syria', symbol: '£S', code: 'SYP' },
    { country: 'Taiwan', symbol: 'NT$', code: 'TWD' },
    { country: 'Tajikistan', symbol: 'ЅМ', code: 'TJS' },
    { country: 'Tanzania', symbol: 'TSh', code: 'TZS' },
    { country: 'Thailand', symbol: '฿', code: 'THB' },
    { country: 'Timor-Leste', symbol: 'US$', code: 'USD' },
    { country: 'Togo', symbol: 'CFA', code: 'XOF' },
    { country: 'Tonga', symbol: 'T$', code: 'TOP' },
    { country: 'Trinidad and Tobago', symbol: 'TT$', code: 'TTD' },
    { country: 'Tunisia', symbol: 'DT', code: 'TND' },
    { country: 'Turkey', symbol: '₺', code: 'TRY' },
    { country: 'Turkmenistan', symbol: 'm', code: 'TMT' },
    { country: 'Tuvalu', symbol: 'AU$', code: 'AUD' },
    { country: 'Uganda', symbol: 'USh', code: 'UGX' },
    { country: 'Ukraine', symbol: '₴', code: 'UAH' },
    { country: 'United Arab Emirates', symbol: 'AED', code: 'AED' },
    { country: 'United Kingdom', symbol: '£', code: 'GBP' },
    { country: 'United States', symbol: 'US$', code: 'USD' },
    { country: 'Uruguay', symbol: '$U', code: 'UYU' },
    { country: 'Uzbekistan', symbol: 'so\'m', code: 'UZS' },
    { country: 'Vanuatu', symbol: 'VT', code: 'VUV' },
    { country: 'Vatican City', symbol: '€', code: 'EUR' },
    { country: 'Venezuela', symbol: 'Bs.', code: 'VES' },
    { country: 'Vietnam', symbol: '₫', code: 'VND' },
    { country: 'Yemen', symbol: '﷼', code: 'YER' },
    { country: 'Zambia', symbol: 'ZK', code: 'ZMW' },
    { country: 'Zimbabwe', symbol: 'Z$', code: 'ZWL' }
];

function checkFirstTimeSetup() {
    if (!localStorage.getItem('isSetupComplete')) {
        displaySetupModal();
    } else {
        const companyName = localStorage.getItem('companyName');
        if (companyName) {
            document.querySelector('.app-title').textContent = companyName;
        }
    }
}

// script.js

// GANTI FUNGSI LAMA ANDA DENGAN VERSI BARU DAN LENGKAP INI

function displaySetupModal() {
    const modal = document.getElementById('setup-modal-overlay');
    if (!modal) {
        console.error("Error: Modal element not found.");
        return;
    }

    // Tampilkan modal terlebih dahulu
    modal.style.display = 'flex';

    // Panggil fungsi untuk mengisi daftarnya
    populateCurrencyList();

    // --- Logika untuk interaksi dropdown ---
    const dropdownContainer = document.getElementById('custom-currency-dropdown');
    const selectedDisplay = dropdownContainer.querySelector('.dropdown-selected-display');
    const optionsWrapper = dropdownContainer.querySelector('.dropdown-options-wrapper');
    const searchInput = document.getElementById('currency-search-input');

    // Menambahkan event listener untuk menampilkan/menyembunyikan menu
    selectedDisplay.addEventListener('click', () => {
        optionsWrapper.classList.toggle('visible');
        selectedDisplay.classList.toggle('open');
    });

    // Event listener untuk fungsionalitas pencarian
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        document.querySelectorAll('#currency-options-list li').forEach(item => {
            const countryName = item.textContent.toLowerCase();
            item.style.display = countryName.includes(searchTerm) ? 'block' : 'none';
        });
    });

    // Event listener untuk menutup dropdown jika pengguna mengklik di luar area dropdown
    document.addEventListener('click', (e) => {
        // Cek apakah yang di-klik bukan bagian dari container dropdown
        if (!dropdownContainer.contains(e.target)) {
            optionsWrapper.classList.remove('visible');
            selectedDisplay.classList.remove('open');
        }
    });
}

function populateCurrencyList() {
    const listElement = document.getElementById('currency-options-list');
    if(!listElement) return; // Pengaman jika elemen tidak ada
    
    listElement.innerHTML = ''; // Kosongkan dulu

    currencyData.forEach(currency => {
        const listItem = document.createElement('li');
        listItem.textContent = `${currency.country} (${currency.symbol})`;
        listItem.dataset.info = JSON.stringify(currency);

        listItem.addEventListener('click', () => {
            listElement.querySelector('li.selected')?.classList.remove('selected');
            listItem.classList.add('selected');
            document.getElementById('selected-currency-text').textContent = listItem.textContent;
            selectedCurrency = currency;
            listElement.parentElement.classList.remove('visible');
            document.querySelector('.dropdown-selected-display').classList.remove('open');
            if (document.getElementById('company-name-input').value.trim()) {
                document.getElementById('save-setup-btn').disabled = false;
            }
        });
        listElement.appendChild(listItem);
    });
}

function saveSetup() {
    const companyName = document.getElementById('company-name-input').value.trim();
    if (!companyName || !selectedCurrency) {
        alert('Nama perusahaan dan mata uang harus diisi!');
        return;
    }

    fetch('/setup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company_name: companyName, currency_info: selectedCurrency })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem('isSetupComplete', 'true');
            localStorage.setItem('companyName', companyName);
            localStorage.setItem('currencyInfo', JSON.stringify(selectedCurrency));
            document.getElementById('setup-modal-overlay').style.display = 'none';
            showMessage('Penyiapan berhasil!', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showMessage('Gagal menyimpan penyiapan.', 'error');
        }
    })
    .catch(error => showMessage('Terjadi kesalahan jaringan: ' + error, 'error'));
}

// Modifikasi juga fungsi formatCurrency Anda menjadi dinamis
function formatCurrency(amount) {
    const currencyInfo = JSON.parse(localStorage.getItem('currencyInfo')) || { code: 'IDR' };
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: currencyInfo.code,
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(amount);
}

// Ganti atau buat event listener DOMContentLoaded yang baru
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadTranslations();
    loadExpenseTypes();
    checkFirstTimeSetup();
    if (localStorage.getItem('isSetupComplete')) {
        showPage('home');
    }
});

// script.js

// ... (di dalam event listener DOMContentLoaded atau di scope global)

// Event listener untuk form PPE
document.getElementById('ppe-form')?.addEventListener('submit', handlePpeFormSubmit);

// Tampilkan/sembunyikan field khusus UoP



// --- FUNGSI-FUNGSI BARU UNTUK PPE ---

// script.js
// script.js

function loadPpeAssets() {
    const tableBody = document.getElementById('ppe-table-body');
    tableBody.innerHTML = `<tr><td colspan="7" class="text-center"><i class="fas fa-spinner fa-spin"></i> Memuat data aset...</td></tr>`;

    fetch('/get_ppe_assets')
    .then(response => {
        // Cek jika server merespons dengan error (seperti 500 Internal Server Error)
        if (!response.ok) {
            throw new Error(`Server Error: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        // Hapus indikator loading
        tableBody.innerHTML = '';
        
        if (!data || data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="7" class="text-center">Belum ada aset tetap yang ditambahkan.</td></tr>';
            return;
        }

        data.forEach(asset => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${asset.name}</td>
                <td>${asset.category}</td>
                <td>${asset.purchase_date}</td>
                <td>${formatCurrency(asset.cost)}</td>
                <td>${formatCurrency(asset.book_value)}</td>
                <td>${asset.depreciation_method.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</td>
                <td>
                    <button class="btn btn-info btn-sm" onclick="showDepreciationSchedule(${asset.id})" title="Lihat Jadwal">
                        <i class="fas fa-list-alt"></i> Detail
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deletePpeAsset(${asset.id})" title="Hapus Aset">
                        <i class="fas fa-trash-alt"></i> Hapus
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        // Ini blok baru yang akan menangani semua jenis error (koneksi, server, dll)
        console.error('Gagal memuat aset PPE:', error);
        tableBody.innerHTML = `<tr><td colspan="7" class="text-center text-danger"><strong>Gagal Memuat Data.</strong><br><small>Coba refresh halaman atau periksa log server.</small></td></tr>`;
    });
}

// GANTI SELURUH FUNGSI LAMA ANDA DENGAN BLOK BARU INI

// script.js

function deletePpeAsset(assetId) {
    alert('Fungsi Hapus untuk aset ID ' + assetId + ' belum diimplementasikan.');
}

function handlePpeFormSubmit(event) {
    event.preventDefault(); // Mencegah halaman refresh

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    if (data.depreciation_method === 'uop') {
        data.uop_details = {
            total_units: data.uop_total_units
        };
    }

    fetch('/add_ppe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showMessage(result.message, 'success');
            
            const ppeModalEl = document.getElementById('ppe-form-modal');
            
            // ▼▼▼ INI ADALAH CARA YANG PALING BENAR DAN STABIL ▼▼▼

            // 1. Daftarkan sebuah "pendengar" yang akan aktif TEPAT SETELAH modal benar-benar hilang (termasuk backdrop-nya)
            ppeModalEl.addEventListener('hidden.bs.modal', () => {
                // 3. Setelah modal hilang, baru kita muat ulang data tabelnya
                loadPpeAssets();
            }, { once: true }); // Opsi { once: true } memastikan perintah ini hanya berjalan sekali dan tidak menumpuk

            // 2. Sekarang, perintahkan modal untuk memulai proses penutupan
            const modalInstance = bootstrap.Modal.getInstance(ppeModalEl);
            if (modalInstance) {
                modalInstance.hide();
            }

        } else {
            showMessage(result.message, 'error');
        }
    })
    .catch(error => {
        console.error("Error submitting PPE form:", error);
        showMessage("Terjadi kesalahan koneksi saat menyimpan.", "error");
    });
}

function showDepreciationSchedule(assetId) {
    fetch(`/get_depreciation_schedule/${assetId}`)
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            document.getElementById('schedule-modal-title').textContent = `Jadwal Depresiasi - ${result.asset.name}`;
            const scheduleBody = document.getElementById('depreciation-schedule-body');
            scheduleBody.innerHTML = '';
            result.schedule.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row.period}</td>
                    <td>${formatCurrency(row.beginning_book_value)}</td>
                    <td>${formatCurrency(row.depreciation_expense)}</td>
                    <td>${formatCurrency(row.accumulated_depreciation)}</td>
                    <td>${formatCurrency(row.ending_book_value)}</td>
                    <td><span class="badge bg-${row.status === 'Recorded' ? 'success' : 'secondary'}">${row.status}</span></td>
                `;
                scheduleBody.appendChild(tr);
            });
            new bootstrap.Modal(document.getElementById('depreciation-schedule-modal')).show();
        } else {
            showMessage(result.message, 'error');
        }
    });
}

function previewPeriodDepreciation() {
    const period = document.getElementById('depreciation-period-select').value;
    if (!period) {
        showMessage('Silakan pilih periode.', 'error');
        return;
    }

    fetch('/preview_period_depreciation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ period: period })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success && result.preview_data.length > 0) {
            const previewBody = document.getElementById('depreciation-preview-body');
            previewBody.innerHTML = '';
            result.preview_data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.name}</td>
                    <td>${item.category}</td>
                    <td>${formatCurrency(item.depreciation_expense)}</td>
                `;
                previewBody.appendChild(row);
            });

            document.getElementById('depreciation-preview-title').textContent = `Konfirmasi Pencatatan Depresiasi Tahun ${period}`;

            const previewModalEl = document.getElementById('depreciation-preview-modal');
            const previewModal = new bootstrap.Modal(previewModalEl);
            
            const confirmBtn = document.getElementById('confirm-record-depreciation-btn');
            // Clone and replace to remove old event listeners safely
            const newConfirmBtn = confirmBtn.cloneNode(true);
            confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);

            newConfirmBtn.addEventListener('click', () => {
                confirmAndRecordDepreciation(period);
                previewModal.hide();
            }, { once: true });

            previewModal.show();

        } else {
            showMessage(result.message || 'Tidak ada depresiasi untuk dicatat pada periode ini.', 'info');
        }
    })
    .catch(error => {
        console.error("Error fetching depreciation preview:", error);
        showMessage("Terjadi kesalahan saat mengambil data preview.", "error");
    });
}

function confirmAndRecordDepreciation(period) {
    fetch('/record_period_depreciation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ period: period })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showMessage(result.message, 'success');
            loadPpeAssets(); // Muat ulang nilai buku
        } else {
            showMessage(result.message, 'error');
        }
    });
}

function populateDepreciationPeriodSelect() {
    const select = document.getElementById('depreciation-period-select');
    const currentYear = new Date().getFullYear();
    for (let i = 0; i < 5; i++) {
        const year = currentYear - i;
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        select.appendChild(option);
    }
}

function loadDepreciationHistory() {
     fetch('/get_depreciation_history')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('depreciation-history-body');
        tableBody.innerHTML = '';
        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" class="text-center">Belum ada riwayat.</td></tr>';
            return;
        }
        data.forEach(rec => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${rec.date_recorded}</td>
                <td>${rec.asset_name}</td>
                <td>${rec.period}</td>
                <td>${formatCurrency(rec.amount)}</td>
            `;
            tableBody.appendChild(row);
        });
    });
}


// Terakhir, panggil fungsi-fungsi ini saat halaman PPE ditampilkan
// Di dalam fungsi showPage(pageId) yang sudah ada:
// case 'ppe':
//    loadPpeAssets();
//    populateDepreciationPeriodSelect();
//    break;

// Modifikasi juga fungsi formatCurrency Anda menjadi dinamis
function formatCurrency(amount) {
    const currencyInfo = JSON.parse(localStorage.getItem('currencyInfo')) || { code: 'IDR' };
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: currencyInfo.code,
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(amount);
}

// Ganti atau buat event listener DOMContentLoaded yang baru
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadTranslations();
    loadExpenseTypes();
    checkFirstTimeSetup();
    if (localStorage.getItem('isSetupComplete')) {
        showPage('home');
    }
});
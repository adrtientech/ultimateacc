# File: data_manager.py
# Tugas: Menyimpan dan memuat data aplikasi dari/ke file JSON.

import json
from collections import defaultdict

def save_app_data(data_to_save, filename):
    """Menyimpan seluruh data aplikasi (variabel app_data) ke file JSON."""
    try:
        # Penting: json.dump tidak bisa menangani defaultdict secara langsung.
        # Kita ubah dulu general_ledger menjadi dict biasa sebelum menyimpan.
        if 'general_ledger' in data_to_save and isinstance(data_to_save['general_ledger'], defaultdict):
            data_to_save['general_ledger'] = dict(data_to_save['general_ledger'])

        with open(filename, 'w', encoding='utf-8') as f:
            # indent=4 agar file JSON mudah dibaca
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        print(f"✅ Data aplikasi berhasil disimpan ke {filename}")
        return True
    except Exception as e:
        print(f"❌ Gagal menyimpan data: {e}")
        return False

def load_app_data(filename):
    """Memuat data aplikasi dari file JSON."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        # Penting: Setelah dimuat, kita ubah kembali general_ledger menjadi defaultdict.
        # Ini penting agar kode Anda yang lain tetap berfungsi normal.
        if 'general_ledger' in loaded_data:
            # Memberikan list kosong sebagai default factory untuk kunci yang tidak ada
            loaded_data['general_ledger'] = defaultdict(list, loaded_data['general_ledger'])

        # Pastikan account_balances juga defaultdict(float)
        if 'account_balances' in loaded_data:
            loaded_data['account_balances'] = defaultdict(float, loaded_data['account_balances'])

        print(f"✅ Data aplikasi berhasil dimuat dari {filename}")
        return loaded_data
    except FileNotFoundError:
        print(f"ℹ️ File data '{filename}' tidak ditemukan. Memulai dengan data baru.")
        return None # Mengembalikan None jika file tidak ada
    except Exception as e:
        print(f"❌ Gagal memuat data: {e}")
        return None
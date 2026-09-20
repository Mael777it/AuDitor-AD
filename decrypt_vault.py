#!/usr/bin/env python3
# AuDitor-AD
# Copyright (c) 2026 Marcin Lewandowski <marcin.lewandowski.x@gmail.com>
# SPDX-License-Identifier: MIT
# https://github.com/mael777it/AuDitor-AD
"""Awaryjne odszyfrowanie sejfu AuDitor-AD (auditor-ad.vault.json) bez przeglądarki.
Obsługuje też sejfy z poprzedniej wersji (ad_assessment.vault.json, format "adsec-vault").

Użycie:
    pip install cryptography
    python3 decrypt_vault.py auditor-ad.vault.json             # podsumowanie domen
    python3 decrypt_vault.py auditor-ad.vault.json -o out.json # zapis JAWNEGO JSON-a (dane wrażliwe!)
"""
import argparse, base64, getpass, json, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

ap = argparse.ArgumentParser()
ap.add_argument("vault")
ap.add_argument("-o", "--out", help="zapisz odszyfrowany JSON do pliku")
a = ap.parse_args()

f = json.load(open(a.vault, encoding="utf-8"))
if f.get("format") not in ("auditor-ad-vault", "adsec-vault"):
    sys.exit("To nie jest plik sejfu AuDitor-AD")
kdf = f["kdf"]
key = PBKDF2HMAC(hashes.SHA256(), 32, base64.b64decode(kdf["salt"]), kdf["iter"]).derive(
    getpass.getpass("Hasło do sejfu: ").encode())
try:
    data = json.loads(AESGCM(key).decrypt(base64.b64decode(f["iv"]), base64.b64decode(f["ct"]), None))
except InvalidTag:
    sys.exit("Nieprawidłowe hasło lub uszkodzony plik")

doms = data.get("domains", [])
print(f"Zapisano: {data.get('saved')} · domen: {len(doms)}")
for d in doms:
    st = [v.get("status") for v in d.get("ctl", {}).values()]
    print(f"  {d.get('name'):<30} niezgodne: {st.count('fail'):>3}  częściowo: {st.count('part'):>3}  zgodne: {st.count('ok'):>3}  konta: {len(d.get('accounts', []))}")
if a.out:
    json.dump(data, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Zapisano jawny JSON: {a.out} – usuń go po użyciu.")

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/auditor-ad-logo-dark.svg">
    <img src="assets/auditor-ad-logo.svg" alt="AuDitor-AD" width="420">
  </picture>
</p>

<p align="center">
  Lokalna aplikacja do oceny bezpieczeństwa <b>Active Directory</b>, <b>PKI (AD CS)</b> i utwardzenia końcówek – osobno dla każdej domeny,<br>
  z raportem dla administratorów i dla managementu. Jeden plik HTML, bez serwera, dane w zaszyfrowanym sejfie.
</p>

<p align="center">
  <img alt="Licencja MIT" src="https://img.shields.io/badge/licencja-MIT-D7263D">
  <img alt="Wersja" src="https://img.shields.io/badge/wersja-1.0.0-1B1F24">
  <a href="https://github.com/mael777it/AuDitor-AD"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-mael777it%2FAuDitor--AD-1B1F24?logo=github"></a>
</p>

---

## Pliki

| Plik | Opis |
|---|---|
| `auditor-ad.html` | Aplikacja. Otwierasz ją w Chromium, Chrome albo Edge. Katalog kontroli jest wbudowany. |
| `ad_controls.csv` | Katalog 93 kontroli (separator `;`). Można go edytować i wczytać w Ustawieniach. |
| `decrypt_vault.py` | Awaryjne odczytanie sejfu bez przeglądarki. Wymaga `pip install cryptography`. |
| `assets/` | Logo (wersja jasna, ciemna i sam znak). |

## Praca

1. **Pierwsze uruchomienie:** wybierasz folder sejfu i ustawiasz hasło (min. 12 znaków). Dane trafiają do pliku `auditor-ad.vault.json` (AES-256-GCM, PBKDF2-SHA256 600 000 iteracji), a kopie zapasowe do `backups/`.
2. **+ Dodaj domenę:** każda domena ma własną ocenę, rejestr kont i plan naprawczy.
3. **Przegląd i mapa:** mapa pokrycia (kafelki według obszarów, kolor oznacza status), wskaźniki, dane domeny, wyniki narzędzi i pole **Podsumowanie dla kierownictwa**.
4. **Kontrole:** każdą kontrolę oznaczasz jako *Zgodne*, *Częściowo*, *Niezgodne* albo *N/D*. Po rozwinięciu widać opis, ryzyko biznesowe, sposób weryfikacji (PingCastle, BloodHound, Certipy, PowerShell), **instrukcję naprawy** oraz pola na ustalenia, obiekty, priorytet, właściciela, termin i uzasadnienie N/D lub akceptacji ryzyka. **+ Własne znalezisko** dodaje rzeczy spoza katalogu.
5. **Konta niebezpieczne:** rejestr kont z powodami (T0, Kerberoastable, AS-REP, delegacja, DCSync, ścieżka do DA, ESC, shadow credentials…). „Wklej wiele kont naraz” przydaje się do list z BloodHound.
6. **Plan naprawczy:** wszystkie niezgodności w jednej tabeli. Puste terminy można uzupełnić według priorytetu: P1 30 dni, P2 90, P3 180, P4 365 od daty oceny.
7. **Import narzędzi (pomocniczy):**
   - **PingCastle:** raport `ad_hc_<domena>.xml` – zmapowane reguły oznaczają kontrole jako niezgodne, niezmapowane trafiają jako własne znaleziska.
   - **Certipy:** plik z `certipy find -json` – podatności ESC1–ESC16 oznaczają kontrole PKI, a szablony i CA trafiają do pola „obiekty”.
   - Import zawsze najpierw pokazuje podgląd. **Mapowanie reguł PingCastle jest orientacyjne** – nazwy reguł zmieniają się między wersjami; w razie potrzeby popraw kolumnę `pingcastle` w CSV.
8. **▦ Porównanie domen:** wskaźniki i zgodność według obszarów obok siebie, macierz kontroli × domeny (eksport CSV).

## Raporty

**Raport** → wybierasz domenę albo zestawienie wszystkich domen, odbiorcę i klauzulę. Wydruk do PDF, HTML, Markdown lub plan w CSV.

- **Zarządczy:** ocena A–E z interpretacją, kluczowe wskaźniki, stan według obszarów, najważniejsze ryzyka językiem biznesowym, harmonogram P1–P4, działania wymagające decyzji lub budżetu, zaakceptowane ryzyka. Wersja „wszystkie domeny” pokazuje problemy wspólne dla wielu domen.
- **Techniczny:** każde znalezisko z ustaleniami, obiektami, weryfikacją, krokami konfiguracji i wpływem wdrożenia, rejestr kont, lista N/D, kontrole nieocenione.

**Ocena A–E** to zgodność ważona ryzykiem. Wagi: Krytyczne 10, Wysokie 5, Średnie 2, Niskie 1. Punkty: Zgodne 1, Częściowo 0,5, Niezgodne 0. Progi: A ≥ 90%, B ≥ 75%, C ≥ 60%, D ≥ 40%, poniżej E. Otwarta niezgodność krytyczna ogranicza ocenę do maks. C. Poniżej 70% pokrycia ocena jest oznaczana jako niepełna.

## Katalog (CSV)

Kolumny: `id; area; title; risk; effort; description; business_risk; check; sources; pingcastle; certipy; remediation; impact; mitre`.
Nie zmieniaj `id` kontroli w trwających ocenach – stan kontroli jest przypisany do jej ID.

## Przejście z „AD Security Assessment”

AuDitor-AD otwiera sejfy poprzedniej wersji bez żadnej konwersji. Jeśli w folderze jest tylko `ad_assessment.vault.json`, aplikacja go odczyta i od tej chwili zapisuje dane do `auditor-ad.vault.json`. Stary plik zostaje nietknięty – po sprawdzeniu możesz go usunąć. `decrypt_vault.py` obsługuje oba formaty.

## Bezpieczeństwo danych

- W sejfie są dane bardzo wrażliwe: ścieżki ataku i podatne konta. Trzymaj go na zaszyfrowanym dysku, a raporty techniczne udostępniaj tylko właściwym administratorom.
- **Repozytorium zawiera wyłącznie kod.** `.gitignore` wyklucza sejfy, kopie zapasowe, eksporty jawne, raporty i wyniki narzędzi – nie commituj danych żadnej organizacji.
- Instrukcje naprawy to punkt wyjścia. Zmiany (NTLM, RC4, podpisywanie LDAP/SMB, Credential Guard, WDAC) wdrażaj najpierw w trybie audytu lub pilotażu.

## Autor i licencja

**AuDitor-AD** – autor i twórca: **Marcin Lewandowski** ([@mael777it](https://github.com/mael777it)).
Repozytorium: https://github.com/mael777it/AuDitor-AD
Udostępnione na licencji [MIT](LICENSE) – możesz używać, modyfikować i rozpowszechniać, zachowując informację o prawach autorskich.

Logotyp korzysta z kroju Poppins (SIL Open Font License 1.1), zamienionego na krzywe.

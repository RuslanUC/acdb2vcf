# Android Contacts Database To VCF
Tools to extract data from *Android Contacts Database* (*SQLite3*). By default, it's located at */data/data/com.android.providers.contacts/databases/contacts2.db* although some manufacturers may change it.

The easy way to get *contacts2.db* is using [*adb*](https://developer.android.com/studio/releases/platform-tools) tool:
   ```bash
   $# adb pull /data/data/com.android.providers.contacts/databases/contacts2.db
   ```

More information about *Android Contacts Database* can be found on:
- [Android Contacts Database Structure](https://www.dev2qa.com/android-contacts-database-structure/)
- [Contacts Provider](https://developer.android.com/guide/topics/providers/contacts-provider)


## [acdb2vcf.py](https://github.com/RuslanUC/acdb2vcf/blob/master/acdb2vcf.py)
*Python* tool by to export contacts data from *Android Contacts Databases* (*SQLite3*) to *vCard 3.0* text files. It's useful to recover contacts data from an *Android* phone (*contacts2.db*) into *Google Contacts* or other services supporting *vCard* file format (.vcf).

*acdb2vcf.py* v2.0 supports:
- *Android Contacts Database* format (*SQLite3*).
- Account type filtering: *Google*, *Exchange*, *WhatsApp*, *Telegram*, *Phone*, *SIM*, ...
- Custom account types
- N, FN, ADR, BDAY, EMAIL, NOTE, ORG, ROLE, TEL properties from *vCard 3.0* standard.

### Usage
```
usage: acdb2vcf.py [-h] [--all] [--exchange] [--google] [--imap] [--phone] [--sim] [--telegram] [--tuenti] [--twitter] [--whatsapp] [--list-accounts] [--account [ACCOUNTS ...]] db_path [vcf_path]

positional arguments:
  db_path               Path to input contacts2.db
  vcf_path              Path to output vcf file

options:
  -h, --help            show this help message and exit
  --all, -a             Export all accounts
  --exchange            Export contacts associated with "exchange" account
  --google              Export contacts associated with "google" account
  --imap                Export contacts associated with "imap" account
  --phone               Export contacts associated with "phone" account
  --sim                 Export contacts associated with "sim" account
  --telegram            Export contacts associated with "telegram" account
  --tuenti              Export contacts associated with "tuenti" account
  --twitter             Export contacts associated with "twitter" account
  --whatsapp            Export contacts associated with "whatsapp" account
  --list-accounts       Just list accounts
  --account [ACCOUNTS ...]
                        Export account that is not listed above
```

### Additional info
It's based on Python2 tool [AndroidContactsDatabase-tools](https://github.com/alejandrolopezparra/AndroidContactsDatabase-tools)

Information about *vCard 3.0* can be found at:
- [vCard 3.0 format specification](https://www.evenx.com/vcard-3-0-format-specification)
- [RFC2425: A MIME Content-Type for Directory Information](https://tools.ietf.org/html/rfc2425)
- [RFC2426: vCard MIME Directory Profile](https://tools.ietf.org/html/rfc2426.html)
- [Representing vCard Objects in RDF](https://www.w3.org/Submission/2010/SUBM-vcard-rdf-20100120/)
- [Wikipedia: vCard](https://en.wikipedia.org/wiki/VCard)

#!/usr/bin/env python3
import argparse

import sqlite3
from types import SimpleNamespace


known_account_types = {
    "exchange": "com.google.android.gm.exchange",
    "google": "com.google",
    "imap": "com.google.android.gm.legacyimap",
    "phone": "vnd.sec.contact.phone",
    "sim": "vnd.sec.contact.sim",
    "telegram": "org.telegram.messenger",
    "tuenti": "com.tuenti.messenger.auth",
    "twitter": "com.twitter.android.auth.login",
    "whatsapp": "com.whatsapp",
}


# Remove Line Breaks from strings
def remove_line_breaks(text: str | None) -> str | None:
    if text is not None:
        text = text.replace("\n"," ")
        text = text.replace("\r"," ")
    return text

# Contact class stores contacts data
class Contact:
    def __init__(self, id_: int):
        self._id = id_
        self._phone_numbers = []
        self._mail_addresses = []
        self._addresses = []
        self._name = ""
        self._lastname = ""
        self._firstname = ""
        self._org = ""
        self._role = ""
        self._note = ""
        self._bday = ""

    @property
    def id(self) -> int:
        return self._id

    def add_phone(self, number: str) -> None:
        if number is not None:
            self._phone_numbers.append(remove_line_breaks(number))

    def get_phones(self):
        return self._phone_numbers

    def add_mail(self, mail: str) -> None:
        if mail is not None:
            self._mail_addresses.append(remove_line_breaks(mail))

    def get_mails(self):
        return self._mail_addresses

    def add_address(self, address: str) -> None:
        if address is not None:
            self._addresses.append(remove_line_breaks(address))

    def get_addresses(self):
        return self._addresses

    @property
    def first_name(self) -> str:
        return self._firstname

    @first_name.setter
    def first_name(self, value: str | None) -> None:
        if value is not None:
            self._firstname = remove_line_breaks(value)

    @property
    def last_name(self) -> str:
        return self._lastname

    @last_name.setter
    def last_name(self, value: str | None) -> None:
        if value is not None:
            self._lastname = remove_line_breaks(value)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str | None) -> None:
        if value is not None:
            self._name = remove_line_breaks(value)

    @property
    def full_name(self):
        return self._name, self._lastname, self._firstname

    @property
    def note(self) -> str:
        return self._note

    @note.setter
    def note(self, value: str | None) -> None:
        if value is not None:
            self._note = remove_line_breaks(value)

    @property
    def birthday(self) -> str:
        return self._bday

    @birthday.setter
    def birthday(self, value: str | None) -> None:
        if value is not None:
            self._bday = remove_line_breaks(value)

    @property
    def org(self) -> str:
        return self._org

    @org.setter
    def org(self, value: str | None) -> None:
        if value is not None:
            self._org = remove_line_breaks(value)

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value: str | None) -> None:
        if value is not None:
            self._role = remove_line_breaks(value)

    def to_vcard(self):
        vcard = [
            # HEADER
            "BEGIN:VCARD",
            "VERSION:3.0",
            # N:
            f"N:{self._lastname};{self._firstname}"
        ]

        # FN:
        full_name = "?"
        if self.name != "":
            full_name = self.name
        elif len(self._lastname) > 0 and len(self._firstname) > 0:
            full_name = f"{self._firstname} {self._lastname}"
        elif len(self._lastname) > 0:
            full_name = self._lastname
        elif len(self._firstname) > 0:
            full_name = self._firstname
        vcard.append(f"FN:{full_name}")

        # TEL;
        for phone in self._phone_numbers:
            vcard.append(f"TEL;{phone}")

        # EMAIL;
        for mail in self._mail_addresses:
            vcard.append(f"EMAIL;{mail}")

        # ADR;
        for address in self._addresses:
            vcard.append(f"ADR;{address}")

        # ORG:
        if self._org:
            vcard.append(f"ORG:{self._org}")

        # ROLE:
        if self._role:
            vcard.append(f"ROLE:{self._role}")

        # NOTE:
        if self._note:
            vcard.append(f"NOTE:{self._note}")

        # BDAY:
        if self._bday:
            vcard.append(f"BDAY:{self._bday}")

        vcard.append("END:VCARD")
        return vcard


class ArgsNamespace(SimpleNamespace):
    all: bool
    list_accounts: bool
    accounts: list[str]
    db_path: str
    vcf_path: str


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", "-a", action="store_true", default=False, help="Export all accounts")
    for account_name, account_package in known_account_types.items():
        parser.add_argument(f"--{account_name}", action="append_const", dest="accounts", const=account_package,
                            help=f"Export contacts associated with \"{account_name}\" account")
    parser.add_argument("--list-accounts", action="store_true", default=False, help="Just list accounts")
    parser.add_argument("--account", required=False, action="extend", dest="accounts", nargs="*",
                        help="Export account that is not listed above")
    parser.add_argument("db_path", type=str, help="Path to input contacts2.db")
    parser.add_argument("vcf_path", type=str, nargs="?", help="Path to output vcf file")

    args = parser.parse_args(namespace=ArgsNamespace())

    conn = sqlite3.connect(args.db_path)
    cur = conn.cursor()

    if args.list_accounts or args.all:
        if args.all and args.accounts is None:
            args.accounts = []

        cur.execute("SELECT account_name, account_type FROM accounts")
        for account_name, account_type in cur:
            if args.all:
                args.accounts.append(account_type)
            else:
                print(f"{account_type} ({account_name})")

        if args.list_accounts:
            return

    if args.all:
        if args.accounts is None:
            args.accounts = []
        args.accounts.extend(known_account_types.values())

    if not args.accounts:
        print("No accounts specified!")
        return

    args.accounts = list(set(args.accounts))

    contacts: list[Contact] = []

    for account_package in args.accounts:
        cur.execute("SELECT _id, account_name FROM accounts WHERE account_type=?", (account_package,))
        for account_id, account_name in cur.fetchall():
            cur.execute("SELECT COUNT(*) FROM raw_contacts WHERE account_id=?", (account_id,))
            num_entries = cur.fetchone()[0]
            if not num_entries:
                continue

            print(f"Exporting {num_entries} contacts from {account_name}")

            cur.execute("SELECT _id FROM raw_contacts WHERE account_id=?", (account_id,))
            for raw_contact_id in cur:
                if raw_contact_id not in contacts:
                    contacts.append(Contact(raw_contact_id))

    mimetypes: dict[int, str] = {}
    cur.execute("SELECT _id, mimetype FROM mimetypes")
    for mimetype_id, mimetype_name in cur:
        mimetypes[mimetype_id] = mimetype_name

    for contact in contacts:
        # TODO: data11-data15 (photo, etc.)
        cur.execute(
            "SELECT mimetype_id, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10 "
            "FROM data "
            "WHERE raw_contact_id=?",
            contact.id
        )

        for mimetype_id, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10 in cur:
            if mimetype_id not in mimetypes:
                continue

            mimetype = mimetypes[mimetype_id]
            if mimetype == "vnd.android.cursor.item/email_v2":
                # TODO: verify that email is stored in data1
                contact.add_mail(f"type=INTERNET;type=WORK:{data1}")
            elif mimetype == "vnd.android.cursor.item/organization":
                # TODO: verify that org is stored in data1, data4 and data5
                org = data1
                role = data4
                org_unit = data5
                if org or org_unit:
                    contact.org = f"{org};{org_unit}"
                if role:
                    contact.role = role
            elif mimetype == "vnd.android.cursor.item/phone_v2":
                phone_number = data1
                phone_type = data2
                phone_type_string = "WORK"  # Work, by default
                if phone_type == "1" and len(phone_number) > 8:  # Home
                    phone_type_string = "HOME"
                elif phone_type == "2" and len(phone_number) > 8:  # Mobile
                    phone_type_string = "CELL"
                contact.add_phone(f"type={phone_type_string}:{phone_number}")
            elif mimetype == "vnd.android.cursor.item/name":
                contact.name = data1
                contact.first_name = data2
                contact.last_name = data3
            elif mimetype == "vnd.android.cursor.item/postal-address_v2":
                # TODO: verify that address is stored in data2, data4, data7, data8, data9 and data10
                address_type = data2
                street = data4
                locality = data7
                region = data8
                postal_code = data9
                country = data10
                type_string = "WORK"  # Work, by default
                if address_type == "1":  # Home
                    type_string = "HOME"
                contact.add_address(f"type={type_string}:;;{street};{locality};{region};{postal_code};{country}")
            elif mimetype == "vnd.android.cursor.item/note":
                # TODO: verify that note is stored in data1
                contact.note = data1
            elif mimetype == "vnd.com.miui.cursor.item/lunarBirthday":
                # TODO: verify that note is stored in data1
                contact.birthday = data1

            # TODO: add viber/telegram number

        vcard = "\n".join(contact.to_vcard())
        if args.vcf_path is None:
            print(vcard)
            print()
        else:
            with open(args.vcf_path, "w" if contact is contacts[0] else "a") as f:
                f.write(vcard)
                f.write("\n")


if __name__ == "__main__":
    main()

import sys
import sqlite3
import os
import json
import re

def list_table_columns(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        print(f"Table: {table}")
        cursor.execute(f"PRAGMA table_info('{table}')")
        columns = [row[1] for row in cursor.fetchall()]
        print("Columns:", ", ".join(columns))
        print()
    conn.close()

def export_verses_to_json(db_path, out_dir):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)
    # Get all sura numbers
    cursor.execute("SELECT DISTINCT sura FROM verses")
    suras = [row[0] for row in cursor.fetchall()]
    for sura in suras:
        cursor.execute("SELECT ayah, text FROM verses WHERE sura=? ORDER BY ayah", (sura,))
        verses = cursor.fetchall()
        ayah_dict = {str(ayah): text for ayah, text in verses}
        out_path = os.path.join(out_dir, f"{sura}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(ayah_dict, f, ensure_ascii=False, indent=4)
    conn.close()

def find_non_alphanumeric_in_json(out_dir):
    non_alnum_chars = set()
    for filename in os.listdir(out_dir):
        if filename.endswith(".json"):
            with open(os.path.join(out_dir, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                for text in data.values():
                    chars = set(re.findall(r'[^a-zA-Z0-9\s]', text))
                    non_alnum_chars.update(chars)
    print("Non-alphanumeric characters found:")
    print("".join(sorted(non_alnum_chars)))

def print_example_verses_for_special_chars(out_dir, special_chars):
    found = {ch: None for ch in special_chars}
    for filename in os.listdir(out_dir):
        if filename.endswith(".json"):
            sura = os.path.splitext(filename)[0]
            with open(os.path.join(out_dir, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                for ayah, text in data.items():
                    for ch in special_chars:
                        if found[ch] is None and ch in text:
                            found[ch] = (f"{sura}:{ayah}", text)
    for ch in special_chars:
        print(f"Character: {repr(ch)}")
        if found[ch]:
            ref, verse = found[ch]
            print(f"  Example ({ref}): {verse}")
        else:
            print("  Not found.")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sql2json.py <db_file_path> <out_dir>")
        sys.exit(1)
    db_path = sys.argv[1]
    out_dir = sys.argv[2]
    export_verses_to_json(db_path, out_dir)
    # After exporting, find non-alphanumeric characters
    find_non_alphanumeric_in_json(out_dir)
    # Print example verses for each special character
    special_chars = "!',-.:;?[]ÂâãéîûĩũȂ˹˺ḍḤḥṢṣṬẓ‎—‘’“”Ⱬ"
    print_example_verses_for_special_chars(out_dir, special_chars)

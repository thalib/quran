#!/usr/bin/env python3
"""
Convert comprehensive Surah data into Hugo markdown files.

This script processes detailed Surah data in a dictionary format with fields:
- name: Primary Arabic/transliterated name
- anglicized_names: List of alternative transliterated names
- english_names: List of English translations
- place: Place of revelation (Makkah/Madinah)
- title_refers: Verse references that explain the title
- juz: List of Juz (parts) the Surah spans

Each Surah is converted into a markdown file at:
{output_dir}/{sura_number}/_index.md

With comprehensive frontmatter containing all the above fields.
"""

import os
import re
from typing import List, Tuple, Optional, Dict, Any


def parse_surah_line(line: str) -> Optional[Tuple[int, str, str]]:
    """
    Parse a single line of Surah data.
    
    Args:
        line: Input line in format "{number} - {name} ({translation})"
        
    Returns:
        Tuple of (sura_number, surah_name, translation) or None if invalid
        
    Example:
        >>> parse_surah_line("1 - Al-Fatiha (The opener)")
        (1, "Al-Fatiha", "The opener")
    """
    # Remove any leading/trailing whitespace
    line = line.strip()
    if not line:
        return None
    
    # Pattern to match: number - name (translation)
    pattern = r'^(\d+)\s*-\s*([^(]+)\s*\(([^)]+)\)$'
    match = re.match(pattern, line)
    
    if not match:
        return None
    
    sura_number = int(match.group(1))
    surah_name = match.group(2).strip()
    translation = match.group(3).strip()
    
    return sura_number, surah_name, translation


def create_markdown_content(sura_info: dict, sura_number: int) -> str:
    """
    Generate markdown content with enhanced TOML frontmatter.
    
    Args:
        sura_info: Dictionary containing all Surah information
        sura_number: The Surah number
        
    Returns:
        Complete markdown content string
    """
    # Format arrays for TOML with proper escaping
    def format_toml_array(arr):
        """Format array for TOML with proper quote escaping."""
        escaped_items = [item.replace('"', '\\"').replace("'", "\\'") for item in arr]
        return '[' + ', '.join(f'"{item}"' for item in escaped_items) + ']'
    
    # Format string for TOML with proper escaping
    def format_toml_string(s):
        """Format string for TOML with proper quote escaping."""
        return s.replace('"', '\\"').replace("'", "\\'")
    
    titles_ar = format_toml_array(sura_info['anglicized_names'])
    titles_en = format_toml_array(sura_info['english_names'])
    juz_array = '[' + ', '.join(str(j) for j in sura_info['juz']) + ']'
    
    return f"""+++
weight = {sura_number}
title = "{format_toml_string(sura_info['name'])}"
en = "{format_toml_string(sura_info['english_names'][0] if sura_info['english_names'] else '')}"
titles_ar = {titles_ar}
titles_en = {titles_en}
place = "{format_toml_string(sura_info['place'])}"
title_refers = "{format_toml_string(sura_info['title_refers'])}"
juz = {juz_array}
+++
"""


def create_surah_files(data: dict, output_dir: str) -> None:
    """
    Process Surah data dictionary and create markdown files.
    
    Args:
        data: Dictionary containing comprehensive Surah data
        output_dir: Base directory where files will be created
        
    Raises:
        OSError: If directory creation or file writing fails
    """
    processed_count = 0
    skipped_count = 0
    
    for sura_number, sura_info in data.items():
        try:
            # Create directory structure
            surah_dir = os.path.join(output_dir, str(sura_number))
            os.makedirs(surah_dir, exist_ok=True)
            
            # Generate markdown content
            content = create_markdown_content(sura_info, sura_number)
            
            # Write to file
            file_path = os.path.join(surah_dir, '_index.md')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {file_path}")
            processed_count += 1
            
        except (KeyError, OSError) as e:
            print(f"Error processing Surah {sura_number}: {e}")
            skipped_count += 1
            continue
    
    print(f"\nProcessing complete!")
    print(f"Files created: {processed_count}")
    print(f"Entries skipped: {skipped_count}")


def main() -> None:
    """
    Main function to process the Surah data.
    """
    # Comprehensive Surah data structure with additional fields from Wikipedia
    surah_data = {
        1: {
            "name": "Al-Fatiha",
            "anglicized_names": ["Al-Hamd", "Al-Asas", "Al-Sab' al-Mathani"],
            "english_names": ["The Opening", "The Opening of the Divine Writ", "The Essence of the Divine Writ", "The Surah of Praise", "The Foundation of the Qur'an", "The Seven Oft-Repeated Verses"],
            "place": "Makkah",
            "title_refers": "Whole Surah",
            "juz": [1]
        },
        2: {
            "name": "Al-Baqarah",
            "anglicized_names": ["Al-Baqara"],
            "english_names": ["The Cow", "The Red Heifer"],
            "place": "Madinah",
            "title_refers": "v. 67-73",
            "juz": [1, 2, 3]
        },
        3: {
            "name": "Al 'Imran",
            "anglicized_names": ["Aal Imran"],
            "english_names": ["The Family of Imran", "The House of ʿImrān"],
            "place": "Madinah",
            "title_refers": "v. 33, 35",
            "juz": [3, 4]
        },
        4: {
            "name": "An-Nisa",
            "anglicized_names": ["An-Nisaa"],
            "english_names": ["The Women"],
            "place": "Madinah",
            "title_refers": "Whole Surah",
            "juz": [4, 5, 6]
        },
        5: {
            "name": "Al-Ma'idah",
            "anglicized_names": ["Al-'Uqud"],
            "english_names": ["The Table", "The Last Supper", "The Contracts"],
            "place": "Madinah",
            "title_refers": "v. 112-114",
            "juz": [6, 7]
        },
        6: {
            "name": "Al-An'am",
            "anglicized_names": ["Al-Anam"],
            "english_names": ["The Cattle"],
            "place": "Makkah",
            "title_refers": "v. 136",
            "juz": [7, 8]
        },
        7: {
            "name": "Al-A'raf",
            "anglicized_names": ["Al-Araf"],
            "english_names": ["The Heights", "The Faculty of Discernment"],
            "place": "Makkah",
            "title_refers": "v. 46, 48",
            "juz": [8, 9]
        },
        8: {
            "name": "Al-Anfal",
            "anglicized_names": ["Badr"],
            "english_names": ["The Spoils of War", "Badr"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [9, 10]
        },
        9: {
            "name": "At-Tawbah",
            "anglicized_names": ["Bara'a"],
            "english_names": ["Repentance", "Dissociation"],
            "place": "Madinah",
            "title_refers": "",
            "juz": [10, 11]
        },
        10: {
            "name": "Yunus",
            "anglicized_names": ["Younus"],
            "english_names": ["Jonah"],
            "place": "Makkah",
            "title_refers": "v. 98",
            "juz": [11]
        },
        11: {
            "name": "Hud",
            "anglicized_names": ["Hood"],
            "english_names": ["Hud"],
            "place": "Makkah",
            "title_refers": "v. 50-60",
            "juz": [11, 12]
        },
        12: {
            "name": "Yusuf",
            "anglicized_names": ["Yoosuf"],
            "english_names": ["Joseph"],
            "place": "Makkah",
            "title_refers": "Whole Surah",
            "juz": [12, 13]
        },
        13: {
            "name": "Ar-Ra'd",
            "anglicized_names": ["Ar-Raad"],
            "english_names": ["The Thunder"],
            "place": "Madinah",
            "title_refers": "v. 13",
            "juz": [13]
        },
        14: {
            "name": "Ibrahim",
            "anglicized_names": ["Ibraheem"],
            "english_names": ["Abraham"],
            "place": "Makkah",
            "title_refers": "v. 35-41",
            "juz": [13]
        },
        15: {
            "name": "Al-Hijr",
            "anglicized_names": ["Al-Hejr"],
            "english_names": ["The Rocky Tract", "The Stoneland", "The Rock City", "Hegra"],
            "place": "Makkah",
            "title_refers": "v. 80",
            "juz": [14]
        },
        16: {
            "name": "An-Nahl",
            "anglicized_names": ["An-Nahal"],
            "english_names": ["The Bees"],
            "place": "Makkah",
            "title_refers": "v. 68-69",
            "juz": [14]
        },
        17: {
            "name": "Al-Isra",
            "anglicized_names": ["Bani Israil"],
            "english_names": ["The Night Journey", "Children of Israel"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [15]
        },
        18: {
            "name": "Al-Kahf",
            "anglicized_names": ["Al-Kahaf"],
            "english_names": ["The Cave"],
            "place": "Makkah",
            "title_refers": "v. 13-20",
            "juz": [15, 16]
        },
        19: {
            "name": "Maryam",
            "anglicized_names": ["Mariam"],
            "english_names": ["Mary"],
            "place": "Makkah",
            "title_refers": "v. 16-37",
            "juz": [16]
        },
        20: {
            "name": "Ta-Ha",
            "anglicized_names": ["Al-Kalim"],
            "english_names": ["Ṭāʾ Hāʾ", "The Interlocutor"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [16]
        },
        21: {
            "name": "Al-Anbiya",
            "anglicized_names": ["Al-Ambiyaa"],
            "english_names": ["The Prophets"],
            "place": "Makkah",
            "title_refers": "v. 48-91",
            "juz": [17]
        },
        22: {
            "name": "Al-Hajj",
            "anglicized_names": ["Al-Haj"],
            "english_names": ["The Pilgrimage", "The Hajj"],
            "place": "Madinah",
            "title_refers": "v. 25-38",
            "juz": [17]
        },
        23: {
            "name": "Al-Mu'minun",
            "anglicized_names": ["Al-Muminoon"],
            "english_names": ["The Believers"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [18]
        },
        24: {
            "name": "An-Nur",
            "anglicized_names": ["An-Noor"],
            "english_names": ["The Light"],
            "place": "Madinah",
            "title_refers": "v. 35",
            "juz": [18]
        },
        25: {
            "name": "Al-Furqan",
            "anglicized_names": ["Al-Furqaan"],
            "english_names": ["The Criterion", "The Standard", "The Standard of True and False"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [18, 19]
        },
        26: {
            "name": "Ash-Shu'ara",
            "anglicized_names": ["Ash-Shuaraa"],
            "english_names": ["The Poets"],
            "place": "Makkah",
            "title_refers": "v. 224",
            "juz": [19]
        },
        27: {
            "name": "An-Naml",
            "anglicized_names": ["Sulayman"],
            "english_names": ["The Ants", "Solomon"],
            "place": "Makkah",
            "title_refers": "v. 18",
            "juz": [19, 20]
        },
        28: {
            "name": "Al-Qasas",
            "anglicized_names": ["Al-Qesas"],
            "english_names": ["The Narrations", "The Stories", "The Story"],
            "place": "Makkah",
            "title_refers": "v. 25",
            "juz": [20]
        },
        29: {
            "name": "Al-Ankabut",
            "anglicized_names": ["Al-Ankaboot"],
            "english_names": ["The Spider"],
            "place": "Makkah",
            "title_refers": "v. 41",
            "juz": [20, 21]
        },
        30: {
            "name": "Ar-Rum",
            "anglicized_names": ["Ar-Room"],
            "english_names": ["Rome", "Byzantium"],
            "place": "Makkah",
            "title_refers": "v. 2",
            "juz": [21]
        },
        31: {
            "name": "Luqman",
            "anglicized_names": ["Luqmaan"],
            "english_names": ["Luqman"],
            "place": "Makkah",
            "title_refers": "v. 12-19",
            "juz": [21]
        },
        32: {
            "name": "As-Sajdah",
            "anglicized_names": ["Al-Madaji'"],
            "english_names": ["The Prostration", "The Beds"],
            "place": "Makkah",
            "title_refers": "v. 15",
            "juz": [21]
        },
        33: {
            "name": "Al-Ahzab",
            "anglicized_names": ["Al-Ahzaab"],
            "english_names": ["The Clans", "The Confederates", "The Combined Forces"],
            "place": "Madinah",
            "title_refers": "v. 9-27",
            "juz": [21, 22]
        },
        34: {
            "name": "Saba",
            "anglicized_names": ["Sabaa"],
            "english_names": ["Sheba"],
            "place": "Makkah",
            "title_refers": "v. 15-20",
            "juz": [22]
        },
        35: {
            "name": "Fatir",
            "anglicized_names": ["Al-Mala'ika"],
            "english_names": ["The Originator", "The Angels"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [22]
        },
        36: {
            "name": "Ya-Sin",
            "anglicized_names": ["Yaseen"],
            "english_names": ["Yāʾ Sīn"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [22, 23]
        },
        37: {
            "name": "As-Saffat",
            "anglicized_names": ["As-Saaffaat"],
            "english_names": ["Those Who Set The Ranks", "Drawn Up In Ranks", "Those Ranged in Ranks"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [23]
        },
        38: {
            "name": "Sad",
            "anglicized_names": ["Dawud"],
            "english_names": ["Ṣād", "David"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [23]
        },
        39: {
            "name": "Az-Zumar",
            "anglicized_names": ["Al-Ghuraf"],
            "english_names": ["The Crowds", "The Troops", "Throngs", "The Chambers"],
            "place": "Makkah",
            "title_refers": "v. 71, 73",
            "juz": [23, 24]
        },
        40: {
            "name": "Ghafir",
            "anglicized_names": ["Al-Muʼmin"],
            "english_names": ["The Forgiver (God)", "Forgiving", "The Believer"],
            "place": "Makkah",
            "title_refers": "v. 3",
            "juz": [24]
        },
        41: {
            "name": "Fussilat",
            "anglicized_names": ["Al-Masabih"],
            "english_names": ["Expounded", "Explained In Detail", "Clearly Spelled Out", "The Lamps"],
            "place": "Makkah",
            "title_refers": "v. 3",
            "juz": [24, 25]
        },
        42: {
            "name": "Ash-Shura",
            "anglicized_names": ["Ha Mim 'Ayn Sin Qaf"],
            "english_names": ["The Consultation", "Ḥāʾ Mīm ʿAyn Sīn Qāf"],
            "place": "Makkah",
            "title_refers": "v. 36",
            "juz": [25]
        },
        43: {
            "name": "Az-Zukhruf",
            "anglicized_names": ["Az-Zukharaf"],
            "english_names": ["The Gold Adornments", "The Ornaments of Gold", "Luxury", "Gold"],
            "place": "Makkah",
            "title_refers": "v. 35",
            "juz": [25]
        },
        44: {
            "name": "Ad-Dukhan",
            "anglicized_names": ["Ad-Dukhaan"],
            "english_names": ["The Smoke"],
            "place": "Makkah",
            "title_refers": "v. 10",
            "juz": [25]
        },
        45: {
            "name": "Al-Jathiyah",
            "anglicized_names": ["Al-Shari'a"],
            "english_names": ["The Kneeling Down", "Crouching", "The Sharia"],
            "place": "Makkah",
            "title_refers": "v. 28",
            "juz": [25]
        },
        46: {
            "name": "Al-Ahqaf",
            "anglicized_names": ["Al-Ahqaaf"],
            "english_names": ["Winding Sand-tracts", "The Dunes", "The Sand-Dunes"],
            "place": "Makkah",
            "title_refers": "v. 21",
            "juz": [26]
        },
        47: {
            "name": "Muhammad",
            "anglicized_names": ["Al-Qital"],
            "english_names": ["Muhammad", "The Combat", "The Warfare"],
            "place": "Madinah",
            "title_refers": "v. 2",
            "juz": [26]
        },
        48: {
            "name": "Al-Fath",
            "anglicized_names": ["Al-Fatah"],
            "english_names": ["The Victory"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [26]
        },
        49: {
            "name": "Al-Hujurat",
            "anglicized_names": ["Al-Hujuraat"],
            "english_names": ["The Private Apartments", "The Inner Apartments"],
            "place": "Madinah",
            "title_refers": "v. 4",
            "juz": [26]
        },
        50: {
            "name": "Qaf",
            "anglicized_names": ["Al-Basiqat"],
            "english_names": ["Qāf", "The Tall Ones"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [26]
        },
        51: {
            "name": "Adh-Dhariyat",
            "anglicized_names": ["Adh-Dhaariyaat"],
            "english_names": ["The Wind That Scatter", "The Winnowing Winds", "The Dust-Scattering Winds"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [26, 27]
        },
        52: {
            "name": "At-Tur",
            "anglicized_names": ["At-Toor"],
            "english_names": ["The Mount", "Mount Sinai"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [27]
        },
        53: {
            "name": "An-Najm",
            "anglicized_names": ["An-Najam"],
            "english_names": ["The Star", "The Unfolding"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [27]
        },
        54: {
            "name": "Al-Qamar",
            "anglicized_names": ["Iqtarabat"],
            "english_names": ["The Moon", "Approached"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [27]
        },
        55: {
            "name": "Ar-Rahman",
            "anglicized_names": ["Ar-Rahmaan"],
            "english_names": ["The Most Merciful", "The Most Gracious"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [27]
        },
        56: {
            "name": "Al-Waqi'ah",
            "anglicized_names": ["Al-Waaqiah"],
            "english_names": ["The Inevitable", "The Event", "That Which Must Come to Pass"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [27]
        },
        57: {
            "name": "Al-Hadid",
            "anglicized_names": ["Al-Hadeed"],
            "english_names": ["Iron"],
            "place": "Madinah",
            "title_refers": "v. 25",
            "juz": [27]
        },
        58: {
            "name": "Al-Mujadila",
            "anglicized_names": ["Al-Zihar"],
            "english_names": ["The Pleading Woman", "The Backs", "The Zihar"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [28]
        },
        59: {
            "name": "Al-Hashr",
            "anglicized_names": ["Al-Hashar"],
            "english_names": ["The Mustering", "The Gathering", "Exile", "Banishment"],
            "place": "Madinah",
            "title_refers": "v. 2",
            "juz": [28]
        },
        60: {
            "name": "Al-Mumtahanah",
            "anglicized_names": ["Al-Mumtahinah"],
            "english_names": ["The Examined One", "She That Is To Be Examined"],
            "place": "Madinah",
            "title_refers": "v. 10",
            "juz": [28]
        },
        61: {
            "name": "As-Saff",
            "anglicized_names": ["Al-Hawariyyin"],
            "english_names": ["The Ranks", "Battle Array", "The Apostles"],
            "place": "Madinah",
            "title_refers": "v. 4",
            "juz": [28]
        },
        62: {
            "name": "Al-Jumu'ah",
            "anglicized_names": ["Al-Jumuah"],
            "english_names": ["Congregation", "Friday", "Friday prayer"],
            "place": "Madinah",
            "title_refers": "v. 9-10",
            "juz": [28]
        },
        63: {
            "name": "Al-Munafiqun",
            "anglicized_names": ["Al-Munaafiqoon"],
            "english_names": ["The Hypocrites"],
            "place": "Madinah",
            "title_refers": "Whole Surah",
            "juz": [28]
        },
        64: {
            "name": "At-Taghabun",
            "anglicized_names": ["At-Taghaabun"],
            "english_names": ["The Cheating", "The Mutual Disillusion", "The Mutual Loss and Gain", "Loss and Gain"],
            "place": "Madinah",
            "title_refers": "v. 9",
            "juz": [28]
        },
        65: {
            "name": "At-Talaq",
            "anglicized_names": ["At-Talaaq"],
            "english_names": ["Divorce"],
            "place": "Madinah",
            "title_refers": "Whole Surah",
            "juz": [28]
        },
        66: {
            "name": "At-Tahrim",
            "anglicized_names": ["Lima Tuharrim"],
            "english_names": ["The Prohibition", "Why do you prohibit?"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [28]
        },
        67: {
            "name": "Al-Mulk",
            "anglicized_names": ["Tabarak"],
            "english_names": ["The Dominion", "The Sovereignty", "The Kingship", "Blessed"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        68: {
            "name": "Al-Qalam",
            "anglicized_names": ["Nun"],
            "english_names": ["The Pen", "Nūn"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        69: {
            "name": "Al-Haqqah",
            "anglicized_names": ["Al-Haaqqah"],
            "english_names": ["The Sure Reality", "The Laying-Bare of the Truth"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        70: {
            "name": "Al-Ma'arij",
            "anglicized_names": ["Sa'ala Sa'il"],
            "english_names": ["The Ways of Ascent", "The Ascending Stairways", "An asker asked"],
            "place": "Makkah",
            "title_refers": "v. 3",
            "juz": [29]
        },
        71: {
            "name": "Nuh",
            "anglicized_names": ["Nooh"],
            "english_names": ["Noah"],
            "place": "Makkah",
            "title_refers": "Whole Surah",
            "juz": [29]
        },
        72: {
            "name": "Al-Jinn",
            "anglicized_names": ["Al-Wahy"],
            "english_names": ["The Jinn", "The Spirits", "The Unseen Beings", "The Revelation"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        73: {
            "name": "Al-Muzzammil",
            "anglicized_names": ["Al-Muzammil"],
            "english_names": ["The Enfolded One", "The Enshrouded One", "Bundled Up", "The Enwrapped One"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        74: {
            "name": "Al-Muddaththir",
            "anglicized_names": ["Al-Muddathir"],
            "english_names": ["The One Wrapped Up", "The Cloaked One", "The Man Wearing A Cloak", "The Enfolded One"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        75: {
            "name": "Al-Qiyamah",
            "anglicized_names": ["Al-Qiyaamah"],
            "english_names": ["Resurrection", "The Day of Resurrection", "Rising Of The Dead"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        76: {
            "name": "Al-Insan",
            "anglicized_names": ["Ad-Dahr"],
            "english_names": ["The Human", "Man"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        77: {
            "name": "Al-Mursalat",
            "anglicized_names": ["Al-Mursalaat"],
            "english_names": ["Those Sent Forth", "The Emissaries", "Winds Sent Forth"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [29]
        },
        78: {
            "name": "An-Naba",
            "anglicized_names": ["'Amma"],
            "english_names": ["The Great News", "The Announcement", "The Tiding", "About what?"],
            "place": "Makkah",
            "title_refers": "v. 2",
            "juz": [30]
        },
        79: {
            "name": "An-Nazi'at",
            "anglicized_names": ["As-Sahira"],
            "english_names": ["Those Who Tear Out", "Those Who Drag Forth", "Soul-snatchers", "Those That Rise", "The Watchful", "The Sleepless", "The Alert"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        80: {
            "name": "Abasa",
            "anglicized_names": ["As-Safara"],
            "english_names": ["He Frowned", "The Messenger-Angels", "The Journeyers"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        81: {
            "name": "At-Takwir",
            "anglicized_names": ["At-Takweer"],
            "english_names": ["The Folding Up", "The Overthrowing", "Shrouding in Darkness"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        82: {
            "name": "Al-Infitar",
            "anglicized_names": ["Al-Infitaar"],
            "english_names": ["The Cleaving Asunder", "Bursting Apart"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        83: {
            "name": "Al-Mutaffifin",
            "anglicized_names": ["Al-Mutaffifeen"],
            "english_names": ["The Dealers in Fraud", "Defrauding", "The Cheats", "Those Who Give Short Measure"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        84: {
            "name": "Al-Inshiqaq",
            "anglicized_names": ["Al-Inshiqaaq"],
            "english_names": ["The Rending Asunder", "The Sundering", "Splitting Open", "The Splitting Asunder"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        85: {
            "name": "Al-Buruj",
            "anglicized_names": ["Al-Burooj"],
            "english_names": ["The Mansions Of The Stars", "The Constellations", "The Great Constellations"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        86: {
            "name": "At-Tariq",
            "anglicized_names": ["At-Taareq"],
            "english_names": ["The Night-Visitant", "The Morning Star", "The Nightcomer", "That Which Comes in the Night"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        87: {
            "name": "Al-A'la",
            "anglicized_names": ["Al-Alaa"],
            "english_names": ["The Most High", "The All-Highest", "Glory To Your Lord In The Highest"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        88: {
            "name": "Al-Ghashiyah",
            "anglicized_names": ["Al-Ghaashiyah"],
            "english_names": ["The Overwhelming Event", "The Overshadowing Event", "The Pall"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        89: {
            "name": "Al-Fajr",
            "anglicized_names": ["Al-Fajar"],
            "english_names": ["The Break of Day", "The Daybreak", "The Dawn"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        90: {
            "name": "Al-Balad",
            "anglicized_names": ["Al-Balid"],
            "english_names": ["The city", "The Land"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        91: {
            "name": "Ash-Shams",
            "anglicized_names": ["Ash-Shamas"],
            "english_names": ["The Sun"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        92: {
            "name": "Al-Layl",
            "anglicized_names": ["Al-Lail"],
            "english_names": ["The Night"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        93: {
            "name": "Ad-Dhuha",
            "anglicized_names": ["Ad-Duha"],
            "english_names": ["The Glorious Morning Light", "The Forenoon", "Morning Hours", "Morning Bright", "The Bright Morning Hours"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        94: {
            "name": "Ash-Sharh",
            "anglicized_names": ["Ash-Sharah"],
            "english_names": ["The Expansion of Breast", "Solace", "Consolation", "Relief", "Patient", "The Opening-Up of the Heart"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        95: {
            "name": "At-Tin",
            "anglicized_names": ["At-Teen"],
            "english_names": ["The Fig Tree", "The Fig"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        96: {
            "name": "Al-'Alaq",
            "anglicized_names": ["Al-Alaq"],
            "english_names": ["The Clinging Clot", "Clot of Blood", "The Germ-Cell"],
            "place": "Makkah",
            "title_refers": "v. 2",
            "juz": [30]
        },
        97: {
            "name": "Al-Qadr",
            "anglicized_names": ["Al-Qader"],
            "english_names": ["The Night of Honor", "The Night of Decree", "Power", "Fate", "Destiny"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        98: {
            "name": "Al-Bayyinah",
            "anglicized_names": ["Ahl al-Kitab"],
            "english_names": ["The Clear Evidence", "The Evidence of the Truth", "The People of the Book"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        99: {
            "name": "Az-Zalzalah",
            "anglicized_names": ["Az-Zalzala"],
            "english_names": ["The Earthquake"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        100: {
            "name": "Al-'Adiyat",
            "anglicized_names": ["Al-Aadiyaat"],
            "english_names": ["The Courser", "The Chargers", "The War Horse"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        101: {
            "name": "Al-Qari'ah",
            "anglicized_names": ["Al-Qaariah"],
            "english_names": ["The Striking Hour", "The Great Calamity", "The Stunning Blow", "The Sudden Calamity"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        102: {
            "name": "At-Takathur",
            "anglicized_names": ["At-Takaathur"],
            "english_names": ["The Piling Up", "Rivalry in World Increase", "Competition", "Greed for More and More"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        103: {
            "name": "Al-'Asr",
            "anglicized_names": ["Al-Asar"],
            "english_names": ["The Time", "The Declining Day", "The Epoch", "The Flight of Time", "Success Criteria"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        104: {
            "name": "Al-Humazah",
            "anglicized_names": ["Al-Humaza"],
            "english_names": ["The Scandalmonger", "The Traducer", "The Gossipmonger", "The Slanderer"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        105: {
            "name": "Al-Fil",
            "anglicized_names": ["Al-Feel"],
            "english_names": ["The Elephant"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        106: {
            "name": "Quraysh",
            "anglicized_names": ["Quraish"],
            "english_names": ["The Quraysh"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        107: {
            "name": "Al-Ma'un",
            "anglicized_names": ["Ad-Din"],
            "english_names": ["The Neighbourly Assistance", "Small Kindnesses", "Almsgiving", "Assistance", "The Recompense"],
            "place": "Makkah",
            "title_refers": "v. 7",
            "juz": [30]
        },
        108: {
            "name": "Al-Kawthar",
            "anglicized_names": ["Al-Kauthar"],
            "english_names": ["Abundance", "Plenty", "Good in Abundance"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        109: {
            "name": "Al-Kafirun",
            "anglicized_names": ["Al-'Ibada"],
            "english_names": ["The Disbelievers", "The Kafirs", "The Worship", "The Adoration"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        110: {
            "name": "An-Nasr",
            "anglicized_names": ["At-Tawdi'"],
            "english_names": ["The Help", "The Divine Support", "The Farewell"],
            "place": "Madinah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        111: {
            "name": "Al-Masad",
            "anglicized_names": ["Tabbat"],
            "english_names": ["The Plaited Rope", "The Palm Fibre", "The Twisted Strands", "Ruined"],
            "place": "Makkah",
            "title_refers": "v. 5",
            "juz": [30]
        },
        112: {
            "name": "Al-Ikhlas",
            "anglicized_names": ["At-Tawhid"],
            "english_names": ["The Purity of Faith", "The Fidelity", "The Oneness and Unification of God"],
            "place": "Makkah",
            "title_refers": "Whole Surah",
            "juz": [30]
        },
        113: {
            "name": "Al-Falaq",
            "anglicized_names": ["Al-Falak"],
            "english_names": ["The Daybreak", "Dawn", "The Rising Dawn"],
            "place": "Makkah",
            "title_refers": "v. 1",
            "juz": [30]
        },
        114: {
            "name": "An-Nas",
            "anglicized_names": ["An-Naas"],
            "english_names": ["Mankind", "Men", "Mass"],
            "place": "Makkah",
            "title_refers": "Whole Surah",
            "juz": [30]
        }
    }

    # Default output directory - can be modified as needed
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'surah')
    
    print(f"Converting Surah data to markdown files...")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print("-" * 50)
    
    try:
        create_surah_files(surah_data, output_dir)
    except (OSError, Exception) as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()

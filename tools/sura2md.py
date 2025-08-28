#!/usr/bin/env python3
"""
Convert Surah data into Hugo markdown files.

This script processes Surah data in the format:
{sura_number} - {surah_name} ({translation})

And converts each line into a markdown file at:
{output_dir}/{sura_number}/_index.md

With frontmatter containing weight, title, and translation.
"""

import os
import re
from typing import List, Tuple, Optional


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


def create_markdown_content(sura_number: int, surah_name: str, translation: str) -> str:
    """
    Generate markdown content with TOML frontmatter.
    
    Args:
        sura_number: The Surah number
        surah_name: The Arabic/transliterated name
        translation: The English translation
        
    Returns:
        Complete markdown content string
    """
    return f"""+++
weight = {sura_number}
title = "{surah_name}"
en = "{translation}"
+++
"""


def create_surah_files(data: str, output_dir: str) -> None:
    """
    Process Surah data and create markdown files.
    
    Args:
        data: Multi-line string containing Surah data
        output_dir: Base directory where files will be created
        
    Raises:
        OSError: If directory creation or file writing fails
    """
    lines = data.strip().split('\n')
    processed_count = 0
    skipped_count = 0
    
    for line_num, line in enumerate(lines, 1):
        parsed = parse_surah_line(line)
        
        if parsed is None:
            print(f"Warning: Skipping invalid line {line_num}: {line}")
            skipped_count += 1
            continue
        
        sura_number, surah_name, translation = parsed
        
        # Create directory structure
        surah_dir = os.path.join(output_dir, str(sura_number))
        os.makedirs(surah_dir, exist_ok=True)
        
        # Generate markdown content
        content = create_markdown_content(sura_number, surah_name, translation)
        
        # Write to file
        file_path = os.path.join(surah_dir, '_index.md')
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {file_path}")
            processed_count += 1
        except OSError as e:
            print(f"Error writing file {file_path}: {e}")
            raise
    
    print(f"\nProcessing complete!")
    print(f"Files created: {processed_count}")
    print(f"Lines skipped: {skipped_count}")


def main() -> None:
    """
    Main function to process the Surah data.
    """
    # The Surah data as provided
    surah_data = """1 - Al-Fatiha (The Opener)
2 - Al-Baqarah (The Cow)
3 - Al-Imran (Family of Imran)
4 - An-Nisa (The Women)
5 - Al-Ma'idah (The Table Spread)
6 - Al-Anam (The Cattle)
7 - Al-A'raf (The Heights)
8 - Al-Anfal (The Spoils of War)
9 - At-Taubah (The Repentance)
10 - Yunus (Jonah)
11 - Hud (Hud)
12 - Yusuf (Joseph)
13 - Ar-Ra'd (Thunder)
14 - Ibrahim (Abraham)
15 - Al-Hijr (The Stoneland)
16 - An-Nahl (The Bee)
17 - Al-Isra (The Night Journey)
18 - Al-Kahf (The Cave)
19 - Maryam (Mary)
20 - Ta-Ha (Ta-Ha)
21 - Al-Anbiya (The Prophets)
22 - Al-Hajj (The Pilgrimage)
23 - Al-Mu'minun (The Believers)
24 - An-Nur (The Light)
25 - Al-Furqan (The Criterion)
26 - Ash-Shu'ara (The Poets)
27 - An-Naml (The Ants)
28 - Al-Qasas (The Story)
29 - Al-Ankabut (Spider)
30 - Ar-Rum (The Romans)
31 - Luqman (Luqman)
32 - As-Sajdah (Prostration)
33 - Al-Ahzab (The Confederates)
34 - Saba (Sheba)
35 - Fatir (The Originator)
36 - Ya-Sin (Ya Sin)
37 - As-Saffat (Those Who Set the Ranks)
38 - Sad (The letter Saad)
39 - Az-Zumar (The Troops)
40 - Ghafir (The Forgiver)
41 - Fussilat (Explained in Detail)
42 - Ash-Shura (The Consultation)
43 - Az-Zukhruf (The Ornaments of Gold)
44 - Ad-Dukhan (The Smoke)
45 - Al-Jathiyah (The Crouching)
46 - Al-Ahqaf (The Wind Curved Sandhill)
47 - Muhammad (Muhammad)
48 - Al-Fath (The Victory)
49 - Al-Hujurat (The Private Chambers)
50 - Qaf (Qaf)
51 - Adh-Dhariyat (The Scatterers)
52 - At-Tur (The Mountain)
53 - An-Najm (The Star)
54 - Al-Qamar (The Moon)
55 - Ar-Rahman (The Beneficent)
56 - Al-Waqi'ah (The Inevitable)
57 - Al-Hadid (The Iron)
58 - Al-Mujadila (The Pleading Women)
59 - Al-Hashr (The Exile)
60 - Al-Mumtahanah (She That is to be Examined)
61 - As-Saff (The Ranks)
62 - Al-Jumu'ah (Congregation Prayer)
63 - Al-Munafiqun (The Hypocrites)
64 - At-Taghabun (Mutual Disposession)
65 - At-Talaq (The Divorce)
66 - At-Tahrim (The Prohibition)
67 - Al-Mulk (The Sovereignty)
68 - Al-Qalam (The Pen)
69 - Al-Haqqah (The Reality)
70 - Al-Ma'arij (The Ascending Stairways)
71 - Nuh (Noah)
72 - Al-Jinn (The Jinn)
73 - Al-Muzzammil (The Enshrouded One)
74 - Al-Muddaththir (The Cloaked One)
75 - Al-Qiyamah (The Resurrection)
76 - Al-Insan (The Man)
77 - Al-Mursalat (The Emissaries)
78 - An-Naba (The Tidings)
79 - An-Nazi'at (Those who drag forth)
80 - Abasa (He Frowned)
81 - At-Takwir (The Overthrowing)
82 - Al-Infitar (The Cleaving)
83 - Al-Mutaffifin (The Defrauding)
84 - Al-Inshiqaq (The Sundering)
85 - Al-Buruj (The Mansions of the Stars)
86 - At-Tariq (The Nightcommer)
87 - Al-Ala (The Most High)
88 - Al-Ghashiyah (The Overwhelming)
89 - Al-Fajr (The Dawn)
90 - Al-Balad (The City)
91 - Ash-Shams (The Sun)
92 - Al-Lail (The Night)
93 - Ad-Duha (The Morning Brightness)
94 - Ash-Sharh (The Expansion)
95 - At-Tin (The Fig)
96 - Al-Alaq (The Blood Clot)
97 - Al-Qadr (The Power)
98 - Al-Bayyina (The Evidence)
99 - Az-Zalzalah (The Earthquake)
100 - Al-Adiyat (The Courser)
101 - Al-Qari'ah (The Calamity)
102 - At-Takathur (Vying for increase)
103 - Al-Asr (The Declining Day)
104 - Al-Humazah (The Slanderer)
105 - Al-Fil (The Elephant)
106 - Quraysh (Quraish)
107 - Al-Ma'un (The Small Kindness)
108 - Al-Kawthar (The Abundance)
109 - Al-Kafirun (The Disbelievers)
110 - An-Nasr (The Divine Support)
111 - Al-Masad (The Palm Fiber)
112 - Al-Ikhlas (The Sincerity)
113 - Al-Falaq (The Daybreak)
114 - An-Nas (The Mankind)"""

    # Default output directory - can be modified as needed
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'surah')
    
    print(f"Converting Surah data to markdown files...")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print("-" * 50)
    
    try:
        create_surah_files(surah_data, output_dir)
    except OSError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return


if __name__ == "__main__":
    main()

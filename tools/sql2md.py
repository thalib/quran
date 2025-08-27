
#!/usr/bin/env python3
"""
SQL to Markdown Converter for Quran Verses

This script reads verses from a SQLite database and exports each verse
to a separate markdown file with Hugo front matter.

Database schema expected:
- Table: verses
- Columns: sura (int), ayah (int), text (str)

Output format: out/{sura}/{ayah}.md
"""

import sqlite3
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Set


def extract_tags_from_text(text: str) -> List[str]:
    """
    Extract meaningful tags from verse text.
    
    Args:
        text: The verse text to analyze
        
    Returns:
        List of tags extracted from the text
    """
    # Common meaningful words/concepts in Quran verses
    common_concepts = {
        'allah', 'god', 'lord', 'prayer', 'believe', 'believers', 'faith',
        'paradise', 'garden', 'heaven', 'fire', 'hell', 'punishment',
        'mercy', 'forgiveness', 'guidance', 'revelation', 'prophet',
        'messenger', 'book', 'quran', 'scripture', 'signs', 'verses',
        'righteous', 'good', 'evil', 'sin', 'worship', 'prostrate',
        'angels', 'devil', 'satan', 'creation', 'earth', 'sky', 'heavens',
        'day', 'judgment', 'resurrection', 'death', 'life', 'world',
        'knowledge', 'wisdom', 'truth', 'falsehood', 'guidance', 'astray',
        'charity', 'poor', 'orphan', 'needy', 'wealth', 'provision',
        'family', 'parents', 'children', 'marriage', 'divorce',
        'people', 'nation', 'community', 'humanity', 'mankind',
        'covenant', 'promise', 'oath', 'testimony', 'witness',
        'repentance', 'forgive', 'sin', 'transgression', 'wrong'
    }
    
    # Convert text to lowercase and extract words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Find meaningful concepts
    tags = set()
    for word in words:
        if word in common_concepts:
            tags.add(word)
        # Add plural forms
        elif word.endswith('s') and word[:-1] in common_concepts:
            tags.add(word[:-1])
    
    # Additional pattern-based tags
    if re.search(r'\b(pray|prayer|salah)\b', text, re.IGNORECASE):
        tags.add('prayer')
    if re.search(r'\b(paradise|garden|jannah)\b', text, re.IGNORECASE):
        tags.add('paradise')
    if re.search(r'\b(hell|fire|jahannam)\b', text, re.IGNORECASE):
        tags.add('hell')
    if re.search(r'\b(believe|faith|iman)\b', text, re.IGNORECASE):
        tags.add('faith')
    
    return sorted(list(tags))


def create_markdown_content(sura: int, ayah: int, text: str, date_str: str, row_count: int) -> str:
    """
    Create markdown content with Hugo front matter.
    
    Args:
        sura: Surah number
        ayah: Ayah number
        text: Verse text
        date_str: Date string in YYYY-MM-DD format
        row_count: Current row number (1-based index)
        
    Returns:
        Complete markdown content with front matter
    """
    tags = extract_tags_from_text(text)
    tags_str = ', '.join(f'"{tag}"' for tag in tags)
    
    front_matter = f"""+++
title = 'Surah {sura}, Verses {ayah}'
date = '{date_str}'
weight = {row_count}
ayah = {ayah}
tags = [{tags_str}]
+++

{text}"""
    
    return front_matter


def export_verses_to_markdown(db_path: str, output_dir: str = "out") -> None:
    """
    Export all verses from SQLite database to individual markdown files.
    
    Args:
        db_path: Path to the SQLite database file
        output_dir: Output directory for markdown files (default: "out")
    """
    # Check if database file exists
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")
    
    # Get current date in required format
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query all verses
        cursor.execute("SELECT sura, ayah, text FROM verses ORDER BY sura, ayah")
        verses = cursor.fetchall()
        
        if not verses:
            print("No verses found in the database.")
            return
        
        print(f"Found {len(verses)} verses to export...")
        
        exported_count = 0
        for row_index, (sura, ayah, text) in enumerate(verses, 1):
            try:
                # Create surah directory
                surah_dir = output_path / str(sura)
                surah_dir.mkdir(exist_ok=True)
                
                # Create markdown file path
                md_file = surah_dir / f"{ayah}.md"
                
                # Generate markdown content
                markdown_content = create_markdown_content(sura, ayah, text, today, row_index)
                
                # Write to file
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                exported_count += 1
                
                # Progress indicator
                if exported_count % 100 == 0:
                    print(f"Exported {exported_count} verses...")
                    
            except Exception as e:
                print(f"Error processing verse {sura}:{ayah} - {e}")
                continue
        
        print(f"Successfully exported {exported_count} verses to {output_dir}/")
        
    except sqlite3.Error as e:
        raise RuntimeError(f"Database error: {e}")
    
    finally:
        if conn:
            conn.close()


def main():
    """Main function to handle command line execution."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python sql2md.py <database_path> [output_directory]")
        print("Example: python sql2md.py quran.en.clearquran.db out")
        sys.exit(1)
    
    db_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "out"
    
    try:
        export_verses_to_markdown(db_path, output_dir)
        print("Export completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
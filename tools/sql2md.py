
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
    Extract meaningful tags from verse text by including all words except common function words,
    plus custom semantic mappings.
    
    Args:
        text: The verse text to analyze
        
    Returns:
        List of tags extracted from the text
    """
    # Function words and common verbs to exclude from tags
    excluded_words = [
        # Personal Pronouns
        "he", "she", "it", "him", "her", "his", "hers", "its",
        "they", "them", "their", "theirs", "i", "me", "my", "mine",
        "you", "your", "yours", "we", "us", "our", "ours",
        
        # Demonstrative Pronouns
        "this", "that", "these", "those", "here", "there", "now", "then",
        
        # Question Words (Interrogatives)
        "who", "whom", "whose", "what", "which", "when", "where", "why", "how",
        "whether", "if",
        
        # Coordinating Conjunctions
        "and", "but", "or", "for", "nor", "so", "yet",
        
        # Subordinating Conjunctions
        "because", "since", "as", "although", "though", "while", "before", "after",
        "unless", "until", "wherever", "whenever",
        
        # Prepositions
        "in", "on", "at", "by", "with", "to", "from", "of", "up", "down", "over", "under",
        "through", "across", "between", "during", "within", "without",
        
        # Articles & Determiners
        "the", "a", "an", "some", "any", "many", "each", "every", "all",
        "few", "several", "most",
        
        # Adverbs of Time
        "soon", "today", "tomorrow", "yesterday", "already", "still", "always", "never",
        "sometimes", "often", "rarely", "usually",
        
        # Adverbs of Place
        "everywhere", "above", "below", "inside", "outside", "nearby", "far",
        "left", "right", "forward", "back",
        
        # Adverbs of Manner
        "well", "badly", "quickly", "slowly", "carefully", "easily",
        "hard", "fast", "loud", "quiet",
        
        # Modal Verbs
        "can", "could", "may", "might", "will", "would", "shall", "should", "must",
        
        # Common Linking Words
        "also", "too", "either", "however", "therefore", "thus", "moreover", "furthermore",
        "nevertheless", "nonetheless", "indeed", "certainly", "perhaps",
        
        # Auxiliary and Common Verbs
        "be", "is", "are", "was", "were", "been", "being", "have", "has", "had",
        "do", "does", "did", "ought", "need", "dare", "used"
    ]
    
    # Convert excluded words to set for faster lookup (case-insensitive)
    excluded_words_set = {word.lower() for word in excluded_words}
    
    # Custom word mappings for semantic grouping (case-insensitive)
    custom_mappings = {
        "prophet": ["musa", "moses", "abraham", "ibrahim", "jesus", "isa", "muhammad", "noah", "nuh", 
                   "joseph", "yusuf", "david", "dawud", "solomon", "sulaiman", "adam", "lot", "lut"],
        "angel": ["gabriel", "jibril", "michael", "mikail", "israfil", "azrael"],
        "book": ["torah", "injil", "gospel", "zabur", "psalms", "quran", "koran"],
        "place": ["mecca", "makkah", "medina", "madinah", "jerusalem", "baitul", "kaaba", "kabah"],
        "prayer": ["salah", "namaz", "dua", "dhikr", "worship"],
        "paradise": ["jannah", "garden", "gardens"],
        "hell": ["jahannam", "fire", "hellfire"],
        "faith": ["iman", "belief", "believe"]
    }
    
    # Convert text to lowercase and extract words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # Filter out excluded function words and collect meaningful content words
    tags = set()
    for word in words:
        # Skip excluded function words
        if word in excluded_words_set:
            continue
            
        # Add the original word (content word)
        if len(word) > 2:  # Skip very short words
            tags.add(word)
            
        # Handle plural forms - add singular if it's not an excluded word
        if word.endswith('s') and len(word) > 3:
            singular = word[:-1]
            if singular not in excluded_words_set:
                tags.add(singular)
    
    # Add custom semantic tags based on word mappings
    text_lower = text.lower()
    for custom_tag, trigger_words in custom_mappings.items():
        for trigger_word in trigger_words:
            # Use word boundaries to match complete words only
            if re.search(rf'\b{re.escape(trigger_word)}\b', text_lower):
                tags.add(custom_tag)
                break  # Only add the custom tag once per category
    
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
surah = {sura}
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
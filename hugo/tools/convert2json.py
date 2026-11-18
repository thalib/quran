import sys
import os
import json

def convert_text_to_json(input_filepath, output_dir="out"):
    """
    Converts a text file with format {chapter}|{verse}|{text}
    into multiple JSON files ({chapter}.json) in the output directory.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    chapters_data = {}

    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            for line_num, line in enumerate(infile, 1):
                line = line.strip()
                if not line:
                    continue # Skip empty lines

                parts = line.split('|', 2)
                if len(parts) != 3:
                    print(f"Warning: Skipping malformed line {line_num}: {line}", file=sys.stderr)
                    continue

                try:
                    chapter_no = int(parts[0])
                    verse_no = int(parts[1])
                    text = parts[2].replace('"', '') # Remove double quotes
                except ValueError:
                    print(f"Warning: Skipping line {line_num} due to non-integer chapter/verse: {line}", file=sys.stderr)
                    continue
                except IndexError:
                     print(f"Warning: Skipping malformed line {line_num} (IndexError): {line}", file=sys.stderr)
                     continue


                if chapter_no not in chapters_data:
                    chapters_data[chapter_no] = {}

                if verse_no in chapters_data[chapter_no]:
                     print(f"Warning: Duplicate verse {chapter_no}:{verse_no} found. Overwriting.", file=sys.stderr)

                chapters_data[chapter_no][verse_no] = text

    except FileNotFoundError:
        print(f"Error: Input file not found: {input_filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}", file=sys.stderr)
        sys.exit(1)

    # Write data to JSON files
    for chapter_no, verses in chapters_data.items():
        output_filename = os.path.join(output_dir, f"{chapter_no}.json")
        try:
            with open(output_filename, 'w', encoding='utf-8') as outfile:
                json.dump(verses, outfile, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error writing file {output_filename}: {e}", file=sys.stderr)
        except Exception as e:
             print(f"An unexpected error occurred while writing {output_filename}: {e}", file=sys.stderr)


    print(f"Conversion complete. JSON files saved in '{output_dir}' directory.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert2json.py <input_text_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_text_to_json(input_file)

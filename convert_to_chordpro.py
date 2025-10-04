import os
import re

def convert_to_chordpro(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Extract title and hymn number
            first_line = lines[0].strip()
            match = re.match(r'(\d+)\s*–\s*(.*)', first_line)
            if not match:
                continue

            hymn_number = int(match.group(1))
            title = match.group(2).strip()

            # Pad the hymn number
            padded_hymn_number = str(hymn_number).zfill(3)

            # Create the new filename
            new_filename = f"{padded_hymn_number} - {title}.cho"
            new_filepath = os.path.join(output_dir, new_filename)

            # Build the ChordPro content
            chordpro_content = []
            chordpro_content.append(f"{{title: {title} - {hymn_number}}}")
            chordpro_content.append("")

            in_verse = False
            for line in lines[1:]:
                line = line.strip()
                if re.match(r'^\d+', line): # Verse number
                    if in_verse:
                        chordpro_content.append("{end_of_verse}")
                        chordpro_content.append("")
                    chordpro_content.append("{start_of_verse}")
                    in_verse = True
                elif line:
                    chordpro_content.append(line)

            if in_verse:
                chordpro_content.append("{end_of_verse}")

            # Write the new file
            with open(new_filepath, 'w') as f:
                f.write("\n".join(chordpro_content))

if __name__ == "__main__":
    convert_to_chordpro("raw_text", "chordpro")
    print("Conversion to ChordPro format complete.")
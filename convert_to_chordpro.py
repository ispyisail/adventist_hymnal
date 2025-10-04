import os
import glob
import re
import zipfile

def convert_to_chordpro_zip():
    input_dir = './raw_text/'
    output_zip_path = './Chordpro.zip'

    print("Script starting.")
    print(f"Input directory: {input_dir}")
    print(f"Output zip file: {output_zip_path}")

    # Get a sorted list of text files
    files = sorted(glob.glob(os.path.join(input_dir, '*.txt')))

    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files:
                base_name = os.path.basename(file_path)
                file_name_no_ext = os.path.splitext(base_name)[0]
                output_filename = f"{file_name_no_ext}.cho"

                print(f"Processing {file_path} -> {output_filename} in zip")

                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        lines = infile.readlines()

                        # Title
                        if not lines:
                            print(f"Skipping empty file: {file_path}")
                            continue

                        title_line = lines[0].strip()
                        title_parts = title_line.split(' – ')
                        if len(title_parts) < 2:
                            print(f"Skipping file with invalid title format: {file_path}")
                            continue

                        title = title_parts[1].strip()

                        # Build content in memory
                        output_content = []
                        output_content.append(f"{{title: {title}}}")
                        output_content.append("")

                        # Verses
                        in_verse = False
                        for line in lines[2:]:
                            stripped_line = line.strip()
                            if re.match(r'^\d+$', stripped_line):
                                if in_verse:
                                    output_content.append("")
                                output_content.append(f"{{comment: Verse {stripped_line}}}")
                                in_verse = True
                            elif stripped_line:
                                output_content.append(stripped_line)

                        # Write content to zip
                        zf.writestr(output_filename, '\n'.join(output_content))

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
                else:
                    print(f"Finished processing {file_path}")

    except Exception as e:
        print(f"Failed to create zip file: {e}")
    else:
        print(f"Successfully created {output_zip_path}")

    print("Script finished.")

if __name__ == "__main__":
    convert_to_chordpro_zip()
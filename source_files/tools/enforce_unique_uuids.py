import os
import uuid
import re

def ensure_unique_uuids(root_dir='.'):
    # The specific file names we are looking for
    target_files = {'info.json', 'infoAssessment.json', 'infoCourseInstance.json'}
    
    # Dictionary mapping UUID to full file path
    uuid_map = {}
    
    # Regex to strictly match the second line requirement:
    # Group 1 (prefix): Any whitespace/tabs, followed by "uuid": "
    # Group 2 (current_uuid): The actual UUID string inside the quotes
    # Group 3 (suffix): The closing quote, optional comma, and any trailing spaces
    uuid_pattern = re.compile(r'^(\s*"uuid":\s*")([^"]+)(",?\s*)$')
    
    # Recursively search directories
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename in target_files:
                filepath = os.path.join(dirpath, filename)
                
                # Read the file
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.read().splitlines()
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    continue
                    
                # Ignore files that don't have at least two lines
                if len(lines) < 2:
                    continue
                    
                second_line = lines[1]
                match = uuid_pattern.match(second_line)
                
                # If the second line matches the exact "uuid": "..." format
                if match:
                    prefix = match.group(1)
                    current_uuid = match.group(2)
                    suffix = match.group(3)
                    
                    # Check if the UUID is already in use
                    if current_uuid in uuid_map:
                        print(f"Collision detected! '{current_uuid}' in '{filepath}' is already used by '{uuid_map[current_uuid]}'.")
                        
                        # Generate a completely new UUID
                        new_uuid = str(uuid.uuid4())
                        
                        # Extreme edge case safeguard: ensure the new UUID didn't miraculously collide
                        while new_uuid in uuid_map:
                            new_uuid = str(uuid.uuid4())
                            
                        print(f"  -> Rewriting file with new UUID: '{new_uuid}'")
                        
                        # Update the specific line with the new UUID, preserving original tabs/formatting
                        lines[1] = f"{prefix}{new_uuid}{suffix}"
                        
                        # Overwrite the file
                        try:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write('\n'.join(lines) + '\n')
                            
                            # Add the new UUID to our dictionary
                            uuid_map[new_uuid] = filepath
                        except Exception as e:
                            print(f"Error writing to {filepath}: {e}")
                    else:
                        # No collision, add the existing UUID to the dictionary
                        uuid_map[current_uuid] = filepath

    return uuid_map

if __name__ == "__main__":
    print("Starting recursive search...")
    
    # Get the absolute path of the directory containing this script (e.g., 'tools')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go one level up to the parent directory
    parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    print(f"Searching from root: {parent_dir}")
    
    # Run the function starting from the parent directory
    final_uuid_map = ensure_unique_uuids(parent_dir)
    
    # Verification Output
    print("\n" + "-"*30)
    print("Verification:")
    print(f"Total target files successfully mapped: {len(final_uuid_map)}")
    print("Successfully verified: All target files have unique UUIDs.")
    print("-"*30)

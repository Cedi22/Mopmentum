import os
import re

def verify_godot_project(root_dir):
    errors = []
    print(f"Verifying project in {root_dir}...")
    
    # Check all .tscn and .tres files
    for root, dirs, files in os.walk(root_dir):
        if ".godot" in root:
            continue
        for f in files:
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, root_dir)
            if f.endswith(('.tscn', '.tres')):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                # Check load_steps
                first_line = content.split('\n')[0]
                match = re.search(r'load_steps=(\d+)', first_line)
                if match:
                    declared_steps = int(match.group(1))
                    sub_resources = len(re.findall(r'\[sub_resource ', content))
                    ext_resources = len(re.findall(r'\[ext_resource ', content))
                    actual_steps = sub_resources + ext_resources + 1
                    if declared_steps != actual_steps:
                        errors.append(f"{rel_path}: declared load_steps={declared_steps}, but actual is {actual_steps} (sub={sub_resources}, ext={ext_resources})")
                
                # Check ext_resource paths exist
                ext_matches = re.findall(r'path="res://([^"]+)"', content)
                for res_rel in ext_matches:
                    full_res = os.path.join(root_dir, res_rel.replace('/', os.sep))
                    if not os.path.exists(full_res):
                        errors.append(f"{rel_path}: referenced resource does not exist: {res_rel}")

    if errors:
        print(f"Found {len(errors)} issues:")
        for err in errors:
            print("  -", err)
    else:
        print("All scenes, resources, and paths verified with 0 errors!")

if __name__ == "__main__":
    verify_godot_project(r"c:/Users/visita/OneDrive/Documents/Desktop/Test/Mopmentum")

import os
import subprocess
import glob

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e}")

def sanitize():
    print(":::group:::Sanitizing Codebase")
    
    # 1. Update manifest XMLs
    xml_files = glob.glob("manifests/**/*.xml", recursive=True)
    for xml_file in xml_files:
        run_command(f"sed -i 's|github.com/WildKernels/AnyKernel3|github.com/huangdihd/AnyKernel3|g' {xml_file}")
        run_command(f"sed -i 's|fetch=\"https://github.com/WildKernels\" name=\"wild\"|fetch=\"https://github.com/huangdihd\" name=\"wild\"|g' {xml_file}")
        run_command(f"sed -i -E 's/(name=\"AnyKernel3\".*revision=\")[^\"]+(\")/\\1gki-2.0\\2/g' {xml_file}")

    # 2. Update config JSONs
    json_files = glob.glob("configs/**/*.json", recursive=True)
    for json_file in json_files:
        run_command(f"sed -i 's/\"uname\": \"OP-WILD\"/\"uname\": \"OP-RESUKISU\"/g' {json_file}")

    # 3. Update build-kernel action.yml AnyKernel3 URL
    action_path = ".github/actions/build-kernel/action.yml"
    if os.path.exists(action_path):
        run_command(f"sed -i 's|https://github.com/WildKernels/AnyKernel3|https://github.com/huangdihd/AnyKernel3|g' {action_path}")
        
        # 4. Remove KernelSU-Next / KSUN steps
        with open(action_path, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        skip = False
        for line in lines:
            if '- name: Add KernelSU-Next' in line or '- name: Add KSUN' in line:
                skip = True
            elif skip and line.startswith('    - name:'):
                skip = False
            
            if not skip:
                new_lines.append(line)
        
        with open(action_path, 'w') as f:
            f.writelines(new_lines)
            
    print(":::endgroup:::")

if __name__ == "__main__":
    sanitize()

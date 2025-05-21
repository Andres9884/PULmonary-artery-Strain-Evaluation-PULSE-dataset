import os
from tqdm import tqdm
import re
import shutil

# Define input and output folders
input_folder = "Here goes .in file/s to change"
output_folder = "Here goes the destination of changing original file"
os.makedirs(output_folder, exist_ok=True)

# Mapping for elastic modulus values (MPa to name)
modulus_value_mapping = {
    "100": ("0.175", "175"),
    "200": ("0.25", "250"),
    "300": ("0.35", "350")
}

# Iterate over all .in files
for filename in tqdm(os.listdir(input_folder)):
    if filename.endswith(".in") and "ElasticModule" in filename:
        # Extract the original modulus value from filename
        parts = filename.split("_")
        for part in parts:
            if "ElasticModule" in part:
                original_mod = part.replace("ElasticModule", "").strip()
                break
        
        if original_mod not in modulus_value_mapping:
            print(f"❌ Skipping {filename} — Unknown modulus")
            continue
        
        new_modulus_value, new_modulus_label = modulus_value_mapping[original_mod]

        # Read and modify file
        input_path = os.path.join(input_folder, filename)
        with open(input_path, "r") as f:
            lines = f.readlines()

        # Modify the 8th and 9th lines
        lines[7] = f"MP,EX, 1,{new_modulus_value} \n"
        lines[8] = "MP,PRXY,1,0.45 \n"
        lines[-8] = "SOLVE \n"
        lines[-35] = "NSUBST,10,20,1 \n"
        lines[-36] = "AUTOTS,1 \n"
        lines[-38] = "NLGEOM,ON \n"
        lines.pop(-9)

        # Update /OUTPUT line (4th from the end)
        output_line_idx = -4
        if "ElasticModule" in lines[output_line_idx]:
            lines[output_line_idx] = lines[output_line_idx].replace(
                f"ElasticModule{original_mod}_",
                f"ElasticModule{new_modulus_label}_"
            )

        # Rename the output file accordingly
        new_filename = filename.replace(
            f"ElasticModule{original_mod}_",
            f"ElasticModule{new_modulus_label}_"
        )
        output_path = os.path.join(output_folder, new_filename)

        # Write modified content to new file
        with open(output_path, "w") as f:
            f.writelines(lines)

print("✅ All files processed and saved with updated values and names.")

for filename in tqdm(os.listdir(input_folder)):
    if filename.endswith(".in"):
        file_path = os.path.join(input_folder, filename)

        with open(file_path, "r") as f:
            lines = f.readlines()

        # Safely check there are enough lines
        if len(lines) >= 4:
            output_line = lines[-4]
            if "TIENT_FILES\\" in output_line:
                lines[-4] = output_line.replace("TIENT_FILES\\", "")
                print(f"✅ Fixed: {filename}")

                # Save the modified file
                with open(file_path, "w") as f:
                    f.writelines(lines)

print("🎯 Cleanup complete: Removed 'TIENT_FILES\\' from all applicable /OUTPUT lines.")

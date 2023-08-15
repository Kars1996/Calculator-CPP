import os
import shutil
import subprocess

def compile_project():
    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))

    # Step 1: Create a temporary folder for compilation
    temp_folder = os.path.join(root_folder, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    try:
        # Step 2: Copy all project files to the temporary folder
        for root, _, files in os.walk(root_folder):
            relative_path = os.path.relpath(root, root_folder)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(temp_folder, relative_path, file)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy(src_file, dst_file)

        # Step 3: Install the required dependencies into the virtual environment
        requirements_file = os.path.join(temp_folder, "requirements.txt")
        subprocess.run(["pip", "install", "-r", requirements_file])

        # Step 4: Compile the project using PyInstaller within the virtual environment
        main_script = os.path.join(temp_folder, "main.py")
        subprocess.run(["pyinstaller", main_script, "--onefile"])

        print("Compilation completed successfully!")

    finally:
        shutil.rmtree(temp_folder)

if __name__ == "__main__":
    compile_project()

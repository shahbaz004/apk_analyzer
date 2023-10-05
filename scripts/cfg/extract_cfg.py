import os
import subprocess
import concurrent.futures

def process_dex_file(dex_file, output_dir):
    print("output_dir:", output_dir)
    jadx_command = ["jadx", dex_file, "--cfg", "-d", output_dir]
    subprocess.run(jadx_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(os.path.basename(dex_file), ": successfully Control Flow Graphs Created")

def extract_cfg(dex_folder, input_folder):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for root, dirs, files in os.walk(dex_folder):
            if "temp" not in root:
                for filename in files:
                    dex_file = os.path.join(root, filename)
                    output_dir = os.path.join(root)
                    executor.submit(process_dex_file, dex_file, output_dir)

if __name__ == "__main__":
    dex_folder = input("Enter DEX files' Path: ")
    extract_cfg(dex_folder)

import os
import subprocess
import shutil
import zipfile
from scripts.cfg.extract_cfg import extract_cfg
import multiprocessing
import time
import sys


def get_relative_path(input_folder, apk_file):
    return os.path.relpath(apk_file, input_folder)


def extract_dex_from_apk(apk_file, output_dir, input_folder):
    output_dir = output_dir[:-4]
    temp_dir = os.path.join(output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    with zipfile.ZipFile(apk_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    apktool_command = ['apktool', 'd', '-o', output_dir, apk_file]
    subprocess.run(apktool_command, cwd=temp_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    dex_files = [f for f in os.listdir(temp_dir) if f.endswith('.dex')]
    for dex_file in dex_files:
        dex_file = shutil.move(os.path.join(temp_dir, dex_file), os.path.join(output_dir, dex_file))
    extract_cfg(output_dir, input_folder)
    shutil.rmtree(temp_dir)

def process_apk(apk_file, output_folder, input_folder):
    file_name = os.path.splitext(os.path.basename(apk_file))[0]
    relative_path = get_relative_path(input_folder, apk_file)
    output_dir = os.path.join(output_folder, relative_path)

    extract_dex_from_apk(apk_file, output_dir, input_folder)


def process_apk_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    apk_files = [os.path.join(root, file) for root, _, files in os.walk(input_folder) for file in files if
                 file.endswith('.apk')]

    num_apks = len(apk_files)
    num_cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cpus)

    print(f"Processing {num_apks} APK files using {num_cpus} CPUs...")

    start_time = time.time()
    pool.starmap(process_apk, [(apk_file, output_folder, input_folder) for apk_file in apk_files])
    end_time = time.time()

    total_time_minutes = (end_time - start_time) / 60
    print(f"Total time taken: {total_time_minutes:.2f} minutes")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py input_apk_folder")
        sys.exit(1)

    input_apk_folder = sys.argv[1]
    base_directory = os.getcwd()
    output = input_apk_folder.split('/')[-1:]

    output_dex_folder = f'{base_directory}/{output[0]}-out'
    print(output_dex_folder)
    process_apk_files(input_apk_folder, output_dex_folder)

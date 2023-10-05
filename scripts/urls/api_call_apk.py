import os, sys
import re
import time
import openpyxl
import subprocess


def extract_source_code(apk_path, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        print("apk",apk_path)
        jadx_cmd = f"jadx -d {output_dir} {apk_path}"
        start_time = time.time()
        subprocess.run(jadx_cmd, shell=True, check=True)
        end_time = time.time()
        total_time_minutes = (end_time - start_time) / 60
        print(f"Total time taken for {apk_path} ==== {total_time_minutes:.2f} minutes")

        print(f"Source code extracted successfully to {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    except FileNotFoundError:
        print("Error: JADX command not found. Make sure JADX is installed and added to your system PATH.")
        return False


def extract_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        pattern = re.compile(r'\bhttps?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]', re.MULTILINE)
        matches = pattern.findall(content)
        return matches


def find_urls_in_directory(directory):
    urls = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            urls_in_file = extract_urls_from_file(file_path)
            if urls_in_file:
                urls.extend(urls_in_file)
    urls = list(set(urls))
    return urls


def extract_urls_from_directory(apk_folder, output_base_dir):
    urls_list = []
    malicious_urls_list = []
    for root, dirs, files in os.walk(apk_folder):
        for apk_file in files:
            if apk_file.endswith(".apk"):
                apk_path = os.path.join(root, apk_file)
                relative_path = os.path.relpath(apk_path, apk_folder)
                output_dir = os.path.join(output_base_dir, relative_path)[:-4]

                extract_source_code(apk_path, output_dir)
                path = f"{output_dir}/sources"
                urls = find_urls_in_directory(path)
                if urls:
                    if 'Malicious' in output_dir:
                        malicious_urls_list.append([os.path.basename(apk_file), *urls])
                    else:
                        urls_list.append([os.path.basename(apk_file), *urls])
                else:
                    if 'Malicious' in output_dir:
                        li = ["No API Calls found"]
                        malicious_urls_list.append([os.path.basename(apk_file), *li])
                    else:
                        li = ["No API Calls found"]
                        urls_list.append([os.path.basename(apk_file), *li])

    generate_excel(urls_list, output_base_dir, "benign_APIs.xlsx")
    generate_excel(malicious_urls_list, output_base_dir, "malicious_APIs.xlsx")


def generate_excel(urls, output_base_dir, filename):
    excel_file_path = os.path.join(output_base_dir, filename)
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "APIs"

    header_row = ["APK Name", "APIs"]
    worksheet.append(header_row)

    for url in urls:
        worksheet.append(url)

    workbook.save(excel_file_path)
    print(f"Excel file generated: {excel_file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_apk_folder")
        sys.exit(1)

    apk_folder = sys.argv[1]
    output = os.path.basename(apk_folder)
    base_directory = os.getcwd()
    output_base_dir = os.path.join(base_directory, f'{output}-APIs')
    os.makedirs(output_base_dir, exist_ok=True)
    start_time = time.time()
    extract_urls_from_directory(apk_folder, output_base_dir)
    end_time = time.time()
    total_time = (end_time - start_time) / 60
    print(f"Total Time: {total_time:.2f} minutes")

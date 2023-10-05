import os
import re
import csv
import sys
import time
import openpyxl


permission_pattern = re.compile(r'"android.permission.[A-Z_]+', re.MULTILINE)


def extract_permissions_from_sources(apk_folder, output_base_dir):
    permissions_list = []
    malicious_permissions_list = []  # List for permissions in the "malicious" directory
    for root, dirs, files in os.walk(apk_folder):
        for dir_name in dirs:
            if dir_name == 'sources':
                source_dir = os.path.join(root, dir_name)
                print("APK Source:", source_dir)
                permissions = find_permissions_in_directory(source_dir)
                if permissions:
                    if 'Malicious' in source_dir:
                        malicious_permissions_list.append([os.path.basename(root), *permissions])
                    else:
                        permissions_list.append([os.path.basename(root), *permissions])
                else:
                    if 'Malicious' in source_dir:
                        li = ["No Permissions found"]
                        malicious_permissions_list.append([os.path.basename(root), *li])
                    else:
                        li = ["No Permissions found"]
                        permissions_list.append([os.path.basename(root), *li])



    generate_excel(permissions_list, output_base_dir, "permissions.xlsx")
    generate_excel(malicious_permissions_list, output_base_dir, "malicious_permissions.xlsx")


def generate_excel(permissions_list, output_base_dir, filename):
    excel_file_path = os.path.join(output_base_dir, filename)
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Permissions"

    header_row = ["APK Name", "Permissions"]
    worksheet.append(header_row)

    for unique_permissions in permissions_list:
        worksheet.append(unique_permissions)

    workbook.save(excel_file_path)
    print(f"Excel file generated: {excel_file_path}")


def generate_csv(permissions_list, output_base_dir, file_name):
    csv_file_path = os.path.join(output_base_dir, file_name)
    with open(csv_file_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t', lineterminator='\n', )
        header_row = ["APK Name", "Permissions"]
        csv_writer.writerow(header_row)
        for unique_permissions in permissions_list:
            csv_writer.writerow(unique_permissions)
        print(f"CSV GENERATED: {file_name}")


def find_permissions_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        file_contents = file.read()
        permissions = permission_pattern.findall(file_contents)
        return permissions


def find_permissions_in_directory(directory):
    permissions = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            permissions_in_file = find_permissions_in_file(file_path)
            if permissions_in_file:
                permissions.extend(permissions_in_file)
    permissions = list(set(permissions))
    return permissions


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_apk_folder")
        sys.exit(1)

    apk_folder = sys.argv[1]
    output = os.path.basename(apk_folder)
    base_directory = os.getcwd()
    output_base_dir = os.path.join(base_directory, f'{output}-permissions')
    os.makedirs(output_base_dir, exist_ok=True)
    start_time = time.time()
    extract_permissions_from_sources(apk_folder, output_base_dir)
    end_time = time.time()
    total_time = (end_time - start_time) / 60
    print(f"Total Time: {total_time:.2f} minutes")

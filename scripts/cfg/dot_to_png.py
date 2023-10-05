import os
import pydot
import multiprocessing
import time
import timeout_decorator
import sys

@timeout_decorator.timeout(2)
def load_dot_file(input_dot_file):
    graphs = pydot.graph_from_dot_file(input_dot_file)
    return graphs

def convert_dot_to_png(input_dot_file):
    output_png_file = os.path.splitext(input_dot_file)[0] + ".png"

    if os.path.exists(output_png_file):
        print(f"Skipping {input_dot_file} - PNG file already exists.")
        return

    try:
        graphs = load_dot_file(input_dot_file)

        if not graphs:
            print(f"No graphs found in {input_dot_file}.")
            return

        graph = graphs[0]
        try:
            graph.write_png(output_png_file)
            print(f"Conversion successful. PNG file saved as {output_png_file}")
        except Exception as e:
            print(f"Format Error: {output_png_file} - {e}")

    except timeout_decorator.TimeoutError:
        print("The operation took too long and was skipped.")
    except UnicodeDecodeError as ud_err:
        print(f"Skipping Format Error")

def process_dot_files(input_folder, num_processes):
    dot_files = [os.path.join(root, filename) for root, _, files in os.walk(input_folder) for filename in files if filename.endswith(".dot")]

    with multiprocessing.Pool(processes=num_processes) as pool:
        start_time = time.time()

        pool.map(convert_dot_to_png, dot_files)
        end_time = time.time()
        total_time_minutes = (end_time - start_time) / 60
        print(f"Time taken: {total_time_minutes:.2f} minutes")

if __name__ == "__main__":
    input_folder = sys.argv[1]
    num_processes = 2
    print(f"Input folder: {input_folder}")
    print(f"Number of processes: {num_processes}")
    process_dot_files(input_folder, num_processes)

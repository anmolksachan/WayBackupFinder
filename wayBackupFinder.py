import os
import requests
import time
from colorama import init
from termcolor import colored
from threading import Thread
from itertools import cycle

# Loader animation
def loader_animation(message="Processing..."):
    animation = cycle(["|", "/", "-", "\\"])
    while not stop_loader:
        print(f"\r{message} {next(animation)}", end="")
        time.sleep(0.1)
    print("\r" + " " * len(message) + "\r", end="")  # Clear the line

# ASCII Art for aesthetics
def print_ascii_art():
    ascii_art = r'''
    .  .      .__       .          .___      .      
    |  | _.  .[__) _. _.;_/. .._   [__ *._  _| _ ._.
    |/\|(_]\_|[__)(_](_.| \(_|[_)  |   |[ )(_](/,[  
           ._|                |                     
    '''
    print(ascii_art)

print_ascii_art()

# Load extensions from file
def load_extensions_from_file(file_path='extensions.txt'):
    try:
        with open(file_path, 'r') as f:
            extensions = [line.strip() for line in f.readlines() if line.strip()]
        return extensions
    except FileNotFoundError:
        print(colored(f"{file_path} not found. Proceeding with no extensions.", "red"))
        return []

# Load domains from file
def load_domains_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            domains = [line.strip() for line in f.readlines() if line.strip()]
        return domains
    except FileNotFoundError:
        print(colored(f"{file_path} not found. Exiting.", "red"))
        exit()

# Fetch URLs using The Wayback Machine API with streaming and backoff
def fetch_urls(target, file_extensions):
    print(f"\nFetching URLs from The Time Machine Lite for {target}...")
    archive_url = f'https://web.archive.org/cdx/search/cdx?url=*.{target}/*&output=txt&fl=original&collapse=urlkey&page=/'

    global stop_loader
    stop_loader = False
    loader_thread = Thread(target=loader_animation, args=("Fetching URLs...",))
    loader_thread.start()

    max_retries = 3  # Maximum number of retries
    retry_delay = 5  # Delay between retries (in seconds)
    attempt = 0

    while attempt < max_retries:
        try:
            with requests.get(archive_url, stream=True, timeout=60) as response:  # Stream the response
                response.raise_for_status()
                print(colored("\nStreaming response from archive...", "green"))

                url_list = []
                total_lines = 0
                for line in response.iter_lines(decode_unicode=True):  # Process each line incrementally
                    if line:
                        url_list.append(line)
                        total_lines += 1
                        if total_lines % 1000 == 0:  # Show progress every 1000 lines
                            print(f"\rFetched {total_lines} URLs...", end="")

                print(colored(f"\nFetched {total_lines} URLs from archive.", "green"))
                stop_loader = True
                loader_thread.join()
                return {ext: [url for url in url_list if url.lower().endswith(ext.lower())] for ext in file_extensions}
        except requests.exceptions.RequestException as e:
            attempt += 1
            if attempt < max_retries:
                print(colored(f"\nAttempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...", "yellow"))
                time.sleep(retry_delay)
            else:
                print(colored(f"\nError fetching URLs after {max_retries} attempts: {e}", "red"))
                print(colored("The server may be rate-limiting or refusing connections.", "yellow"))
                print(colored("Pausing for 5 minutes before continuing...", "yellow"))
                time.sleep(300)  # Sleep for 5 minutes (300 seconds)
                print(colored("Resuming...", "green"))
                return {}  # Return an empty dictionary after backoff

# Check for archived snapshots
def check_wayback_snapshot(url):
    wayback_url = f'https://archive.org/wayback/available?url={url}'
    try:
        response = requests.get(wayback_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
            snapshot_url = data["archived_snapshots"]["closest"].get("url")
            if snapshot_url:
                print(f"[+] Found possible backup: {colored(snapshot_url, 'green')}")
        else:
            print(f"[-] No archived snapshot found for {url}.")
    except Exception as e:
        print(f"[?] Error checking Wayback snapshot for {url}: {e}")

# Save filtered URLs
def save_urls(target, extension_stats, file_suffix="_filtered_urls.txt"):
    folder = f"content/{target}"
    os.makedirs(folder, exist_ok=True)
    all_filtered_urls = []
    for ext, urls in extension_stats.items():
        if urls:
            file_path = os.path.join(folder, f"{target}_{ext.strip('.')}"+file_suffix)
            with open(file_path, 'w') as file:
                file.write("\n".join(urls))
            all_filtered_urls.extend(urls)
            print(f"Filtered URLs for {ext} saved to: {colored(file_path, 'green')}")
    return all_filtered_urls

# Process domain
def process_domain(target, file_extensions):
    extension_stats = fetch_urls(target, file_extensions)
    if not extension_stats:  # Ensure extension_stats is not empty
        print(colored(f"No URLs fetched for {target}. Skipping...", "yellow"))
        return
    all_filtered_urls = save_urls(target, extension_stats)
    for url in all_filtered_urls:
        check_wayback_snapshot(url)

# Main execution
if __name__ == "__main__":
    init()
    print(colored('    Coded with Love by Anmol K Sachan @Fr13ND0x7f\n', 'green'))

    # Input: Single or multiple domains
    mode = input("Select mode (1: Single Domain, 2: Multiple Domains): ").strip()
    if mode == "1":
        target = input("\nEnter the target domain (e.g., example.com): ").strip()
        if not target:
            print(colored("Target domain is required. Exiting.", "red"))
            exit()
        domains = [target]
    elif mode == "2":
        domain_file = input("\nEnter the path to the file containing domain list: ").strip()
        domains = load_domains_from_file(domain_file)
        print(f"Loaded {len(domains)} domains from {colored(domain_file, 'green')}.")
    else:
        print(colored("Invalid choice. Exiting.", "red"))
        exit()

    # Load default extensions from file
    default_extensions = load_extensions_from_file()
    choice = input("Use custom file extensions or load from extensions.txt? (custom/load): ").strip().lower()
    if choice == "custom":
        file_extensions = input("Enter file extensions to filter (e.g., .zip,.pdf): ").strip().split(",")
    elif choice == "load" and default_extensions:
        file_extensions = default_extensions
    else:
        print(colored("No extensions found. Exiting.", "red"))
        exit()

    # Process each domain
    for target in domains:
        print(colored(f"\nProcessing domain: {target}", "blue"))
        process_domain(target, file_extensions)

    print(colored("\nProcess complete for all domains.", "green"))

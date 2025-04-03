![image](https://github.com/user-attachments/assets/80c07192-187d-4199-a225-8febf8c2e007)

# WayBackup Finder

This Python script fetches URLs from the Wayback Machine and filters them based on specified file extensions. It also checks if archived snapshots are available for each URL and saves the filtered URLs to files.

Read more: <a href="https://anmolksachan.medium.com/unlock-hidden-backups-with-waybackupfinder-py-7b98041a82d9" target="_blank">Medium</a><br>
Watch Tool in action: <a href="https://anmolksachan.medium.com/discovering-backups-secrets-and-more-using-the-waybackupfinder-py-tool-b97f67e95c50">Medium</a>

Community Blogs:<br>
<a href="https://medium.com/@abhirupkonwar04/waybackupfinder-passive-recon-65a49dff050b">WayBackupFinder Passive Recon</a><br>

## Features

- Fetches URLs from the Wayback Machine using the CDX API.
- Filters the fetched URLs by specific file extensions (e.g., `.pdf`, `.zip`).
- Checks if a Wayback snapshot is available for each URL.
- Saves the filtered URLs to text files.
- Customizable file extensions to filter or use default extensions from `extensions.txt`.

## Use Case: Finding Archived Backups

This tool can be especially useful for finding backups of websites or files that may no longer be available on the live site. If a resource (e.g., a PDF or image) was previously available on the website but has since been removed or is temporarily unavailable, there may still be an archived snapshot of it in the Wayback Machine. 

By using this script, you can:

- **Identify URLs** that may have once been accessible but no longer are.
- **Check for backups** on the Wayback Machine that might not be available on the current live site.
- **Retrieve historical versions** of files or content that have been deleted or moved.

The script attempts to retrieve URLs from the Wayback Machine. For each URL found, it checks if an archived snapshot is available. If a snapshot exists, the script provides a link to the backup.

## Requirements

- Python 3.x
- The following Python packages:
  - `requests`
  - `colorama`
  - `termcolor`

You can install the required packages using the following command:

```bash
pip3 install requests colorama termcolor
```

## How to Use

1. Clone the repository or download the script.
2. Ensure you have a file named `extensions.txt` in the same directory as the script, or specify custom file extensions.
3. Run the script:

```bash
python wayBackupFinder.py
```

4. When prompted, enter the target domain (e.g., `example.com`) and specify whether to use custom file extensions or load them from the `extensions.txt` file.
5. The script will:
   - Fetch URLs from the Wayback Machine.
   - Filter the URLs by the provided file extensions.
   - Save the filtered URLs to separate files.
   - Check if archived snapshots are available for each URL.

## Example
![image](https://github.com/user-attachments/assets/4a7652dd-7c43-42aa-a9f0-94f7207dca60)

### Input:

```
Enter the target domain (e.g., example.com): example.com
Would you like to use custom file extensions or load from extensions.txt? (custom/load): load
```

### Output:

The script will print the progress and save the filtered URLs to files such as:

```
Filtered URLs for .pdf saved to: content/example.com/example.com_pdf_filtered_urls.txt
Found possible backup: https://web.archive.org/web/20200101000000/https://example.com/sample.pdf
```

### File Extensions

You can specify custom file extensions to filter by, separated by commas, for example: `.zip,.pdf,.jpg`. If you choose to load extensions from `extensions.txt`, the script will use those.

### File Structure

The script will create a folder called `content` and store the filtered URLs for each extension in subfolders named after the target domain.

## License

This project is licensed under the MIT License - see the [LICENSE](https://raw.githubusercontent.com/anmolksachan/WayBackupFinder/refs/heads/main/LICENSE) file for details.

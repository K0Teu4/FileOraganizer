# File Organizer

> 🗂️ A simple yet powerful console application that automatically organizes files in a folder by their extensions into categorized subfolders.

---

## 📋 Table of Contents

- [Features](#-features)
- [Preview](#-preview)
- [Installation](#-installation)
- [Usage](#-usage)
- [Supported Categories](#-supported-categories)
- [How It Works](#-how-it-works)
- [Logging](#-logging)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 📁 **Automatic sorting** — files are organized by extension into intuitive categories
- 🖼️ **Visual icons** — each category is displayed with a descriptive emoji
- 🔍 **Dry-run preview** — review all planned moves before anything happens
- ⚠️ **Duplicate handling** — automatically renames conflicting files (`file_1.pdf`, `file_2.pdf`, …)
- 📝 **Detailed logging** — every operation is logged to a timestamped `.log` file
- 🛡️ **Safe operation** — hidden files, existing subfolders, and log files are never touched
- 🎨 **Pretty console output** — clean, readable terminal UI with separators and colored prompts

---

## 🖼️ Preview

```
══════════════════════════════════════════════
  📁 FILE ORGANIZER
══════════════════════════════════════════════
  Organize your files automatically by type

  Enter the folder path to organize: /home/user/Downloads

  ✅ Folder selected: /home/user/Downloads

  🔍 Scanning files…

══════════════════════════════════════════════
  📊 SCAN SUMMARY
══════════════════════════════════════════════
  Found 42 files total:
  → 15 images, 12 documents, 8 archives, 7 other files

  🖼️  Images              15 files
  📄 Documents           12 files
  📦 Archives             8 files
  📂 Other                7 files

  Would you like a dry-run preview first? (yes/no): yes

══════════════════════════════════════════════
  🔍 DRY RUN PREVIEW — No files will be moved
══════════════════════════════════════════════
  SOURCE FILE                           →  DESTINATION
  ────────────────────────────────────────────────────────
  photo.jpg                             →  Images/photo.jpg
  report.pdf                            →  Documents/report.pdf
  backup.zip                            →  Archives/backup.zip
  ...

  Total operations planned: 42

  Are you sure you want to proceed? (yes/no): yes

══════════════════════════════════════════════
  🚀 MOVING FILES
══════════════════════════════════════════════
  [   1/42] ✅ photo.jpg                          → Images/
  [   2/42] ✅ report.pdf                         → Documents/
  ...

══════════════════════════════════════════════
  📋 FINAL REPORT
══════════════════════════════════════════════
  ✅ Successfully moved : 42 files
  ❌ Errors encountered : 0 files

  📝 Log file saved at  : /home/user/Downloads/file_organizer_20250115_143052.log

══════════════════════════════════════════════
  Organization complete! 🎉
══════════════════════════════════════════════
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.10+** (uses modern type hints like `dict[str, list[Path]]`)

### Clone the repository

```bash
git clone https://github.com/K0Teu4/file-organizer.git
cd file-organizer
```

### Run the script

No external dependencies are required — the app uses only the Python standard library.

```bash
python main.py
```

---

## 🕹️ Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. Enter the **absolute or relative path** to the folder you want to organize.
3. Review the **scan summary** showing how many files were found in each category.
4. Optionally run a **dry-run preview** to see exactly where each file will go.
5. Confirm to **execute** the organization.

> 💡 **Tip:** You can wrap paths containing spaces in quotes: `"C:\Users\Me\My Folder"`

---

## 📂 Supported Categories

| Category | Extensions |
|----------|------------|
| 🖼️ **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.ico` |
| 📄 **Documents** | `.txt`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.csv`, `.odt` |
| 🎵 **Music** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a` |
| 🎬 **Videos** | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm` |
| 📦 **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz` |
| 📂 **Other** | Everything else |

---

## ⚙️ How It Works

1. **Scan** — reads all top-level files in the target directory (subfolders are ignored).
2. **Categorize** — maps each file extension to a category via the `EXTENSION_MAP` dictionary.
3. **Plan** — builds a move plan with deduplicated destination paths.
4. **Preview (optional)** — shows the plan in a human-readable table.
5. **Execute** — creates subfolders and moves files using `shutil.move`.
6. **Report** — prints a final summary and writes a detailed log.

---

## 📝 Logging

Every session creates a timestamped log file in the target folder, e.g.:

```
file_organizer_20250115_143052.log
```

The log contains:
- Session start/end timestamps
- Full paths of every moved file
- Any errors or permission issues encountered

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ for tidy folders.
</p>

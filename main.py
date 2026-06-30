#!/usr/bin/env python3
"""
File Organizer - A console application to organize files in a folder
Organizes files by extension into categorized subfolders
"""

import os
import shutil
import logging
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# ============================================================
# CONFIGURATION: Extension mappings to folder categories
# ============================================================
EXTENSION_MAP = {
    # Images
    '.jpg':  'Images',
    '.jpeg': 'Images',
    '.png':  'Images',
    '.gif':  'Images',
    '.bmp':  'Images',
    '.svg':  'Images',
    '.webp': 'Images',
    '.ico':  'Images',

    # Documents
    '.txt':  'Documents',
    '.pdf':  'Documents',
    '.doc':  'Documents',
    '.docx': 'Documents',
    '.xls':  'Documents',
    '.xlsx': 'Documents',
    '.ppt':  'Documents',
    '.pptx': 'Documents',
    '.csv':  'Documents',
    '.odt':  'Documents',

    # Music
    '.mp3':  'Music',
    '.wav':  'Music',
    '.flac': 'Music',
    '.aac':  'Music',
    '.ogg':  'Music',
    '.wma':  'Music',
    '.m4a':  'Music',

    # Videos
    '.mp4':  'Videos',
    '.avi':  'Videos',
    '.mkv':  'Videos',
    '.mov':  'Videos',
    '.wmv':  'Videos',
    '.flv':  'Videos',
    '.webm': 'Videos',

    # Archives
    '.zip':  'Archives',
    '.rar':  'Archives',
    '.7z':   'Archives',
    '.tar':  'Archives',
    '.gz':   'Archives',
    '.bz2':  'Archives',
    '.xz':   'Archives',
}

# Folder display names and their emoji icons
FOLDER_ICONS = {
    'Images':    '🖼️  Images',
    'Documents': '📄 Documents',
    'Music':     '🎵 Music',
    'Videos':    '🎬 Videos',
    'Archives':  '📦 Archives',
    'Other':     '📂 Other',
}

# Summary labels used in the final report
SUMMARY_LABELS = {
    'Images':    'image',
    'Documents': 'document',
    'Music':     'music file',
    'Videos':    'video',
    'Archives':  'archive',
    'Other':     'other file',
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def setup_logger(log_path: str) -> logging.Logger:
    """
    Configure and return a logger that writes to both
    the console and a log file.

    Args:
        log_path: Full path to the log file

    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger('FileOrganizer')
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        logger.handlers.clear()

    # --- File handler (always DEBUG level) ---
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # --- Console handler (INFO and above) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_category(extension: str) -> str:
    """
    Return the folder category for a given file extension.

    Args:
        extension: File extension including the dot (e.g. '.jpg')

    Returns:
        Category name string ('Images', 'Documents', etc.)
    """
    return EXTENSION_MAP.get(extension.lower(), 'Other')


def resolve_duplicate(destination: Path) -> Path:
    """
    If the destination path already exists, append an incrementing
    numeric suffix to the stem until a free path is found.

    Example:
        report.pdf  →  report_1.pdf  →  report_2.pdf  …

    Args:
        destination: Desired destination Path

    Returns:
        A Path that does not currently exist on disk
    """
    if not destination.exists():
        return destination

    stem      = destination.stem
    suffix    = destination.suffix
    parent    = destination.parent
    counter   = 1

    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def print_separator(char: str = '─', width: int = 60) -> None:
    """Print a horizontal separator line."""
    print(char * width)


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print()
    print_separator('═')
    print(f"  {title}")
    print_separator('═')


# ============================================================
# CORE FUNCTIONS
# ============================================================

def get_folder_path() -> Path:
    """
    Prompt the user for a folder path and validate it.

    Returns:
        Validated Path object pointing to an existing directory

    Raises:
        SystemExit: If the user enters an invalid path three times
    """
    print_header("📁 FILE ORGANIZER")
    print("  Organize your files automatically by type\n")

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        raw = input("  Enter the folder path to organize: ").strip()

        # Allow quoted paths
        raw = raw.strip('"').strip("'")

        if not raw:
            print("  ⚠️  Path cannot be empty. Please try again.\n")
            attempts += 1
            continue

        folder = Path(raw)

        if not folder.exists():
            print(f"  ❌ Path does not exist: {folder}\n")
            attempts += 1
            continue

        if not folder.is_dir():
            print(f"  ❌ Path is not a directory: {folder}\n")
            attempts += 1
            continue

        return folder.resolve()   # Return absolute, normalized path

    print("\n  Too many invalid attempts. Exiting.")
    raise SystemExit(1)


def scan_files(folder: Path) -> dict[str, list[Path]]:
    """
    Scan the top-level contents of a folder and group files
    by their category.  Subfolders created by this organizer
    are automatically excluded from scanning.

    Args:
        folder: Path to the target directory

    Returns:
        Dictionary mapping category names to lists of file Paths
    """
    # Known organizer subfolder names to skip
    organizer_folders = set(FOLDER_ICONS.keys())

    grouped: dict[str, list[Path]] = defaultdict(list)

    try:
        entries = list(folder.iterdir())
    except PermissionError:
        print(f"  ❌ Permission denied: cannot read '{folder}'")
        raise SystemExit(1)

    for entry in entries:
        # Skip directories (including our own output folders)
        if entry.is_dir():
            continue

        # Skip hidden files (starting with a dot on Unix)
        if entry.name.startswith('.'):
            continue

        # Skip the log file itself so it doesn't get moved
        if entry.name.startswith('file_organizer_') and entry.suffix == '.log':
            continue

        extension = entry.suffix
        category  = get_category(extension)
        grouped[category].append(entry)

    return dict(grouped)


def print_summary(grouped: dict[str, list[Path]]) -> None:
    """
    Display a human-readable summary of discovered files.

    Args:
        grouped: Dictionary mapping categories to file lists
    """
    print_header("📊 SCAN SUMMARY")

    if not grouped:
        print("  No files found in the selected folder.")
        return

    total = sum(len(files) for files in grouped.values())

    # Build summary sentence parts
    parts = []
    for category, files in sorted(grouped.items()):
        count = len(files)
        label = SUMMARY_LABELS.get(category, category.lower())
        parts.append(f"{count} {label}{'s' if count != 1 else ''}")

    print(f"  Found {total} file{'s' if total != 1 else ''} total:")
    print(f"  → {', '.join(parts)}\n")

    # Detailed breakdown per category
    for category, files in sorted(grouped.items()):
        icon  = FOLDER_ICONS.get(category, f'📂 {category}')
        count = len(files)
        print(f"  {icon:<22} {count:>4} file{'s' if count != 1 else ''}")

    print()


def build_move_plan(
    grouped: dict[str, list[Path]],
    folder:  Path
) -> list[tuple[Path, Path]]:
    """
    Build an ordered list of (source, destination) move operations.
    Destination paths are already deduplicated.

    Args:
        grouped: Dictionary mapping categories to file lists
        folder:  Root folder (where subfolders will be created)

    Returns:
        List of (source_path, destination_path) tuples
    """
    plan: list[tuple[Path, Path]] = []

    for category, files in grouped.items():
        target_dir = folder / category

        for src in files:
            raw_dst = target_dir / src.name
            dst     = resolve_duplicate(raw_dst)
            plan.append((src, dst))

    return plan


def preview_plan(plan: list[tuple[Path, Path]], folder: Path) -> None:
    """
    Print the full move plan (dry-run preview) to the console.

    Args:
        plan:   List of (source, destination) tuples
        folder: Root folder used to shorten displayed paths
    """
    print_header("🔍 DRY RUN PREVIEW — No files will be moved")
    print(f"  {'SOURCE FILE':<35} →  {'DESTINATION'}")
    print_separator()

    for src, dst in plan:
        # Show paths relative to the root folder for readability
        try:
            src_rel = src.relative_to(folder)
            dst_rel = dst.relative_to(folder)
        except ValueError:
            src_rel = src
            dst_rel = dst

        # Mark renames caused by duplicate resolution
        renamed = src.name != dst.name
        flag    = " ⚠️  (renamed)" if renamed else ""
        print(f"  {str(src_rel):<35} →  {dst_rel}{flag}")

    print()
    print(f"  Total operations planned: {len(plan)}")
    print()


def confirm_action(prompt: str = "  Proceed? (yes/no): ") -> bool:
    """
    Ask the user for a yes/no confirmation.

    Args:
        prompt: The question to display

    Returns:
        True if user confirmed, False otherwise
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in ('yes', 'y'):
            return True
        if answer in ('no', 'n'):
            return False
        print("  Please type 'yes' or 'no'.")


def execute_plan(
    plan:   list[tuple[Path, Path]],
    folder: Path,
    logger: logging.Logger
) -> tuple[int, int]:
    """
    Execute the move plan: create subfolders and move files.

    Args:
        plan:   List of (source, destination) tuples
        folder: Root folder (for relative path logging)
        logger: Logger instance

    Returns:
        Tuple of (success_count, error_count)
    """
    print_header("🚀 MOVING FILES")

    success_count = 0
    error_count   = 0

    # Pre-create all required subdirectories
    required_dirs = {dst.parent for _, dst in plan}
    for directory in sorted(required_dirs):
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory ensured: {directory}")
        except OSError as exc:
            logger.error(f"Cannot create directory '{directory}': {exc}")
            print(f"  ❌ Cannot create directory: {directory}")
            raise SystemExit(1)

    # Move each file
    for index, (src, dst) in enumerate(plan, start=1):
        try:
            shutil.move(str(src), str(dst))

            # Determine relative paths for display
            try:
                src_rel = src.relative_to(folder)
                dst_rel = dst.relative_to(folder)
            except ValueError:
                src_rel, dst_rel = src, dst

            renamed = src.name != dst.name
            status  = "RENAMED+MOVED" if renamed else "MOVED"

            logger.info(f"{status}: '{src_rel}'  →  '{dst_rel}'")
            print(f"  [{index:>4}/{len(plan)}] ✅ {src.name:<35} → {dst.parent.name}/")

            success_count += 1

        except FileNotFoundError:
            logger.error(f"NOT FOUND: '{src}' — skipped")
            print(f"  [{index:>4}/{len(plan)}] ❌ {src.name} — file not found, skipped")
            error_count += 1

        except PermissionError:
            logger.error(f"PERMISSION DENIED: '{src}' — skipped")
            print(f"  [{index:>4}/{len(plan)}] ❌ {src.name} — permission denied, skipped")
            error_count += 1

        except OSError as exc:
            logger.error(f"OS ERROR moving '{src}': {exc}")
            print(f"  [{index:>4}/{len(plan)}] ❌ {src.name} — error: {exc}")
            error_count += 1

    return success_count, error_count


def print_final_report(
    success: int,
    errors:  int,
    log_path: Path
) -> None:
    """
    Display a final summary report after all operations.

    Args:
        success:  Number of successfully moved files
        errors:   Number of failed operations
        log_path: Path to the written log file
    """
    print_header("📋 FINAL REPORT")
    print(f"  ✅ Successfully moved : {success} file{'s' if success != 1 else ''}")

    if errors:
        print(f"  ❌ Errors encountered : {errors} file{'s' if errors != 1 else ''}")
    else:
        print("  ❌ Errors encountered : 0 files")

    print(f"\n  📝 Log file saved at  : {log_path}")
    print()
    print_separator('═')
    print("  Organization complete! 🎉")
    print_separator('═')
    print()


# ============================================================
# MAIN APPLICATION ENTRY POINT
# ============================================================

def main() -> None:
    """
    Main application flow:
      1. Get and validate folder path
      2. Scan and group files
      3. Show summary
      4. Optional dry-run preview
      5. Confirm and execute
      6. Report results
    """

    # ── Step 1: Get folder path ───────────────────────────────
    folder = get_folder_path()
    print(f"\n  ✅ Folder selected: {folder}\n")

    # ── Step 2: Set up logging ────────────────────────────────
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"file_organizer_{timestamp}.log"
    log_path = folder / log_filename

    logger = setup_logger(str(log_path))
    logger.info(f"Session started — organizing folder: {folder}")

    # ── Step 3: Scan files ────────────────────────────────────
    print("  🔍 Scanning files…")
    grouped = scan_files(folder)

    if not grouped:
        print("\n  ℹ️  No files found to organize. Exiting.")
        logger.info("No files found — nothing to do.")
        return

    # ── Step 4: Show summary ──────────────────────────────────
    print_summary(grouped)

    # ── Step 5: Build move plan ───────────────────────────────
    plan = build_move_plan(grouped, folder)

    # ── Step 6: Dry-run preview ───────────────────────────────
    print_separator()
    if confirm_action("  Would you like a dry-run preview first? (yes/no): "):
        preview_plan(plan, folder)
        print_separator()

    # ── Step 7: Confirm before executing ─────────────────────
    print()
    print(f"  ⚠️  This will move {len(plan)} file(s) into subfolders of:")
    print(f"     {folder}")
    print()

    if not confirm_action("  Are you sure you want to proceed? (yes/no): "):
        print("\n  ⚠️  Operation cancelled by user. No files were moved.")
        logger.info("Operation cancelled by user.")
        return

    # ── Step 8: Execute ───────────────────────────────────────
    logger.info(f"Executing plan — {len(plan)} operations")
    success, errors = execute_plan(plan, folder, logger)

    # ── Step 9: Final report ──────────────────────────────────
    logger.info(f"Session complete — {success} moved, {errors} errors")
    print_final_report(success, errors, log_path)


# ============================================================
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  ⚠️  Interrupted by user (Ctrl+C). Exiting.")
        raise SystemExit(0)
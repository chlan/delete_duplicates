#!/usr/bin/env python3

import argparse
import os
import shutil

def find_duplicates(directory, preferred_ext, default_ext, recursive):

    files_to_delete = []
    files_to_keep = []

    # Durchsuche das Verzeichnis
    for root, dirs, files in os.walk(directory, topdown=True):
        if not recursive:
            # Nicht rekursiv, breche die Schleife nach dem ersten Durchgang ab
            dirs[:] = []

        grouped_files = {}
        # Gruppieren der Dateien nach Namen ohne Erweiterung
        for file in files:
            name, ext = os.path.splitext(file)
            ext = ext[1:]  # entferne den Punkt
            if ext == preferred_ext or ext == default_ext:
                if name in grouped_files:
                    grouped_files[name].append(ext)
                else:
                    grouped_files[name] = [ext]

        # Entscheiden, welche Dateien zu löschen oder zu behalten sind
        for name, exts in grouped_files.items():
            if preferred_ext in exts and default_ext in exts:
                files_to_keep.append(f"{name}.{preferred_ext}")
                files_to_delete.append(f"{name}.{default_ext}")
            elif preferred_ext in exts:
                files_to_keep.append(f"{name}.{preferred_ext}")
            elif default_ext in exts:
                files_to_keep.append(f"{name}.{default_ext}")

    files_to_delete.sort()
    files_to_keep.sort()
    # print("Files to keep", files_to_keep)
    # print("Files to delete", files_to_delete)

    return files_to_keep, files_to_delete

def delete_files(files, dry_run):
    if dry_run:
        print("Dry run aktiviert. Folgende Dateien würden gelöscht:")
    for file in files:
        if dry_run:
            print(file)
        else:
            os.remove(file)
            print(f"Datei gelöscht: {file}")

def main():
    parser = argparse.ArgumentParser(description="Sucht und löscht Duplikate basierend auf Dateierweiterungen.")
    parser.add_argument("-p", "--preferred", type=str, required=True, help="Bevorzugte Dateierweiterung.")
    parser.add_argument("-d", "--default", type=str, required=True, help="Standard Dateierweiterung.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Suche rekursiv in Unterordnern.")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Zeigt Vorgänge nur an, führt sie aber nicht aus.")
    args = parser.parse_args()

    # Dateien suchen
    files_to_keep, files_to_delete = find_duplicates(".", args.preferred, args.default, args.recursive)

    # Ergebnisse ausgeben
    print("Zu erhaltende Dateien:")
    for file in files_to_keep:
        print(file)

    # Dateien löschen, falls nicht Dry Run
    delete_files(files_to_delete, args.dry_run)

if __name__ == "__main__":
    main()

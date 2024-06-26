#!/usr/bin/env python3

import argparse
import os
import shutil

def find_duplicates(directory, preferred_ext, default_ext, recursive, verbose):

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
            ext = ext[1:]  # entferne den Punkt und konvertiere zu Kleinbuchstaben
            base_name = os.path.join(root, name)
            if ext == preferred_ext or ext == default_ext:
                if base_name in grouped_files:
                    grouped_files[base_name].append(ext)
                else:
                    grouped_files[base_name] = [ext]

        # Entscheiden, welche Dateien zu löschen oder zu behalten sind
        for base_name, exts in grouped_files.items():
            if preferred_ext in exts and default_ext in exts:
                files_to_keep.append(f"{base_name}.{preferred_ext}")
                files_to_delete.append(f"{base_name}.{default_ext}")
                if verbose:
                    print(f"Beibehalten: {base_name}.{preferred_ext}, Löschen: {base_name}.{default_ext}")
            elif preferred_ext in exts:
                files_to_keep.append(f"{base_name}.{preferred_ext}")
                if verbose:
                    print(f"Beibehalten (nur bevorzugt vorhanden): {base_name}.{preferred_ext}")
            elif default_ext in exts:
                files_to_keep.append(f"{base_name}.{default_ext}")
                if verbose:
                    print(f"Beibehalten (nur standard vorhanden): {base_name}.{default_ext}")

    files_to_delete.sort()
    files_to_keep.sort()

    if verbose:
        print(f"Anzahl zu behaltende Dateien: {len(files_to_keep)}")
        print(f"Anzahl zu löschender Dateien: {len(files_to_delete)}")

    return files_to_keep, files_to_delete

def delete_files(files, dry_run, verbose):
    if dry_run:
        print(f"Dry run aktiviert. Folgende {len(files)} Dateien würden gelöscht:")
    for file in files:
        if dry_run:
            if verbose:
                print(file, end="", sep="")
        else:
            try:
                os.remove(file)
                if verbose:
                    print(f"Datei gelöscht: {file}")
            except FileNotFoundError:
                if verbose:
                    print(f"Datei nicht gefunden: {file}")
    print()

def main():
    parser = argparse.ArgumentParser(description="Sucht und löscht Duplikate basierend auf Dateierweiterungen.")
    parser.add_argument("-p", "--preferred", type=str, required=True, help="Bevorzugte Dateierweiterung.")
    parser.add_argument("-d", "--default", type=str, required=True, help="Standard Dateierweiterung.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Suche rekursiv in Unterordnern.")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Zeigt Vorgänge nur an, führt sie aber nicht aus.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Zeigt detaillierte Ausgaben an.")
    args = parser.parse_args()

    # Dateien suchen
    files_to_keep, files_to_delete = find_duplicates(".", args.preferred, args.default, args.recursive, args.verbose)

    # Ergebnisse ausgeben
    print(f"{len(files_to_keep)} zu erhaltende Dateien")
    if args.verbose:
        for file in files_to_keep:
            print(file, end="", sep="")
        print()

    # Dateien löschen, falls nicht Dry Run
    delete_files(files_to_delete, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()

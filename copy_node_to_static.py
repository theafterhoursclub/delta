import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NODE_MODULES = os.path.join(BASE_DIR, "node_modules")
STATIC_BOOTSTRAP = os.path.join(BASE_DIR, "static", "bootstrap")
STATIC_SORTABLE = os.path.join(BASE_DIR, "static", "sortable")

def copy_file(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Copied {src} -> {dest}")

def main():
    files_to_copy = [
        # Bootstrap files
        (os.path.join("bootstrap", "dist", "css", "bootstrap.min.css"), "css/bootstrap.min.css"),
        (os.path.join("bootstrap", "dist", "js", "bootstrap.bundle.min.js"), "js/bootstrap.bundle.min.js"),
        # SortableJS file
        (os.path.join("sortablejs", "Sortable.min.js"), "Sortable.min.js"),
    ]
    for src_rel, dest_rel in files_to_copy:
        if "bootstrap" in src_rel:
            src = os.path.join(NODE_MODULES, src_rel)
            dest = os.path.join(STATIC_BOOTSTRAP, dest_rel)
        elif "sortablejs" in src_rel:
            src = os.path.join(NODE_MODULES, src_rel)
            dest = os.path.join(STATIC_SORTABLE, dest_rel)
        else:
            continue
        copy_file(src, dest)

if __name__ == "__main__":
    main()

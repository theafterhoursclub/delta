"""Script to copy selected files from node_modules to the Django static directory."""

import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NODE_MODULES = os.path.join(BASE_DIR, "node_modules")
STATIC_BOOTSTRAP = os.path.join(BASE_DIR, "static", "bootstrap")
STATIC_SORTABLE = os.path.join(BASE_DIR, "static", "sortable")
STATIC_AGGRID = os.path.join(BASE_DIR, "static", "ag-grid")
STATIC_TINYMCE = os.path.join(BASE_DIR, "static", "tinymce")


def copy_file(src, dest):
    """Copy a single file from src to dest, creating directories as needed."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Copied {src} -> {dest}")


def main():
    """Copy required frontend dependencies from node_modules to static folders."""
    files_to_copy = [
        # Bootstrap files
        (
            os.path.join("bootstrap", "dist", "css", "bootstrap.min.css"),
            "css/bootstrap.min.css",
        ),
        (
            os.path.join("bootstrap", "dist", "js", "bootstrap.bundle.min.js"),
            "js/bootstrap.bundle.min.js",
        ),
        # SortableJS file
        (os.path.join("sortablejs", "Sortable.min.js"), "Sortable.min.js"),
        # AG Grid files
        (
            os.path.join(
                "ag-grid-community", "dist", "ag-grid-community.min.noStyle.js"
            ),
            "ag-grid-community.min.noStyle.js",
        ),
        (
            os.path.join("ag-grid-community", "styles", "ag-grid.css"),
            "styles/ag-grid.css",
        ),
        (
            os.path.join("ag-grid-community", "styles", "ag-theme-alpine.css"),
            "styles/ag-theme-alpine.css",
        ),
        # TinyMCE file
        (os.path.join("tinymce", "tinymce.min.js"), "tinymce.min.js"),
    ]
    for src_rel, dest_rel in files_to_copy:
        if "bootstrap" in src_rel:
            src = os.path.join(NODE_MODULES, src_rel)
            dest = os.path.join(STATIC_BOOTSTRAP, dest_rel)
        elif "sortablejs" in src_rel:
            src = os.path.join(NODE_MODULES, src_rel)
            dest = os.path.join(STATIC_SORTABLE, dest_rel)
        elif "ag-grid-community" in src_rel:
            src = os.path.join(NODE_MODULES, src_rel)
            dest = os.path.join(STATIC_AGGRID, dest_rel)
        elif "tinymce" in src_rel:
            src = os.path.join(NODE_MODULES, src_rel)
            dest = os.path.join(STATIC_TINYMCE, dest_rel)
        else:
            continue
        copy_file(src, dest)


if __name__ == "__main__":
    main()

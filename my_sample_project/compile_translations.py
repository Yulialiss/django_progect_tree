import polib
import os

def compile_po_to_mo(po_filepath, mo_filepath):
    po = polib.pofile(po_filepath)
    po.save_as_mofile(mo_filepath)

base_dir = r"C:\Users\User\PycharmProjects567890\pythonProject34567890\django_progect_tree\my_sample_project\blog_app\locale"
languages = ["uk", "ru"]

for lang in languages:
    po_file = os.path.join(base_dir, lang, "LC_MESSAGES", "django.po")
    mo_file = os.path.join(base_dir, lang, "LC_MESSAGES", "django.mo")
    if os.path.exists(po_file):
        compile_po_to_mo(po_file, mo_file)
        print(f"Compiled {po_file} to {mo_file}")
    else:
        print(f"File not found: {po_file}")

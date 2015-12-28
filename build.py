from cx_Freeze import setup, Executable
import os

DEBUG = True
company_name = "arthurwut"
product_name = "pygametest"
versionNumbers = [0, 2, 0]
try:
    versionNumbers[2] = len(os.listdir("dist"))
except:
    pass

version = "%s.%s.%s" % tuple(map(str, versionNumbers))

bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
}

buildOptions = {
    "include_files" : ['data/'],
    "packages" : ["source"]
}
execs = [Executable("main.py", base = None if DEBUG else "Win32GUI", shortcutName = product_name, shortcutDir = "DesktopFolder")]

setup(
    name = "pygame-testing",
    version = version,
    description = "Testing for pygame",
    options = {
        "build_exe" : buildOptions,
        "bdist_msi" : bdist_msi_options
    },
    executables = execs
)

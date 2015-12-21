from cx_Freeze import setup, Executable

DEBUG = True 
company_name = "arthurwut"
product_name = "pygametest"

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
    version = "0.1",
    description = "Testing for pygame",
    options = {
        "build_exe" : buildOptions,
        "bdist_msi" : bdist_msi_options
    },
    executables = execs
)

import sys
import os
import re
import pathlib


def fiddle_serial_number(application_dot_xml_text):
    trial_serial_regex = r'(<Data key="TrialSerialNumber">)(\d+)(</Data>)'
    m = re.search(trial_serial_regex, application_dot_xml_text)
    trial_serial = int(m[2])
    new_trial_serial = trial_serial + 1
    repl = r'<Data key="TrialSerialNumber">' + str(new_trial_serial) + '</Data>'
    return re.sub(trial_serial_regex, repl, application_dot_xml_text)


def find_application_xml(adobe_product_install_dir):
    adobe_product_install_dir = pathlib.Path(adobe_product_install_dir)
    if not adobe_product_install_dir.is_dir():
        raise RuntimeError(f"{adobe_product_install_dir} is not a directory")
    candidates = adobe_product_install_dir.glob('**/application.xml')
    candidates = [*candidates]
    if len(candidates) == 0:
        raise RuntimeError(f"{adobe_product_install_dir} has no application.xml beneath it")
    return candidates[0]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    # Program takes the installation directory of the Adobe product
    # e.g. "C:/Program Files/Adobe/Adobe Premiere Pro CC 2018"
    #         ^             ^     ^^^ backslash important! (fuck windows)
    adobe_product_install_dir = pathlib.Path(sys.argv[1])
    application_dot_xml = find_application_xml(adobe_product_install_dir)
    with open(application_dot_xml, "r+") as f:
        text = f.read()
        output = fiddle_serial_number(text)
        assert(len(output) == len(text))
    with open(application_dot_xml, "w") as f:
        f.write(output)

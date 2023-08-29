import pytest
import random
import string
import yaml
from datetime import datetime


with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)

# Создание экземпляра SSHCheckers
# ssh_checkers = SSHCheckers(ssh_executor)  # Предполагается, что ssh_executor создан ранее

@pytest.fixture()
def make_folders(ssh_checkers):
    cmd = "mkdir {} {} {} {}".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"])
    return ssh_checkers.checkout(cmd, "")

@pytest.fixture()
def clear_folders(ssh_checkers):
    cmd = "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_in"], data["folder_ext"], data["folder_ext2"])
    return ssh_checkers.checkout(cmd, "")

@pytest.fixture()
def make_files(ssh_checkers):
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        cmd = "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename, data["bs"])
        if ssh_checkers.checkout(cmd, ""):
            list_of_files.append(filename)
    return list_of_files

@pytest.fixture()
def make_subfolder(ssh_checkers):
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    cmd1 = "cd {}; mkdir {}".format(data["folder_in"], subfoldername)
    cmd2 = "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername, testfilename)
    if ssh_checkers.checkout(cmd1, ""):
        if ssh_checkers.checkout(cmd2, ""):
            return subfoldername, testfilename
        else:
            return subfoldername, None
    else:
        return None, None

@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))

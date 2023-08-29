import pytest
import yaml
from checkers import SSHCheckers, SSHExecutor

with open('config.yaml') as f:
    data = yaml.safe_load(f)

# Создание экземпляра SSHExecutor
ssh_executor = SSHExecutor(data["ssh_host"], data["ssh_username"], data["ssh_password"])

# Создание экземпляра SSHCheckers
ssh_checkers = SSHCheckers(ssh_executor)

class TestPositive:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Подготовка окружения для тестов
        ssh_checkers.checkout("mkdir {}".format(data["folder_in"]), "")
        yield
        # Очистка окружения после тестов
        ssh_checkers.checkout("rm -rf {}/*".format(data["folder_in"]), "")

    def test_step1(self, make_folders):
        # test1
        cmd1 = "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"])
        cmd2 = "ls {}".format(data["folder_out"])
        res1 = ssh_checkers.checkout(cmd1, "Everything is Ok")
        res2 = ssh_checkers.checkout(cmd2, "arx.7z")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        cmd1 = "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"])
        cmd2 = "cd {}; 7z e arx.7z -o{} -y".format(data["folder_out"], data["folder_ext"])
        res.append(ssh_checkers.checkout(cmd1, "Everything is Ok"))
        res.append(ssh_checkers.checkout(cmd2, "Everything is Ok"))
        for item in make_files:
            cmd3 = "ls {}".format(data["folder_ext"])
            res.append(ssh_checkers.checkout(cmd3, item))
        assert all(res)

    def test_step3(self):
        # test3
        cmd = "cd {}; 7z t arx.7z".format(data["folder_out"])
        assert ssh_checkers.checkout(cmd, "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        cmd = "cd {}; 7z u arx2.7z".format(data["folder_in"])
        assert ssh_checkers.checkout(cmd, "Everything is Ok"), "test4 FAIL"

    def test_step5(self, make_folders, clear_folders, make_files, print_time):
        # test5
        cmd1 = "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"])
        ssh_checkers.checkout(cmd1, "Everything is Ok")
        res = []
        for i in make_files:
            cmd2 = "cd {}; 7z l arx.7z".format(data["folder_out"])
            res.append(ssh_checkers.checkout(cmd2, i))
        assert all(res), "test5 FAIL"

    def test_step6(self, make_folders, clear_folders, make_files, make_subfolder, print_time):
        # test6
        cmd1 = "cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"])
        ssh_checkers.checkout(cmd1, "Everything is Ok")
        cmd2 = "cd {}; 7z x arx.7z -o{} -y".format(data["folder_out"], data["folder_ext2"])
        ssh_checkers.checkout(cmd2, "Everything is Ok")
        res = []
        for i in make_files:
            cmd3 = "ls {}".format(data["folder_ext2"])
            res.append(ssh_checkers.checkout(cmd3, i))
        cmd4 = "ls {}".format(data["folder_ext2"])
        res.append(ssh_checkers.checkout(cmd4, make_subfolder[0]))
        cmd5 = "ls {}/{}".format(data["folder_ext2"], make_subfolder[0])
        res.append(ssh_checkers.checkout(cmd5, make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self):
        # test7
        cmd = "cd {}; 7z d arx.7z".format(data["folder_out"])
        assert ssh_checkers.checkout(cmd, "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for i in make_files:
            cmd1 = "cd {}; 7z h {}".format(data["folder_in"], i)
            cmd2 = "cd {}; crc32 {}".format(data["folder_in"], i)
            hash = ssh_checkers.getout(cmd2).upper()
            res.append(ssh_checkers.checkout(cmd1, "Everything is Ok"))
            res.append(ssh_checkers.checkout(cmd1, hash))
        assert all(res), "test8 FAIL"

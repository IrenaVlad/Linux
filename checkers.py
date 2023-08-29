import subprocess
import paramiko


class SSHExecutor:
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, self.port, self.username, self.password)

    def execute_command(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def close(self):
        self.client.close()

class SSHCheckers:
    def __init__(self, ssh_executor):
        self.ssh_executor = ssh_executor

    def checkout(self, cmd, text):
        stdout, _ = self.ssh_executor.execute_command(cmd)
        print(stdout)
        if text in stdout:
            return True
        else:
            return False

    def checkout_negative(self, cmd, text):
        stdout, stderr = self.ssh_executor.execute_command(cmd)
        if (text in stdout or text in stderr):
            return True
        else:
            return False

    def getout(self, cmd):
        stdout, _ = self.ssh_executor.execute_command(cmd)
        return stdout

# Создание экземпляра SSHExecutor
# ssh_executor = SSHExecutor(data["ssh_host"], data["ssh_username"], data["ssh_password"])

# Создание экземпляра SSHCheckers
# ssh_checkers = SSHCheckers(ssh_executor)

"""_summary_
logging functionality.
"""

import json


class Log:
    """_summary_
    Class represents the logging functionality.
    """
    def __init__(self) -> None:
        """
        constructor.
        """
        self.dump = []

    def _add_log(self, log_message: str) -> None:
        """_summary_
        adds a log message to the dump and prints it to the console.
        """
        self.dump.append(log_message)
        print(log_message)

    def info(self, log_message: str) -> str:
        """_summary_
        adds an info log message. consumer method.
        """
        self._add_log(f"[INFO] {log_message}")
        return (f"[INFO] {log_message}")

    def warning(self, log_message: str) -> str:
        """_summary_
        adds a warning log message. consumer method.
        """
        self._add_log(f"[WARNING] {log_message}")
        return f"[WARNING] {log_message}"

    def error(self, log_message: str) -> str:
        """_summary_
        adds an error log message. consumer method.
        """
        self._add_log(f"[ERROR] {log_message}")
        return f"[ERROR] {log_message}"

    def debug(self, log_message: str) -> str:
        """_summary_
        adds a debug log message. consumer method.
        """
        self._add_log(f"[DEBUG] {log_message}")
        return f"[DEBUG] {log_message}"

    def dump_logs(self) -> dict:
        """_summary_
        dumps the logs to the console. consumer method.
        """
        # package the logs into a json object and return it
        json_logs: dict = json.loads(json.dumps(self.dump))
        return json_logs

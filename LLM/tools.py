from langchain.tools import tool
import subprocess

@tool
def open_app(app_name: str) -> str:
    """Useful for opening the application the user want to open"""
    from sys import platform
    if platform == "linux" or platform == "linux2":
        # linux
        subprocess.run(app_name)
    elif platform == "darwin":
        # MAC OS
        subprocess.run(["open", "-a", app_name])
    elif platform == "win32":
        # Windows
        subprocess.run(["cmd", "/c", "start", "", app_name], shell=True)
    return f"{app_name} is opened."

@tool
def close_app(app_name: str) -> str:
    """Useful for closing the application the user want to close"""
    from sys import platform
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        # linux or MacOS
        subprocess.run(["pkill", app_name])
    elif platform == "win32":
        # Windows

        subprocess.run(["powershell", "-Command", f"Stop-Process -Name {app_name} -Force"], shell = True)

    return f"{app_name} is closed."

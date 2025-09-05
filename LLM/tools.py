from langchain.tools import tool
import subprocess
@tool
def check_working() -> str:
    """Useful for when user want to check if the tool function is working"""
    return 'Tool is working!!!'

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
        subprocess.run(["start", app_name])
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
        subprocess.run(["Stop-Process -Name ", app_name])

    return f"{app_name} is closed."

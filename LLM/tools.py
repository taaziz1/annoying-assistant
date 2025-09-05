from langchain.tools import tool
import subprocess
import webbrowser

@tool
def open_app(app_name: str) -> str:
    """Useful for opening the application the user want to open"""
    from sys import platform
    try:
        if platform == "linux" or platform == "linux2":
            # linux
            subprocess.run(app_name)
        elif platform == "darwin":
            # MAC OS
            subprocess.run(["open", "-a", app_name])
        elif platform == "win32":
            # Windows
            subprocess.run(["cmd", "/c", "start", "", app_name], shell=True)
    except Exception as e:
        return f"Error: {e}"
    return f"{app_name} has been opened."

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

    return f"{app_name} has been closed."

@tool
def go_to_url(location: str) -> str:
    """Open a URL in the system default browser"""
    try:
        webbrowser.open(location)
        return f"The URL was opened in your browser."
    except Exception:
        return f"Cannot go to {location}."

@tool
def google_search(query: str) -> str:
    """Search on Google the content that is given in query, use this when you need to access the Internet to access information"""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Google search for {query} is opened in your browser."

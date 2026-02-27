import subprocess
import sys
import platform


def install_requirements():
    print("=" * 50)
    print("Step 1: Installing dependencies...")
    print("=" * 50)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"]
    )
    print("Dependencies installed successfully.\n")


def print_environment_info():
    print("=" * 50)
    print("Step 2: Environment Information")
    print("=" * 50)
    print(f"  Python version : {platform.python_version()}")
    print(f"  Platform       : {platform.system()} {platform.release()}")
    print(f"  Executable     : {sys.executable}")
    print()


def hello_world():
    print("=" * 50)
    print("Step 3: Hello World!")
    print("=" * 50)
    print("  Hello from Cloudera AI AMP!")
    print("  This is your first AMP running on Cloudera AI.")
    print()
    print("  Next steps:")
    print("  - Explore the .project-metadata.yaml to understand AMP structure")
    print("  - Try adding a Job task in the next level AMP")
    print("=" * 50)


if __name__ == "__main__":
    install_requirements()
    print_environment_info()
    hello_world()

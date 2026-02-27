import subprocess
import sys
import platform


def install_requirements():
    print("=" * 55)
    print("  Step 1: Installing Python dependencies")
    print("=" * 55)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"]
    )
    print("  All dependencies installed successfully.\n")


def verify_imports():
    print("=" * 55)
    print("  Step 2: Verifying installed packages")
    print("=" * 55)
    packages = {"requests": "requests", "pandas": "pandas"}
    for display_name, module_name in packages.items():
        try:
            mod = __import__(module_name)
            version = getattr(mod, "__version__", "unknown")
            print(f"  [OK] {display_name} == {version}")
        except ImportError:
            print(f"  [FAIL] {display_name} not found")
            sys.exit(1)
    print()


def print_environment_info():
    print("=" * 55)
    print("  Step 3: Runtime Environment")
    print("=" * 55)
    print(f"  Python version : {platform.python_version()}")
    print(f"  Platform       : {platform.system()} {platform.release()}")
    print(f"  Executable     : {sys.executable}")
    print()
    print("  Setup complete. The Job task will run next.")
    print("=" * 55)


if __name__ == "__main__":
    install_requirements()
    verify_imports()
    print_environment_info()

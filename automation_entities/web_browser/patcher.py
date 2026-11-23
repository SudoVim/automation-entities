import os
import shutil
import subprocess
from distutils.version import LooseVersion
from typing import Optional

import undetected_chromedriver as uc
from undetected_chromedriver.patcher import IS_POSIX


class Patcher(uc.Patcher):
    """
    Local version of the undetected-chromedriver Patcher so swap out as much
    functionality as I'm willing to support.
    """

    def find_patch_chromedriver(self) -> str:
        """
        Find or patch chromedriver that works with the chrome/chromium version
        that's currently installed.
        """
        import pdb

        pdb.set_trace()
        self.load_versions_from_chrome()

        # First, check to see if we already have our binary installed +
        # patched.
        if self.is_chromedriver_installed():
            return self.executable_path

        # If we don't even have a chromedriver installed locally, perform the
        # standard download mechanism from Google.
        chromedriver_executable = self.find_chromedriver_executable()
        if chromedriver_executable is not None and self.copy_patch_chromedriver(
            chromedriver_executable
        ):
            return self.executable_path

        return self.download_chromedriver()

    def load_versions_from_chrome(self) -> None:
        """
        Load versions from any discovered chrome/chromium executable. This will
        be used to compare to the local chromedriver already patched or
        discover new chromedrivers to patch.
        """
        chrome_executable = uc.find_chrome_executable()
        self.version_full = self.get_version_from_executable(chrome_executable)
        self.version_main = self.version_full.version[0]

    def is_chromedriver_installed(self) -> bool:
        """
        Checks to see if we already have the chromedriver of the correct
        version installed and patched.
        """
        if not os.path.exists(self.executable_path) or not os.access(
            self.executable_path, os.X_OK
        ):
            return False

        installed_version = self.get_version_from_executable(self.executable_path)
        if installed_version == self.version_full and self.is_binary_patched():
            return True

        return False

    def download_chromedriver(self) -> str:
        _ = self.unzip_package(self.fetch_package())
        return self.patch_chromedriver()

    def patch_chromedriver(self) -> str:
        if not self.patch():
            raise AssertionError("Failed to patch chromedriver")

        return self.executable_path

    def copy_patch_chromedriver(self, chromedriver_executable: str) -> Optional[str]:
        """
        Copy and patch the given *chromedriver_executable*.
        """
        chromium_version_full = self.get_version_from_executable(
            chromedriver_executable
        )
        if chromium_version_full != self.version_full:
            return None

        os.makedirs(os.path.dirname(self.executable_path), mode=0o755, exist_ok=True)
        shutil.copyfile(chromedriver_executable, self.executable_path)
        os.chmod(self.executable_path, 0o755)
        return self.patch_chromedriver()

    @staticmethod
    def get_version_from_executable(executable: str) -> LooseVersion:
        out = subprocess.check_output(
            [
                executable,
                "--version",
            ],
        )

        return LooseVersion(out.decode().split()[1])

    @staticmethod
    def find_chromedriver_executable() -> Optional[str]:
        """
        Finds the chromedriver executable
        """
        candidates = set()
        if IS_POSIX:
            for item in os.environ.get("PATH").split(os.pathsep):
                for subitem in ("chromedriver",):
                    candidates.add(os.sep.join((item, subitem)))

        for candidate in candidates:
            if os.path.exists(candidate) and os.access(candidate, os.X_OK):
                return os.path.normpath(candidate)

        return None

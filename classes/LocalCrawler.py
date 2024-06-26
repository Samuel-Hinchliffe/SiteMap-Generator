import os
import json
import re
import requests
from datetime import datetime, timezone


class LocalCrawler:
    """
    A class that represents a local directory crawler.

    Attributes:
        root (str): The root directory to start crawling from.
        quiet (bool): A flag indicating whether to suppress output messages.
        files (list[str]): A list of file paths found during the crawl.
        dirs (list[str]): A list of directory paths found during the crawl.
        blackList (dict[str, list[str]]): The loaded blacklist.

    Methods:
        __init__(self, root: str, quiet: bool) -> None:
            Initializes a LocalCrawler object.

        crawl(self) -> list[str]:
            Crawls through the specified root directory and returns a list of files.

        loadBlacklist(self) -> dict[str, list[str]]:
            Loads the blacklist from the 'blackList.json' file.
    """

    def __init__(self, root: str, quiet: bool, domain: str, checkOnline: bool) -> None:
        self.root = root
        self.files = []
        self.dirs = []
        self.domain = domain
        self.quiet = quiet
        self.checkOnline = checkOnline
        self.blackList = self.loadBlacklist()

        self.lastMod = {}

        self.fixDomain()

    def fixDomain(self) -> None:
        # domain must have a trailing slash
        if not self.domain.endswith("/"):
            self.domain += "/"

    def fixPaths(self, path) -> None:
        # if anything has \\ replace it with /

        return path.replace("\\", "/")

    def crawl(self) -> list[str]:
        """
        Crawls through the specified root directory and returns a list of files.

        Returns:
            A list of file paths found during the crawl.
        """
        for root, dirs, files in os.walk(self.root):

            # Exclude directories matching folderPatterns
            dirs[:] = [
                d
                for d in dirs
                if not any(
                    re.match(pattern, d) for pattern in self.blackList["folderPatterns"]
                )
            ]

            # Exclude files matching filePatterns
            files = [
                f
                for f in files
                if not any(
                    re.match(pattern, f) for pattern in self.blackList["filePatterns"]
                )
            ]

            # For each file in the current directory.
            # If the file is in the blacklist, skip it, if not, add it to the list of files.
            for file in files:

                # Blacklist check
                if file in self.blackList["fileNames"]:
                    if not self.quiet:
                        print(f"Skipping {file} because it is in the blacklist")
                    continue

                # Blacklist check
                file_extension = file.split(".")[-1].lower()
                if file_extension in self.blackList["fileExtensions"]:
                    if not self.quiet:
                        print(f"Skipping {file} because it is a {file_extension} file")
                    continue

                # If the file is /index.html, add it as /.
                if file == "index.html":
                    file = ""

                # Meets RFC 3986
                # https://tools.ietf.org/html/rfc3986#section-3.3
                if not re.match(r"^[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=]*$", file):
                    if not self.quiet:
                        print(f"Skipping {file} because it does not meet RFC 3986")
                    continue

                # File is all good.
                relative_path = os.path.relpath(os.path.join(root, file), self.root)

                # Check that said file exists in live if on.
                if self.checkOnline:
                    url = f"https://{self.domain}{relative_path}"
                    print(f"Checking {url}")
                    response = requests.head(url)
                    if response.status_code != 200:
                        if not self.quiet:
                            print(
                                f"Skipping {file} because it does not exist on the domain"
                            )
                        continue

                # Add the files last mod to the lastmod map
                last_modified = datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(root, file)), tz=timezone.utc
                )
                date = last_modified.isoformat()

                self.lastMod[self.fixPaths(relative_path)] = date

                self.files.append(relative_path)

        if not self.quiet:
            print(f"Found {len(self.files)} files")
        return self.files

    def loadBlacklist(self) -> dict[str, list[str]]:
        """
        Loads the blacklist from the 'blackList.json' file.

        Returns:
            list: The loaded blacklist.
        """
        with open("blackList.json", "r") as file:
            blackList = json.load(file)
        return blackList

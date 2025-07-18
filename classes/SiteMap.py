import heapq
import datetime


class SiteMap:
    def __init__(
        self, domain: str, output: str, paths: list[str], lastMod: dict
    ) -> None:
        """
        Initialize a SiteMap object.

        Args:
            domain (str): The domain of the website.
            output (str): The output file path for the generated sitemap.
            paths (list[str]): A list of paths to include in the sitemap.
            lastMod (dict): A dictionary mapping paths to their last modification dates.

        Returns:
            None
        """
        self.siteMapHeap = []
        heapq.heapify(self.siteMapHeap)
        self.output = output
        self.domain = domain
        self.paths = paths
        self.lastMod = lastMod
        self.fixPaths()

    def fixDomain(self) -> None:
        """
        Adds a trailing slash to the domain if it doesn't already have one.

        This method ensures that the domain has a trailing slash, which is required for generating a valid sitemap.

        Returns:
            None
        """
        if not self.domain.endswith("/"):
            self.domain += "/"

    def addPath(self, path: str, priority: float) -> None:
        """
        Add a path to the sitemap heap with the given priority.

        Args:
            path (str): The path to add.
            priority (float): The priority of the path.

        Returns:
            None
        """
        heapq.heappush(self.siteMapHeap, (priority, path))

    def buildSiteMapHeap(self) -> None:
        """
        Build the sitemap heap by adding paths from the `paths` list.

        Returns:
            None
        """
        for path in self.paths:
            self.addPath(path, self.getPriority(path))

    def fixPaths(self) -> None:
        """
        Fix the paths in the `paths` list by replacing "\\" with "/".

        Returns:
            None
        """
        for i in range(len(self.paths)):
            self.paths[i] = self.paths[i].replace("\\", "/")

    def getPriority(self, path: str) -> float:
        """
        Calculate the priority of a path based on its depth.

        Args:
            path (str): The path to calculate the priority for.

        Returns:
            float: The priority of the path.
        """
        depth = path.count("/")
        priority = round(0.8 / (depth + 1), 2)
        return priority

    def writeSiteMap(self) -> str:
        """
        Generate and write the sitemap XML to the output file.

        Returns:
            str: The generated sitemap XML.
        """
        sitemapEntires = []

        while self.siteMapHeap:
            priority, path = heapq.heappop(self.siteMapHeap)
            url = f"https://{self.domain}{path}"
            sitemapEntires.append(
                f"  <url>\n    <loc>{url}</loc>\n    <priority>{priority}</priority>\n    <lastmod>{self.lastMod.get(path)}</lastmod>\n  </url>"
            )

        sitemapEntires.append(
            f"  <url>\n    <loc>https://{self.domain}</loc>\n    <priority>1.0</priority>\n    <lastmod>{self.lastMod.get('.')}</lastmod>\n  </url>"
        )

        sitemap_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(sitemapEntires[::-1])
            + "\n</urlset>"
        )

        sitemap_xml += "\n<!-- Sitemap Generated by Local SiteMap Generator -->"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sitemap_xml += f"\n<!-- Sitemap Generated at {timestamp} -->"
        sitemap_xml += "\n<!-- Signed by Local SiteMap Generator (SH) -->"

        with open(self.output, "w") as f:
            f.write(sitemap_xml)

        return sitemap_xml

from classes.LocalCrawler import LocalCrawler
from classes.SiteMap import SiteMap
import os
import argparse

# User Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--domain", help="Domain for the sitemap", type=str, required=True)
parser.add_argument(
    "--path", help="Root directory for crawling", type=str, required=True
)
parser.add_argument(
    "--quiet",
    help="See live logging",
    action="store_true",
    default=False,
    required=False,
)
parser.add_argument(
    "--liveCheck",
    help="Only add paths that exist on that domain",
    action="store_true",
    required=False,
)
parser.add_argument(
    "--output",
    help="XML File output",
    type=str,
    default="./sitemap.xml",
    required=False,
)
args = parser.parse_args()

# Example usage:
# python generate.py --domain example.com --path /path/to/root --quiet=True --output ./output.xml

# Explanation:
# --domain: Specifies the domain for the sitemap (required)
# --path: Specifies the root directory for crawling (required)
# --quiet: Optional flag to enable live logging (default: False)
# --liveCheck: Optional flag to only add paths that exist on the specified domain (default: False)
# --output: Optional path to the XML file output (default: current directory)

# Note: Replace "example.com" with your desired domain and "/path/to/root" with the actual root directory path.

# Bring in the args
domain = args.domain
path = args.path
quiet = args.quiet
output = args.output
liveCheck = args.liveCheck

# Validate the path
if not os.path.exists(path):
    print(f"Path {path} does not exist")
    exit()

# Validate the output path
output_dir = os.path.dirname(output)
if not os.access(output_dir, os.W_OK):
    print(f"Cannot write to output directory {output_dir}")
    exit()

# Initialize the LocalCrawler
lc = LocalCrawler(root=path, quiet=quiet, domain=domain, checkOnline=liveCheck)

# Get the files
files = lc.crawl()

# Generate the XML based of the files
siteMap = SiteMap(domain, output, files, lc.lastMod)
siteMap.buildSiteMapHeap()
siteMap.writeSiteMap()
print(f"SiteMap generated at {output}")

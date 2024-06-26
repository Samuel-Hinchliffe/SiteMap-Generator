<div align="center">
  <a >
    <img src="git/logo.jpg" alt="Logo" width="150" height="150" style="border-radius: 100%">
  </a>

  <h3 align="center">🗺️ Static SiteMap Generator 🗺️</h3>

  <p align="center">
    🤖 Static/Local Sitemap Generation with Real-Time Validation
    <br><b>Static Sitemaps</b>
    <br />
    <a href="https://github.com//Samuel-Hinchliffe/StaticSiteMap"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</div>

# About

The Static SiteMap Generator is a straightforward Sitemap generator that allows you to create a sitemap for your website. It's not often that you will need to statically generate a sitemap based on local files, but when you do, this tool will suite that edge case perfectly.

The Static SiteMap Generator is a Python script that will generate a sitemap based on the files in a directory. With the ability to cross validate files against their online counterpart, so you can ensure that your sitemap is up to date.

- 🚀 **Simple**: Generate a sitemap.xml file with ease
- 📝 **Cross Validation**: Validate files against their online counterpart
- 📦 **Lightweight**: No need for any heavy installs

## 🏃‍♂️ Requirements

1. Python 3.6 or higher

## 💻 Usage

1. Install the required packages

```bash
pip install -r requirements.txt
```

2. Generate a sitemap.xml file

```bash
python generate.py --domain example.com --path /path/to/files
```

## ⭐ Important Notes

- By default, the script will generate a sitemap.xml based of specific file types. You can change this by modifying the `blacklist.json` file. For example by default, this will not include `.php` files in the sitemap.

## 🤖 Examples

```bash

# Generate a sitemap.xml file for https://www.google.com
python generate.py --domain 'www.google.com' --path './website/YOUR_FILES'

# Generate a sitemap.xml with real-time validation.
# Will check if the file exists on the live website too.
python generate.py --domain 'www.google.com' --path './website/YOUR_FILES' --liveCheck

# Quietly generate a sitemap.xml file for https://www.google.com
python generate.py --domain 'www.google.com' --path './website/YOUR_FILES' --quiet

# Generate a sitemap.xml file for https://www.google.com and output to a specific folder
python generate.py --domain 'www.google.com' --path './website/YOUR_FILES' --output './website/sitemap.xml'
```

## 🗺️ Sitemap Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
 <url>
    <loc>https://www.google.com/</loc>
    <priority>1.0</priority>
    <lastmod>2024-05-19T10:22:23.282862+00:00</lastmod>
  </url>
</urlset>
```

## ⭐ API Guide

### `--domain`

**REQUIRED**: The domain of the website you are generating the sitemap for. This will be used within the sitemap.xml as such `<loc>https://{{YOUR_DOMAIN}}/{{STATIC_FILES}}</loc>`

### `--path`

**REQUIRED**: This is the path to the files you want to generate the sitemap for. This can be a relative or absolute path.

### `--liveCheck`

This flag will enable real-time validation of the files against the live website. This will check if the file exists on the live website too. If the file does not exist, it will not be included in the sitemap and you will see this in the scripts output.

### `--quiet`

To run the script in quiet mode, you can use the `--quiet` flag. This will suppress all output from the script.

### `--output`

Specify the output file for the sitemap.xml. By default, this will be `sitemap.xml` in the root directory.

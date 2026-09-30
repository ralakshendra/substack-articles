from pathlib import Path
import re

DOCS_DIR = Path(__file__).parent
INDEX_FILE = DOCS_DIR / "index.md"


def get_title(md_file):
    """Get the first Markdown H1 title from the article."""

    text = md_file.read_text(encoding="utf-8")

    # Look for:
    # # Article Title

    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)

    if match:
        return match.group(1).strip()

    # If there is no H1, use the filename
    return md_file.stem.replace("-", " ").replace("_", " ").title()


articles = []

for md_file in DOCS_DIR.glob("*.md"):

    # Don't include index.md itself
    if md_file.name.lower() == "index.md":
        continue

    title = get_title(md_file)

    articles.append({
        "title": title,
        "filename": md_file.name
    })


# Sort alphabetically by title
articles.sort(key=lambda x: x["title"].lower())


# Build homepage
content = """# My Articles

Welcome to my article library.

## Articles

"""

for article in articles:
    content += f"- [{article['title']}]({article['filename']})\n"


INDEX_FILE.write_text(content, encoding="utf-8")

print(f"Created {INDEX_FILE}")
print(f"Found {len(articles)} articles.")

for article in articles:
    print(f"- {article['title']}")
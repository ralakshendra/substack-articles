from pathlib import Path
import re
from collections import defaultdict

DOCS_DIR = Path(__file__).parent
INDEX_FILE = DOCS_DIR / "index.md"


def get_title(md_file):
    text = md_file.read_text(encoding="utf-8")

    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)

    if match:
        return match.group(1).strip()

    return (
        md_file.stem
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )


articles = []

for md_file in DOCS_DIR.glob("*.md"):

    if md_file.name.lower() == "index.md":
        continue

    # Ignore helper scripts
    if md_file.name.lower() == "create_index.py":
        continue

    title = get_title(md_file)

    # Extract year from filename
    year_match = re.match(r"^(\d{4})-", md_file.name)

    if year_match:
        year = year_match.group(1)
    else:
        year = "Other"

    articles.append({
        "title": title,
        "filename": md_file.name,
        "year": year
    })


# Newest first
articles.sort(
    key=lambda x: (
        x["year"],
        x["filename"]
    ),
    reverse=True
)


# Group by year
by_year = defaultdict(list)

for article in articles:
    by_year[article["year"]].append(article)


# ==========================================
# HOMEPAGE
# ==========================================

content = """# Write With AI

<div class="hero">

<div class="hero-eyebrow">The Write With AI Archive</div>

# Write With AI

<div class="hero-description">
A searchable archive of ideas, frameworks, prompts and strategies for writing, AI, creators and the internet.
</div>

</div>

"""


# Stats

content += '<div class="stats">'

content += f"""
<div class="stat">
<div class="stat-number">{len(articles)}</div>
<div class="stat-label">Articles</div>
</div>
"""

for year in ["2026", "2025", "2024"]:

    if year in by_year:

        content += f"""
<div class="stat">
<div class="stat-number">{len(by_year[year])}</div>
<div class="stat-label">{year}</div>
</div>
"""


content += "</div>\n\n"


# ==========================================
# LATEST ARTICLES
# ==========================================

content += "## Latest Articles\n\n"

content += '<div class="article-grid">\n\n'


# Show latest 12

for article in articles[:12]:

    content += f"""
<a class="article-card" href="{article['filename']}">

<div class="article-year">
{article['year']}
</div>

<div class="article-title">
{article['title']}
</div>

<div class="read-more">
Read article →
</div>

</a>

"""

content += "</div>\n\n"


# ==========================================
# FULL ARCHIVE
# ==========================================

content += "## Explore the Archive\n\n"


for year in sorted(by_year.keys(), reverse=True):

    year_articles = by_year[year]

    content += f"""
<div class="archive-year">
{year}
</div>

<div class="archive-count">
{len(year_articles)} articles
</div>

"""

    content += '<div class="archive-list">\n\n'

    for article in year_articles:

        content += f"- [{article['title']}]({article['filename']})\n"

    content += "\n</div>\n\n"


INDEX_FILE.write_text(content, encoding="utf-8")

print(f"Created {INDEX_FILE}")
print(f"Found {len(articles)} articles.")

for year in sorted(by_year.keys(), reverse=True):
    print(f"{year}: {len(by_year[year])}")
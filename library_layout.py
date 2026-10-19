"""Resolve paper IDs to their classified directories without changing their identity."""
import csv
import json
import re
from pathlib import Path


def layout(root):
    source = Path(root) / 'classification_manifest.json'
    return json.loads(source.read_text()) if source.exists() else {'categories': [], 'papers': []}


def paper_dir(root, folder):
    records = {p['folder']: p for p in layout(root)['papers']}
    return Path(root) / records.get(folder, {}).get('directory_path', folder)


def rewrite_root_links(root, text):
    records = {p['folder']: p['directory_path'] for p in layout(root)['papers']}

    def replace(match):
        target = match.group(1)
        head, separator, tail = target.partition('/')
        return '](' + records.get(head, head) + separator + tail + ')'

    return re.sub(r'\]\(([^)]+)\)', replace, text)


def refresh_layout(root):
    """Normalize manifests, CSV, and root indices after an existing renderer runs."""
    root = Path(root)
    data = layout(root)
    records = {p['folder']: p for p in data['papers']}
    for name in ['papers_manifest.json', 'conference_2026_manifest.json']:
        path = root / name
        if not path.exists():
            continue
        manifest = json.loads(path.read_text())
        for paper in manifest['papers']:
            record = records.get(paper['folder'])
            if record is None:
                continue
            paper['directory_path'] = record['directory_path']
            paper['primary_category'] = record['primary_category']
            if paper.get('pdf_file'):
                paper['pdf_file'] = record['directory_path'] + '/' + Path(paper['pdf_file']).name
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    for path in root.glob('*.md'):
        text = rewrite_root_links(root, path.read_text())
        if path.name == 'README.md' and '[研究方向分类索引](CLASSIFICATION.md)' not in text:
            text = text.replace('\n', '\n\n按研究方向浏览：[研究方向分类索引](CLASSIFICATION.md)。\n', 1)
        path.write_text(text)
    source = root / 'papers.csv'
    if source.exists():
        with source.open(newline='') as stream:
            reader = csv.DictReader(stream)
            fields = list(reader.fieldnames)
            rows = list(reader)
        for field in ['directory_path', 'primary_category']:
            if field not in fields:
                fields.append(field)
        for row in rows:
            record = records.get(row['folder'])
            if record:
                row.update(directory_path=record['directory_path'], primary_category=record['primary_category'])
                if row.get('pdf_file'):
                    row['pdf_file'] = record['directory_path'] + '/' + Path(row['pdf_file']).name
        with source.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)


if __name__ == '__main__':
    refresh_layout(Path(__file__).resolve().parent)


import os
import glob
import re

def parse_extraction_files():
    files = glob.glob("/Users/goddaffi/Desktop/Final Year Projects/Maryam/Firduasi literature/*-Extraction.md")
    fact_sheet = []
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract Title
            title_match = re.search(r"### 1. Full Title of the Paper:\s*(.*)", content)
            title = title_match.group(1).strip() if title_match else "Unknown Title"
            
            # Extract Authors and Year
            author_match = re.search(r"### 2. Author\(s\) and Year of Publication:\s*(.*)", content)
            author_year = author_match.group(1).strip() if author_match else "Unknown Author (n.d.)"
            
            # Extract Methodology
            method_match = re.search(r"### 7. Methodology Used:\s*(.*)", content)
            methodology = method_match.group(1).strip() if method_match else "Not explicitly stated"
            
            # Extract Relevance
            relevance_match = re.search(r"### 11. Relevance to the Current Project:\s*(.*)", content)
            relevance = relevance_match.group(1).strip() if relevance_match else "N/A"
            
            fact_sheet.append({
                "file": os.path.basename(file_path),
                "title": title,
                "author_year": author_year,
                "methodology": methodology,
                "relevance": relevance
            })
            
    with open("firdausi_chapter_two_fact_sheet.txt", "w", encoding="utf-8") as out:
        for entry in fact_sheet:
            out.write(f"FILE: {entry['file']}\n")
            out.write(f"AUTHOR/YEAR: {entry['author_year']}\n")
            out.write(f"TITLE: {entry['title']}\n")
            out.write(f"METHOD: {entry['methodology']}\n")
            out.write(f"RELEVANCE: {entry['relevance']}\n")
            out.write("-" * 50 + "\n")

if __name__ == "__main__":
    parse_extraction_files()

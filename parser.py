import sys
import json
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from linkedin_parser.utils import clean_text, extract_dates

class ProfileParser:
    """Parses saved linkedin profile html."""
    def __init__(self, html_path):
        self.path = Path(html_path)
        self.soup = None

    def parse(self):
        if not self.path.exists():
            raise FileNotFoundError(f"missing {self.path}")
        
        self.soup = BeautifulSoup(self.path.read_text(encoding='utf-8'), 'lxml')
        
        name_elem = self.soup.find('h1', class_='text-heading-xlarge')
        name = clean_text(name_elem.text) if name_elem else ""
        
        title_elem = self.soup.find('div', class_='text-body-medium')
        title = clean_text(title_elem.text) if title_elem else ""
        
        experiences = []
        exp_section = self.soup.find('section', id='experience-section')
        if exp_section:
            items = exp_section.find_all('li', class_='artdeco-list__item')
            for item in items:
                role_elem = item.find('div', class_='display-flex')
                role_text = clean_text(role_elem.text) if role_elem else ""
                experiences.append({"role": role_text})

        # print(f"parsed {len(experiences)} exp items")
        return {
            "name": name,
            "title": title,
            "experiences": experiences
        }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--out', default=None)
    args = parser.parse_args()

    p = ProfileParser(args.path)
    try:
        res = p.parse()
    except Exception as e:
        print(f"error parsing: {e}")
        sys.exit(1)

    output = json.dumps(res, indent=2)
    if args.out:
        Path(args.out).write_text(output, encoding='utf-8')
    else:
        print(output)

if __name__ == '__main__':
    main()

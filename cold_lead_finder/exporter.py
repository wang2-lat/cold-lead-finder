import csv
from pathlib import Path
from typing import List, Dict

class CSVExporter:
    def export(self, leads: List[Dict], output_path: Path):
        """Export leads to CSV file."""
        
        fieldnames = ["platform", "author", "title", "url", "content", "pain_point", "email_template"]
        
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads)
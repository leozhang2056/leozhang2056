import json
import sys
from bs4 import BeautifulSoup

def main():
    path = r"C:\Users\MagicBook\.gemini\antigravity\brain\c363d6d4-ef10-4853-b258-e55876159d98\.system_generated\steps\24\content.md"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    
    out_lines = []
    
    # Let's search for json-ld
    found = False
    for script in soup.find_all("script"):
        if script.get("type") == "application/ld+json":
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    graphs = [data]
                elif isinstance(data, list):
                    graphs = data
                else:
                    graphs = []
                for graph in graphs:
                    if "@graph" in graph:
                        for item in graph["@graph"]:
                            if item.get("@type") == "JobPosting":
                                out_lines.append(f"TITLE: {item.get('title')}")
                                out_lines.append(f"COMPANY: {item.get('hiringOrganization', {}).get('name')}")
                                out_lines.append("DESCRIPTION:")
                                out_lines.append(BeautifulSoup(item.get("description", ""), "html.parser").get_text())
                                found = True
                                break
                    elif graph.get("@type") == "JobPosting":
                        out_lines.append(f"TITLE: {graph.get('title')}")
                        out_lines.append(f"COMPANY: {graph.get('hiringOrganization', {}).get('name')}")
                        out_lines.append("DESCRIPTION:")
                        out_lines.append(BeautifulSoup(graph.get("description", ""), "html.parser").get_text())
                        found = True
                        break
            except Exception as e:
                pass

    if not found:
        # Fallback: get text of elements with data-automation="jobDescription"
        desc_elem = soup.find(attrs={"data-automation": "jobDescription"})
        if desc_elem:
            out_lines.append("DESCRIPTION FROM data-automation:")
            out_lines.append(desc_elem.get_text(separator="\n"))
            found = True

    if not found:
        out_lines.append("FALLBACK: TEXT")
        text = soup.get_text()
        out_lines.extend([line.strip() for line in text.split("\n") if line.strip()][:300])

    out_text = "\n".join(out_lines)
    with open("scratch/parsed_jd.txt", "w", encoding="utf-8") as out_f:
        out_f.write(out_text)
    print("Successfully wrote parsed JD to scratch/parsed_jd.txt")

if __name__ == "__main__":
    main()

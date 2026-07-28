import difflib
import re

def normalize_content(content: str, attribute: str = "textcontent") -> str:
    if content is None:
        return ""
        
    # Standardize string representations
    val = str(content)
    
    # 1. Normalize line endings to \n
    val = val.replace("\r\n", "\n").replace("\r", "\n")
    
    # 2. Trim trailing space on each line
    lines = [line.strip() for line in val.splitlines()]
    normalized = "\n".join(lines)
    
    # 3. Normalize spaces and tabs
    normalized = re.sub(r"[ \t]+", " ", normalized)
    
    # 4. If comparison is on HTML elements, perform HTML tag cleaning
    attr_lower = str(attribute).lower()
    if attr_lower in {"html", "innerhtml", "outerhtml"}:
        # Strip HTML comments
        normalized = re.sub(r"<!--.*?-->", "", normalized, flags=re.DOTALL)
        # Convert all whitespace (including newlines) to a single space
        normalized = re.sub(r"\s+", " ", normalized)
        # Remove spaces immediately after/before tags to handle dynamic formatting
        normalized = re.sub(r">\s+", ">", normalized)
        normalized = re.sub(r"\s+<", "<", normalized)
        
    return normalized.strip()

def generate_diff(old_content: str, new_content: str) -> str:
    old_norm = normalize_content(old_content)
    new_norm = normalize_content(new_content)
    
    old_lines = old_norm.splitlines()
    new_lines = new_norm.splitlines()
    
    diff = list(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile="before",
        tofile="after",
        lineterm=""
    ))
    
    return "\n".join(diff)

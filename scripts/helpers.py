
import pycountry

def iso_country_name(code: str, lang: str = "en") -> str:
    try:
        country = pycountry.countries.get(alpha_2=code)
        return country.name if country else code
    except Exception:
        return code



def latex(cmd: str, *args) -> str:
    # Convert all args to strings, replace Undefined with empty string
    clean_args = [str(a) if a is not None else "" for a in args]
    joined = "}{".join(clean_args)
    return f"\\{cmd}{{{joined}}}"



def escape_latex(text: str) -> str:
    """Escape LaTeX special characters in text."""
    if not text:
        return ""
    escaped = str(text)
    # Order matters: backslash must be escaped first
    escaped = escaped.replace("\\", "\\textbackslash{}")
    escaped = escaped.replace("&", "\\&")
    escaped = escaped.replace("%", "\\%")
    escaped = escaped.replace("$", "\\$")
    escaped = escaped.replace("#", "\\#")
    escaped = escaped.replace("_", "\\_")
    escaped = escaped.replace("{", "\\{")
    escaped = escaped.replace("}", "\\}")
    escaped = escaped.replace("~", "\\textasciitilde{}")
    escaped = escaped.replace("^", "\\textasciicircum{}")
    return escaped


def join_array(sep: str, items):
    """Join array items with separator, escaping LaTeX special characters."""
    if not items:
        return ""
    escaped_items = [escape_latex(str(item)) for item in items]
    return sep.join(escaped_items)


def format_phone(phone: str) -> str:
    return phone


def format_month(lang: str, date: str) -> str:
    """Convert YYYY-MM or YYYY-MM-DD date format to readable month year.
    
    Args:
        lang: Language code (e.g., 'en', 'es')
        date: Date string in YYYY-MM or YYYY-MM-DD format
    
    Returns:
        Formatted date string (e.g., 'Nov 2023' for English)
    """
    if not date or date == "present":
        return "Present"
    
    months_en = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
    }
    months_es = {
        "01": "Ene", "02": "Feb", "03": "Mar", "04": "Abr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Ago",
        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dic"
    }
    
    months = months_en if lang == "en" else months_es
    
    try:
        # Extract YYYY-MM from YYYY-MM or YYYY-MM-DD
        parts = date.split("-")
        if len(parts) >= 2:
            year = parts[0]
            month = parts[1]
            return f"{months.get(month, month)} {year}"
        return date
    except Exception:
        return date


def cite(pub: dict) -> str:
    return pub.get("name", "")

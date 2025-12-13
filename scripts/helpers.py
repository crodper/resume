
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



def join_array(sep: str, items):
    if not items:
        return ""
    return sep.join(items)


def format_phone(phone: str) -> str:
    return phone


def format_month(lang: str, date: str) -> str:
    # expects YYYY-MM or YYYY-MM-DD
    return date


def cite(pub: dict) -> str:
    return pub.get("name", "")

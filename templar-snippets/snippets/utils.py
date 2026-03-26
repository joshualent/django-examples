import markdown
import nh3

ALLOWED_TAGS = nh3.ALLOWED_TAGS | {
    # Structure
    "p",
    "pre",
    "code",
    "blockquote",
    "hr",
    "br",
    # Headings
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    # Lists
    "ul",
    "ol",
    "li",
    # Inline
    "strong",
    "em",
    "del",
    "a",
    "img",
    # Tables
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    # Pygments needs these
    "span",
    "div",
}

ALLOWED_ATTRIBUTES = {
    # Pygments emits class attributes for syntax highlighting
    "*": {"class"},
    "a": {"href", "title"},
    "img": {"src", "alt", "title"},
    "td": {"align"},
    "th": {"align"},
}


def render_markdown(content: str) -> str:
    # 1. Convert markdown to HTML
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "nl2br",
        ]
    )
    raw_html = md.convert(content)

    # 2. Sanitize, preserving Pygments class attributes
    clean_html = nh3.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
    )

    return clean_html

import re
import random
from xml.sax.saxutils import escape as xml_escape

DEFAULT_COLORS = [
    "#1abc9c", "#16a085", "#f1c40f", "#f39c12", "#2ecc71", "#27ae60",
    "#e67e22", "#d35400", "#3498db", "#2980b9", "#e74c3c", "#c0392b",
    "#9b59b6", "#8e44ad", "#bdc3c7", "#34495e", "#2c3e50", "#95a5a6",
    "#7f8c8d", "#ec87bf", "#d870ad", "#f69785", "#9ba37e", "#b49255",
    "#b49255", "#a94136",
]

INITIALS_SVG_TEMPLATE = """
    <svg xmlns="http://www.w3.org/2000/svg"
        pointer-events="none"
        width="200" height="200">
      <defs>
        <linearGradient id="grad">
        <stop offset="0%" stop-color="{color1}" />
        <stop offset="100%" stop-color="{color2}" />
        </linearGradient>
      </defs>
      <rect width="200" height="200" rx="0" ry="0" fill="url(#grad)"></rect>
      <text text-anchor="middle" y="50%" x="50%" dy="0.35em"
            pointer-events="auto" fill="{text_color}" font-family="sans-serif"
            style="font-weight: 400; font-size: 80px">{text}</text>
    </svg>
    """.strip()

INITIALS_SVG_TEMPLATE = re.sub('(\s+|\n)', ' ', INITIALS_SVG_TEMPLATE)

def get_svg_avatar(initials):
    svg_avatar = INITIALS_SVG_TEMPLATE.format(**{
        'color1': random.choice(DEFAULT_COLORS),
        'color2': random.choice(DEFAULT_COLORS),
        'text_color': random.choice(DEFAULT_COLORS),
        'text': xml_escape(initials),
    }).replace('\n', '')

    return svg_avatar

import re

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

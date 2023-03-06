# This template tag is needed for production
# Add it to one of your django apps (/appdir/templatetags/render_vite_bundle.py, for example)

import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_vite_bundle():
    """
    Template tag to render a vite bundle.
    Supposed to only be used in production.
    For development, see other files.
    """

    fd = open(f"{settings.VITE_APP_DIR}/dist/manifest.json", "r")
    manifest = json.load(fd)

    imports_files = "".join(
        [
            f'<script type="module" src="/static/dist/{manifest[file]["file"]}"></script>'
            for file in manifest["src/main.js"]["dynamicImports"]
        ]
    )

    return mark_safe(
        f"""<script type="module" src="/static/dist/{manifest['src/main.js']['file']}"></script>
        <link rel="stylesheet" type="text/css" href="/static/dist/{manifest['src/main.js']['css'][0]}" />
        {imports_files}"""
    )

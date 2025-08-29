from jinja2 import Environment, BaseLoader
import tempfile
import os
from weasyprint import HTML


class GenerateRepportService:
    def __init__(self, plots):
        self.plots = plots

    def generate_repport(self, output_path=None, extra_data=None, cleanup_plots=False):
        if output_path is None:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            output_path = tmp.name
            tmp.close()
        else:
             if not os.path.exists('/ClusterApp/api/static/downloads'):
                os.makedirs('/ClusterApp/api/static/downloads', exist_ok=True)
        saved_path = self._generate_pdf(output_path, extra_data)

        if cleanup_plots:
            for path in set(self.plots.values()):
                try:
                    if path and os.path.isfile(path):
                        os.remove(path)
                except FileNotFoundError:
                    raise FileNotFoundError("File not found")

        return saved_path


    def _mount_html(self):
        result = []

        for plot_name in self.plots.keys():
            block = f"""
                <div class="plot">
                    <img src="{self.plots[plot_name]}" alt="{plot_name}" style="max-width:100%;height:auto;">
                </div>
                <div class="page-break"></div>
            """
            result.append(block)
        return result

    def _render_with_jinja(self, rendered_html, data=None):
        template = Environment(loader=BaseLoader).from_string(rendered_html)
        return template.render(**(data or {}))

    def _generate_combined_html(self, extra_data=None):
        parts = self._mount_html()
        rendered_parts = []
        for part in parts:
            rendered = self._render_with_jinja(part, extra_data)
            rendered_parts.append(rendered)

        body_parts = []
        for part in rendered_parts:
            body_parts.append(part)

        combined = f"""<!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>Combined Report</title>
            <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .page-break {{ page-break-after: always; }}
            img {{ max-width:100%; height:auto; }}
            </style>
            </head>
            <body>
            <h1>Report with PCoA 2D</h1>
            {''.join(body_parts)}
            </body>
            </html>
        """
        return combined

    def _generate_pdf(self, output_path, extra_data=None):
        html_string = self._generate_combined_html(extra_data)
        HTML(string=html_string,base_url=".").write_pdf(output_path)


        return os.path.abspath(output_path)
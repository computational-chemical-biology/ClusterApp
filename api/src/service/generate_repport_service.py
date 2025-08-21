from jinja2 import Environment, FileSystemLoader, BaseLoader
import tempfile
import os
from weasyprint import HTML


class GenerateRepportService:
    def __init__(self, plots):
        self.plots = plots

    def generate_repport(self, output_path=None, extra_data=None):
        if output_path is None:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            output_path = tmp.name
            tmp.close()

        saved_path = self._generate_pdf(output_path, extra_data)
        return saved_path


    def _mount_html(self):
        result = []
    
        for plot_name in self.plots.keys():
            jinja_template_string = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Report with Plot</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        .plot {{ text-align: center; margin-bottom: 20px; }}
                        .page-break {{ page-break-after: always; }}
                    </style>
                </head>
                <body>
                    <h1>Report with PCoA 2D</h1>
                    <p>{{{{ introduction_text }}}}</p>
                    <div class="plot">
                        <img src="{{{{ plot_image_path }}}}" alt="pcoa2d" style="max-width:100%;height:auto;">
                    </div>
                    <p>{{{{ conclusion_text }}}}</p>
                    <div class="page-break"></div>
                </body>
                </html>
            """
            env = Environment()

            template_data = {
                "introduction_text": "PCoA color coded with first metadata column.",
                "conclusion_text": "Example PCoA report.",
                "debug": self.plots,
                "plot_image_path": self.plots[plot_name]
            }

            template = env.from_string(jinja_template_string)

            rendered_html = template.render(template_data)
            result.append(rendered_html)
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
            start = part.find("<body")
            if start != -1:
                start = part.find(">", start) + 1
                end = part.rfind("</body>")
                body_content = part[start:end]
                body_parts.append(body_content)
            else:
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
            {''.join(body_parts)}
            </body>
            </html>
        """
        return combined

    def _generate_pdf(self, output_path, extra_data=None):
        html_string = self._generate_combined_html(extra_data)
        HTML(string=html_string,base_url=".").write_pdf(output_path)


        return os.path.abspath(output_path)
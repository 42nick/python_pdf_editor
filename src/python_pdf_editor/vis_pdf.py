import base64
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pdf2image import convert_from_bytes
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-pdf",
            children=html.Div(["Drag and Drop or ", html.A("Select PDF Files")]),
            style={
                "width": "50%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.Div(id="output-container"),
    ]
)


@app.callback(Output("output-container", "children"), Input("upload-pdf", "contents"), State("upload-pdf", "filename"))
def render_pdf_contents(contents, filename):
    if contents is not None:
        children = []
        for content, name in zip(contents, filename):
            pdf = PdfReader(io.BytesIO(base64.b64decode(content.split(",")[1])))
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                writer = PdfWriter()
                writer.add_page(page)
                stream = io.BytesIO()
                writer.write(stream)
                image = convert_from_bytes(stream.getvalue(), fmt="jpeg")[0]
                image_bytes = io.BytesIO()
                image.save(image_bytes, format="JPEG")
                image_data = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
                children.append(
                    html.Div(
                        [
                            html.H3(f"{name} - Page {i+1}"),
                            html.Img(src=f"data:image/jpeg;base64,{image_data}", style={"maxWidth": "15%"}),
                        ]
                    )
                )
        return children
    else:
        return html.Div("Upload a PDF file to visualize its pages.")


if __name__ == "__main__":
    app.run_server(debug=True)

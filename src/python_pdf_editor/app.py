import base64
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

UPLOAD_DIRECTORY = Path("/home/hahn/dev_repos/python_pdf_editor/src/python_pdf_editor/assets/uploads")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-image",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        # html.Iframe(id="test", src="/home/hahn/dev_repos/python_pdf_editor/data/test.pdf"),
        html.Div(id="output-image-upload"),
        html.Button("Download PDF", id="btn_image"),
        dcc.Download(id="download-image"),
        dcc.Store(id="store", storage_type="session"),
    ]
)


@app.callback(
    Output("download-image", "data"),
    Input("btn_image", "n_clicks"),
    State("store", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, data):
    return dcc.send_file(data["pdf_path"])


def parse_contents(contents, filename):
    return html.Div(
        [
            html.H5(filename),
            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Div("Raw Content"),
            html.Pre(contents[0:200] + "...", style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"}),
            html.Iframe(id="embedded-pdf", src="assets/uploads/" + filename),
        ]
    )


@app.callback(
    Output("output-image-upload", "children"),
    Output("store", "data"),
    Input("upload-image", "contents"),
    State("upload-image", "filename"),
    State("upload-image", "last_modified"),
    State("store", "data"),
    Input("store", "modified_timestamp"),
)
def update_output(list_of_contents, list_of_names, list_of_dates, storage_data, ts):
    if list_of_contents is not None:
        for content, name, date in zip(list_of_contents, list_of_names, list_of_dates):
            data = content.encode("utf8").split(b";base64,")[1]
            pdf_path = UPLOAD_DIRECTORY.joinpath(name)
            with open(pdf_path.as_posix(), "wb") as fp:
                fp.write(base64.decodebytes(data))

            if storage_data is None:
                storage_data = {}
            storage_data["pdf_path"] = pdf_path.as_posix()

            return parse_contents(content, name), storage_data
    return None, None


if __name__ == "__main__":
    app.run_server(debug=True)

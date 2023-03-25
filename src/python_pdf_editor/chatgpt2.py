import base64
import io
import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import PyPDF2
from dash.dependencies import Input, Output, State

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Define the app layout
app.layout = dbc.Container(
    [
        html.H1("PDF Encryption", className="text-center mt-3 mb-5"),
        dcc.Upload(
            id="upload-data",
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
            multiple=True,
        ),
        html.Div(id="upload-message", className="mt-3"),
        dbc.Input(id="password-input", type="password", placeholder="Enter password"),
        dbc.Button("Encrypt PDF", id="encrypt-button", n_clicks=0, color="primary", className="mt-3 mb-3"),
        html.Div(id="encryption-message"),
        html.Div(id="download-section"),
        html.Div(
            html.A(
                "Download Encrypted PDF",
                id="download-link",
                # download=encrypted_file,
                # href=f"/download/{encrypted_file}",
                className="btn btn-primary mt-3",
                hidden=True,
            ),
            className="text-center",
        ),
    ]
)


# Define the function to encrypt the PDF
def encrypt_pdf(input_file, password):
    output_file = os.path.splitext(input_file)[0] + "_encrypted.pdf"
    pdf_reader = PyPDF2.PdfReader(input_file)
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])
    pdf_writer.encrypt(password)
    with open(output_file, "wb") as f:
        pdf_writer.write(f)
    return output_file


# Define the function to convert the file to base64 encoding
def get_base64_encoded(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


# Define the callback to handle file upload and encryption
@app.callback(Output("upload-message", "children"), Input("upload-data", "filename"))
def update_upload_message(filename):
    if filename:
        return html.Div(f'File "{filename[0]}" uploaded successfully.', className="text-success")
    else:
        return html.Div("Please upload a file.", className="text-muted")


@app.callback(
    Output("encryption-message", "children"),
    Output("download-link", "download"),
    Output("download-link", "hidden"),
    Input("encrypt-button", "n_clicks"),
    State("upload-data", "filename"),
    State("upload-data", "contents"),
    State("password-input", "value"),
)
def encrypt_pdf_callback(n_clicks, filenames, file_contents, password):
    if n_clicks == 0:
        return "", None, True
    if not filenames or not file_contents:
        return html.Div("Please upload a file first.", className="text-danger"), None, True
    if not password:
        return html.Div("Please enter a password.", className="text-danger"), None, True
    filename = filenames[0]
    content_type, content_string = file_contents[0].split(",")
    decoded = base64.b64decode(content_string)
    with open(filename, "wb") as f:
        f.write(decoded)
    encrypted_file = encrypt_pdf(filename, password)
    os.remove(filename)
    return html.Div("You got everything right.", className="text-center"), encrypted_file, False


# Define the callback to update the download link
@app.callback(Output("download-link", "href"), Input("encrypt-button", "n_clicks"), State("upload-data", "filename"))
def update_download_link(n_clicks, filenames):
    if n_clicks == 0:
        return ""
    if not filenames:
        return ""
    filename = os.path.splitext(filenames[0])[0] + "_encrypted.pdf"
    return f"/download/{filename}"


from flask import Response


# Define the route to download the encrypted PDF file
@app.server.route("/download/<filename>")
def download_file(filename):
    encrypted_file = os.path.join(os.getcwd(), filename)
    with open(encrypted_file, "rb") as f:
        encrypted_content = f.read()
    os.remove(encrypted_file)
    response = Response()
    response.headers.set("Content-Disposition", "attachment", filename=filename)
    response.headers.set("Content-Type", "application/pdf")
    response.data = encrypted_content
    return response


if __name__ == "__main__":
    app.run_server(debug=True)

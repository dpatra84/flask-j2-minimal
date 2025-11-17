from app import app
from flask_login import login_required
from flask import render_template, request, redirect
from app.forms.llm import ChatForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from app.services.fileparser_service import pdf_to_txt


@app.route("/members")
@login_required
def members_page():
    """Render a page accessible only to logged-in users."""
    # The 'name' in the User model is now accessible via current_user

    form = ChatForm()
    return render_template("user/members_page.j2", form=form)


@app.route("/upload", methods=["POST"])
@login_required
def llm_upload():
    """Upload a file to the server."""
    if request.method == "POST":
        if request.files:
            files = request.files.getlist("files[]")
            files_data = []
            for file in files:
                files_data.append({})
                filename = secure_filename(file.filename)
                new_filename = str(int(datetime.now().timestamp())) + "_" + filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], new_filename))
                print("File saved as {}".format(new_filename))
                files_data[-1]["name"] = new_filename
                files_data[-1]["type"] = file.content_type
                files_data[-1]["size"] = file.content_length
                if str(file.content_type).find("pdf") == 1:
                    files_data[-1]["content"] = pdf_to_txt(
                        os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
                    )

            return {
                "status": 200,
                "message": "File uploaded successfully",
                "data": {"files": files_data},
            }

        else:
            return {"status": 400, "message": "No files", "data": {}}

    return {"status": 405, "message": "Method not allowed", "data": {}}

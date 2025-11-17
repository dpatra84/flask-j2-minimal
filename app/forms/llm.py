from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField
from markupsafe import Markup

class ChatForm(FlaskForm):
    message = StringField("Message", validators=[])
    files = MultipleFileField("File", name="files", id="files")
    submit = SubmitField("Submit")

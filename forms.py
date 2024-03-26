from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length

class AddPetForm(FlaskForm):
    """Form for adding Pets"""
    name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Species",
                          choices=[("cat", "Cat"), ("dog","Dog"), ("porcupine","Porcupine")]
                          )
    img_url = StringField("Pet Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Pet Age", validators=[Optional(), NumberRange(min=0,max=30)])
    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])
    available = BooleanField("Is Pet Available?")
    
class EditPetForm(FlaskForm):
    """Form for editing pets"""
    img_url = StringField("Pet Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])
    available = BooleanField("Is Pet Available?")
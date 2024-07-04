from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

class EntryForm(FlaskForm):
    date = DateField('日期', default=datetime.today, format='%Y-%m-%d', validators=[DataRequired()])
    sales = DecimalField('当天销售额', validators=[DataRequired()])
    submit = SubmitField('提交')


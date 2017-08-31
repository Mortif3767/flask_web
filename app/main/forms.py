# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length

class EditProfileForm(FlaskForm):
    name = StringField(u'姓名',validators=[Length(0,64)])
    location = StringField(u'位置',validators=[Length(0,64)])
    about_me = TextAreaField(u'个性签名')
    submit = SubmitField(u'提交')
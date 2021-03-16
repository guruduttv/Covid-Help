from django import forms
from django import forms
from django.core import validators
symptoms= [(' ',' '),
    ('None of these','None of these'),
    ('Bluish lips or face', 'Bluish lips or face'),
    ('Severe and constant pain or pressure in the chest', 'Severe and constant pain or pressure in the chest'),
    ('Extreme difficulty breathing', 'Extreme difficulty breathing'),
    ('Unconscious or very difficult to wake up', 'Unconscious or very difficult to wake up'),
    ('Signs of low blood pressure','Signs of low blood pressure'),
    ('Dehydration (dry lips and mouth, sunken eyes)','Dehydration (dry lips and mouth, sunken eyes)'),
    ('More than one of above symptoms','More than one of above symptoms'),
    ]
disease=[(' ',''),('None of these','None of these'),('Diabetes','Diabetes'),('Hypertension','Hypertension'),('Lung Disease','Lung Disease'),('Heart Disease','Heart Disease'),
         ('Kidney Disorder','Kidney Disorder'), ('More than one of above mentioned diseases','More than one of above mentioned diseases'),]
travelled=[('No','No'),('Yes','Yes')]
applies=[(' ',''),('None of these','None of these'),('I have recently interacted or lived with someone who has tested positive for COVID -19','I have recently interacted or lived with someone who has tested positive for COVID -19 '),('I am a healthcare worker and I examined a COVID-19 confirmed case without protective gear',
'I am a healthcare worker and I examined a COVID-19 confirmed case without protective gear')]
class selfassessment(forms.Form):

    phno = forms.CharField(max_length=10,required=True)
    # email = forms.EmailField(required=False)
    age= forms.IntegerField(required = True)
    sym= forms.CharField(required = True,label='Do you have any of following symptoms?', widget=forms.Select(choices=symptoms))
    dis= forms.CharField(required = True,label='Have  you ever had any of the following ?', widget=forms.Select(choices=disease))
    travel= forms.CharField(required = True,label='Have you traveled anywhere internationally in the last 28 - 45 days?', widget=forms.Select (choices=travelled))
    apply= forms.CharField(required = True,label='Which of the following apply to you  ?', widget=forms.Select(choices=applies))
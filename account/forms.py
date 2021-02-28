from django import forms

class AcceptForm(forms.Form):
    """ Форма для принятия заявки """
    comment= forms.CharField(widget=forms.Textarea, label=u'Комментарий')
    reviewer_corrected_manuscript = forms.FileField(label="Расмотренная статья в .doc")
    reviewer_corrected_manuscript_pdf = forms.FileField(label="Расмотренная статья в .pdf")

class RejectForm(forms.Form):
    """ Форма для отклонения заявки """
    comment= forms.CharField(widget=forms.Textarea(attrs={'rows':20, 'cols':15}), label=u'Комментарий')


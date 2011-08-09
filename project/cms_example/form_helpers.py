from django.core.urlresolvers import reverse
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import Layout, Fieldset, Row, HTML

commentform_helper = FormHelper()
"""
# create the layout object
commentform_layout = Layout(
    # first fieldset shows the company
    Fieldset('', 'is_company'),

    # second fieldset shows the contact info
    Fieldset('Contact details',
        HTML(style),
        'email',
        Row('password1','password2'),
        'first_name',
        'last_name',
    )
)

commentform_helper.add_layout(commentform_layout)
"""
commentform_helper.form_action = reverse('comments-post-comment')
commentform_helper.form_method = 'POST'
commentform_helper.add_input(Submit('post','Post'))
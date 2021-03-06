from django.core.urlresolvers import reverse
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import Layout, Fieldset, Row, HTML

comment_form_helper = FormHelper()

comment_form_layout = Layout(
    Fieldset('',
        'parent',
        'content_type',
        'security_hash',
        'title',
        'name',
        'email',
        'url',
        'comment',
        'honeypot'
    )
)

comment_form_helper.add_layout(comment_form_layout)

comment_form_helper.form_action = reverse('comments-post-comment')
comment_form_helper.form_method = 'POST'
comment_form_helper.add_input(Submit('post','Post'))
comment_form_helper.add_input(Submit('preview','Preview'))

search_form_helper = FormHelper()

search_form_layout = Layout(
    Fieldset('',
        'q',
        'models'
    )
)

search_form_helper.add_layout(search_form_layout)
search_form_helper.form_style = 'inline'
search_form_helper.form_method = 'GET'
search_form_helper.add_input(Submit('post','Search'))


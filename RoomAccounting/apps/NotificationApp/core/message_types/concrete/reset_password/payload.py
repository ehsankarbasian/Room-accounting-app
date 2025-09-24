from ....payloads.interface import PayloadInterface
from django.template.loader import render_to_string


class ResetPasswordPayload(PayloadInterface):
    
    @staticmethod
    def build(context):
        token = context['token']
        final_text = f'Your reset password text is: "{token}"'
        print(final_text)

        email = context['identifier']
        context = {
            'email': email,
            'name': "__TODO__",
            'token': token}
        html_content = get_template('AuthApp/reset_password.html').render(context=context)
        send_html_email(subject='reset password',
                message='message',
                to_list=[],
                html_content=html_content)

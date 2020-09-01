from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's email field and some user state that's sure to change
        after a password reset to produce a token that invalidated when it's
        used. Note that user's primary key is not available yet since "user" is
        only an instance not an actual database object.
        The hased fields are:
        1. Email field
        2. The last_login field will usually be updated in the activation view
        Failing those things, settings.PASSWORD_RESET_TIMEOUT eventually
        invalidates the token.
        Running this data through salted_hmac() prevents password cracking
        attempts using the reset token, provided the secret isn't compromised.
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        """
        login_timestamp = '' if user.last_login is None else user.last_login.replace(
            microsecond=0, tzinfo=None)
        return str(user.email) + str(login_timestamp) + str(timestamp)

account_activation_token_generator = AccountActivationTokenGenerator()
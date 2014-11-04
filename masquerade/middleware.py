from masquerade.users import UserModel

class MasqueradeMiddleware(object):
    def process_request(self, request):
        """Checks for the presence of "mask_user" in the session. The value
        should be the username of the user to be masqueraded as. Note we
        also set the "is_masked" attribute to true in that case so that when we
        hit the "mask" or "unmask" URLs this user is properly recognized,
        rather than the user they're masquerading as :) """

        request.user.is_masked = False
        request.user.original_user = None

        if 'mask_user' in request.session:
            User = UserModel()
            try:
                original_user = request.user
                request.user = \
                  User.objects.get(username=request.session['mask_user'])
                request.user.is_masked = True
                request.user.original_user = original_user
            except User.DoesNotExist:
                pass

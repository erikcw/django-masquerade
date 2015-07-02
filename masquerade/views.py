from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from masquerade.forms import MaskForm
from masquerade.signals import mask_on, mask_off

try:
    from django.forms.utils import ErrorList
except ImportError:
    from django.forms.util import ErrorList # compatibility with < Django 1.7

MASQUERADE_REDIRECT_URL = getattr(settings, 'MASQUERADE_REDIRECT_URL', '/')

MASQUERADE_REQUIRE_SUPERUSER = getattr(settings,
  'MASQUERADE_REQUIRE_SUPERUSER', False)

MASQUERADE_REQUIRE_COMMON_GROUP = getattr(settings,
  'MASQUERADE_REQUIRE_COMMON_GROUP', False)

def mask(request, template_name='masquerade/mask_form.html'):
    if not request.user.is_masked and not request.user.is_staff:
        return HttpResponseForbidden()
    elif not request.user.is_superuser and MASQUERADE_REQUIRE_SUPERUSER:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = MaskForm(request.POST)
        form.full_clean()

        if MASQUERADE_REQUIRE_COMMON_GROUP and form.is_valid():
            user_groups = request.user.groups.all()
            mask_groups = form.user.groups.all()
            
            # If the user is not super, and there are no common groups, 
            # then deny access.
            if (
                not request.user.is_superuser and 
                not any(x in mask_groups for x in user_groups)
            ):
                form._errors[forms.forms.NON_FIELD_ERRORS] = (
                    ErrorList([u"You may not access that username"])
                )
                
        if form.is_valid():
            # turn on masquerading
            request.session['mask_user'] = form.cleaned_data['mask_user']
            mask_on.send(sender=form,
                mask_username=form.cleaned_data['mask_user'])
            return HttpResponseRedirect(MASQUERADE_REDIRECT_URL)
    else:
        form = MaskForm()

    return render_to_response(template_name, {'form': form},
      context_instance=RequestContext(request))

def unmask(request):
    # Turn off masquerading. Don't bother checking permissions.
    try:
        mask_username = request.session['mask_user']
        del(request.session['mask_user']) 
        mask_off.send(sender=object(), mask_username=mask_username)
    except KeyError:
        pass

    return HttpResponseRedirect(MASQUERADE_REDIRECT_URL)

from horizon import forms,exceptions,messages

from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.api.salt_api import grains_ls,match_by_grain


class EmptyClass():

    pass

class SelectGrain(forms.SelfHandlingForm):

    grain = forms.ChoiceField(label=_("Grain"),
                                          required=True)
    value = forms.CharField(label=_("Value"),
                           max_length=2048)


    

    def __init__(self, request, *args, **kwargs):

        super(SelectGrain, self).__init__(request, *args, **kwargs)

        try:
            grains = grains_ls()
        except Exception:
            grains = []
            exceptions.handle(request,
                              _('Unable to get grains list'))

        choices = [(grain, grain) for grain in grains]
        choices.sort()
        if not choices:
            choices.insert(0, ("", _("No grains found")))
        elif len(choices) > 1:
            choices.insert(0, ("", _("Any grain")))

        #
        self.fields['grain'].choices = choices




    def handle(self, request, data):

        instances_list = []
        try:
            # Remove any new lines in the public key
            grain=data['grain']
            value=data['value']
            instances_list = match_by_grain(grain=grain,value=value)
            messages.success(request,
                             _('Following instances match: %s')
                             % str(instances_list))

            info = EmptyClass()

            info.id = info.name = grain+':'+value

            info.value=str(instances_list)

            info.instances_list = instances_list
            
            return info

        except Exception:
            exceptions.handle(request, ignore=True)
            self.api_error(_('Salt api error :('))
            return False


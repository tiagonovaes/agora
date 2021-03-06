# -*- coding: utf-8 -*-
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User as UserSys
from .models import User, Termo
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import ldap



def term_required(function):
    #u = UserSys.objects.get(username=request.user)
    def wrap(request, *args, **kwargs):
        try:
            us = User.objects.get(user=request.user)
        except:
            u = UserSys.objects.get(username=request.user)
            l = ldap.initialize("ldaps://ldap1.unicamp.br/")
            baseDN = "ou=people,dc=unicamp,dc=br"
            searchScope = ldap.SCOPE_SUBTREE
            retrieveAttributes = None
            searchFilter = "uid=" + u.username
            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_type, result_data = l.result(ldap_result_id, 0)
            l.unbind_s()
            staffd = '8'

            try:
                pn = result_data[0][1]['givenName'][0]
            except:
                pn = 'none'

            try:
                un = result_data[0][1]['sn'][0]
            except:
                un = 'none'

            try:
                it = result_data[0][1]['ou'][0]
            except:
                it = 'none'

            try:
                uid = result_data[0][1]['uid'][0]
            except:
                uid = '00000'

            try:
                staff = result_data[0][1]['eduPersonAffiliation'][0]
            except:
                staff = '8'

            try:
                staff4 = result_data[0][1]['eduPersonAffiliation'][2]
            except:
                staff4 = 'none'

            try:
                staff2 = result_data[0][1]['eduPersonAffiliation'][1]
            except:
                staff2 = 'none'


            if staff == 'faculty':
                staffd = '1'
                email = uid + "@unicamp.br"

            if staff == 'staff':
                staffd = '2'
                email = uid + "@unicamp.br"

            if staff == 'student':
                first = pn[:1].lower()
                email = first + uid + "@dac.unicamp.br"
                if staff2 == 'POS-GRADUACAO':
                    staffd = '7'
                if staff2 == 'GRADUACAO':
                    staffd = '3'
                if staff2 == 'alumni':
                    if staff4 == 'none':
                        staffd = '8'
                    if staff4 == 'MESTRADO':
                        staffd = '4'
                    if staff4 == 'DOUTORADO':
                        staffd = '5'


            u = UserSys.objects.get(username=request.user)
            x = User(user=u, primeiro_nome=pn, ultimo_nome=un, institute=it, email=email, staff=staffd, projeto="default")
            x.save()
            us = User.objects.get(user=request.user)
        cond = Termo.objects.get(user=us)
        if cond.condition == 'Sim':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('agoraunicamp:termo'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

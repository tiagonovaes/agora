# -*- coding: utf-8 -*-
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User as UserSys
from .models import User, Termo
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import ldap



def term_required(function):
    l = ldap.initialize("ldaps://ldap1.unicamp.br/")
    baseDN = "ou=people,dc=unicamp,dc=br"
    searchScope = ldap.SCOPE_SUBTREE
    retrieveAttributes = None
    searchFilter = "uid=request.user"
    ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
    result_type, result_data = l.result(ldap_result_id, 0)
    l.unbind_s()

    result_data[0][1]['shadowFlag']
    result_data[0][1]['departmentNumber']

    def wrap(request, *args, **kwargs):
        try:
            us = User.objects.get(user=request.user)
        except:
            u = UserSys.objects.get(username=request.user)
            x = User(user=u, primeiro_nome=result_data[0][1]['shadowFlag'], ultimo_nome=result_data[0][1]['departmentNumber'], projeto="default")
            x.save()
            us = User.objects.get(user=request.user)
        cond = Termo.objects.get(user=us)
        print (cond.condition)
        if cond.condition == 'Sim':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('agoraunicamp:termo'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

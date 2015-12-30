from django.shortcuts import redirect
from django.core.urlresolvers import reverse

class UserMiddleware(object):

    def process_request(self, request):

        # Запрещаем удалённому пользователю что либо делать, кидая его на личную страницу и оставив возможность восстановления и выхода

        if (request.user.is_authenticated() and not request.user.is_active) and \
           ('HTTP_ACCEPT' in request.META and 'text/html' in request.META['HTTP_ACCEPT']) and \
           (reverse('user_detail', args=(request.user.id,)) != request.path) and \
           (request.path != reverse('user_delete')) and \
           (request.path != reverse('user_logout')):
            return redirect(reverse('user_detail', args=(request.user.id,)))

        # Запрещаем заблокированному пользователю что либо делать, кидая его на личную страницу и оставив возможность выхода

        if (request.user.is_authenticated() and not request.user.moderated) and \
           ('HTTP_ACCEPT' in request.META and 'text/html' in request.META['HTTP_ACCEPT']) and \
           (reverse('user_detail', args=(request.user.id,)) != request.path) and \
           (request.path != reverse('user_logout')):
            return redirect(reverse('user_detail', args=(request.user.id,)))

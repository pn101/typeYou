from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from users.models import BaseUser, Follow


class FollowCreateView(LoginRequiredMixin, CreateView):
    model = Follow
    fields = [
    ]

    def form_valid(self, form):
        follower = self.request.user
        following = BaseUser.objects.get(
                username=self.request.POST.get('username')
        )

        form.instance.follower = follower
        form.instance.following = following

        if not Follow.objects.filter(follower=follower, following=following).exists():
            messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    settings.FOLLOW_SUCCESS_MESSAGE,
            )
            return super(FollowCreateView, self).form_valid(form)
        messages.add_message(
                self.request,
                messages.SUCCESS,
                settings.ALREADY_FOLLOWING_ERROR_MESSAGE,
        )
        return redirect(reverse('users:teacherpage', kwargs={'slug': form.instance.following.username}))

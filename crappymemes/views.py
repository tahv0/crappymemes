from django.shortcuts import render, redirect,  reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Create your views here.
from social_django.models import UserSocialAuth
from crappymemes.forms import NewCrappyMemeForm, UpdateCrappyMemeForm, CommentForm
from crappymemes.models import Meme, Comment, CommentLike, MemeLike
from copy import deepcopy
from _datetime import datetime
import json
from django.views.generic import TemplateView
from django.http import JsonResponse


@login_required
def home(request):
    memes = Meme.objects.all()
    return render(request, 'index.html', {'memes': memes})


class NewMeme(TemplateView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = NewCrappyMemeForm()
        return render(request, 'core/meme.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = NewCrappyMemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme = form.save(commit=False)
            meme.author = request.user
            meme.save()
        else:
            form = NewCrappyMemeForm()
        return render(request, 'core/meme.html', {'form': form})


class EditMeme(TemplateView):
    @method_decorator(login_required)
    def get(self, request, meme_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id, author=request.user)
        form = UpdateCrappyMemeForm(instance=meme)
        return render(request, 'core/edit_meme.html', {'form': form, 'meme': meme})

    @method_decorator(login_required)
    def post(self, request, meme_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id, author=request.user)
        form = UpdateCrappyMemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme.author = request.user
            form_pic = form.cleaned_data.get('pic', None)
            form_title = form.cleaned_data['title']
            if  form_pic is not None and form_pic != meme.pic:
                meme.pic = form_pic
            meme.title = form_title
            meme.save()
        else:
            form = NewCrappyMemeForm(instance=meme)
        return render(request, 'core/edit_meme.html', {'form': form, 'meme': meme})


class DeleteMeme(TemplateView):
    @method_decorator(login_required)
    def post(self, request, meme_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id, author=request.user)
        meme.delete()
        return redirect(reverse('index'), request)


class ShowMeme(TemplateView):
    @method_decorator(login_required)
    def get(self, request, meme_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id)
        comment_form = CommentForm()
        comments = Comment.objects.filter(meme=meme, reply_to__isnull=True)
        return render(request, 'core/show_meme.html', {'meme': meme, 'comment_form': comment_form, 'comments': comments})


class MemeLikeChart(View):
    @method_decorator(login_required)
    def get(self, request, meme_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id)
        js_data = json.dumps(meme.get_likes_sum_by_month())
        return JsonResponse(js_data, safe=False)



class MemeCommentChart(View):
    @method_decorator(login_required)
    def get(self, request, meme_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id)
        js_data = json.dumps(meme.get_comments_sum_by_month())
        return JsonResponse(js_data, safe=False)


class AddComment(View):
    @method_decorator(login_required)
    def post(self, request, meme_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id, author=request.user)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.meme = meme
            comment.save()
        return redirect(reverse('show_meme', kwargs={'meme_id': meme.id}), request)


class LikeMeme(View):
    @method_decorator(login_required)
    def post(self, request, meme_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id)
        meme_like, created = MemeLike.objects.get_or_create(meme=meme, user=request.user)
        if not created:
            meme_like.delete()
        redirect_addr = request.META.get('HTTP_REFERER', 'index')
        return redirect(redirect_addr, request)


class ReplyComment(View):
    @method_decorator(login_required)
    def post(self, request, meme_id=None, comment_id=None, *args, **kwargs):
        meme = get_object_or_404(Meme, id=meme_id, author=request.user)
        try:
            old_comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            old_comment = None
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.meme = meme
            comment.reply_to = old_comment
            if old_comment is None or old_comment.meme == meme:
                comment.save()
        return redirect(reverse('show_meme', kwargs={'meme_id': meme.id}), request)


class DeleteComment(View):
    @method_decorator(login_required)
    def post(self, request, meme_id=None, comment_id=None, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.deleted = True
        comment.save()
        return redirect(reverse('show_meme', kwargs={'meme_id': meme_id}), request)



class LikeComment(View):
    @method_decorator(login_required)
    def post(self, request, comment_id=None, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        comment_like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            comment_like.delete()
        return redirect(reverse('show_meme', kwargs={'meme_id': comment.meme.id}), request)


@login_required
def settings(request):
    user = request.user
    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})



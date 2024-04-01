from django.shortcuts import render, redirect
# クラスベース汎用View
from django.views.generic import View
from .models import Post
from .forms import PostForm
# ログイン必須
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexView(View):
    def get(self, request , *args, **kwargs):
        # postモデルからデータを取得
        # -idで降順に並び替えてデータを取得
        post_data = Post.objects.order_by('-id')
        # index.htmlにデータを渡す
        # レンダリング
        return render(request, 'app/index.html',{
            # <h1>{{ post_data }}</h1>
            'post_data':post_data
        })

class PostDetailView(View):
    # get メソッドは、GETリクエストを受け取った時に呼び出されます。
    # このメソッドでは、Post モデルから、URLパラメータ pk で指定されたIDの投稿データを取得しています。
    def get(self, request , *args, **kwargs):
        # urlで指定されたidを指定して投稿データを取得
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_detail.html', {
            'post_data':post_data
        })

class CreatePostView(LoginRequiredMixin,View):
    # 最初にLoginRequiredMixinを継承
    def get(self, request , *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'app/post_form.html', {
            'form':form
        })
    
    # 投稿するボタンをクリックしたときの動作
    def post(self, request , *args, **kwargs):
        # forms.py
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            # 詳細画面に飛ばすため、pkが必須
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {
            'form':form
        })
    
    # LoginRequiredMixin: ログインしていないユーザーがこのビューにアクセスしようとすると、ログインページにリダイレクトされます。
    # PostForm: 新規投稿用のフォームクラスです。
    # form.is_valid(): フォームデータが有効かどうかをチェックします。
    # post_data = Post(): Post モデルの新しいインスタンスを作成します。
    # post_data.author = request.user: 現在のユーザーを投稿の作者として設定します。
    # post_data.title = form.changed_data['title']: フォームデータからタイトルを取得して設定します。
    # post_data.content = form.changed_data['content']: フォームデータから内容を取得して設定します。
    # post_data.save(): Post モデルのインスタンスを保存します。
    # redirect('post_detail', post_data.id): 投稿詳細ページにリダイレクトします。

class PostEditView(LoginRequiredMixin, View):
    def get(self, request , *args, **kwargs):
        # get関数はurlからidを取得してpost_dataを取得
        # models.py
        post_data = Post.objects.get(id=self.kwargs['pk'])
        # forms.pyをインスタンス化
        form = PostForm(
            request.POST or None,
            # フォームの初期値を設定
            initial = {
                'title': post_data.title,
                'content': post_data.content
            }
        )

        return render(request, 'app/post_form.html', {
            'form': form
        })
    
    def post(self, request , *args, **kwargs):
        # forms.py
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            post_data.save()
            # 詳細画面に飛ばすため、pkが必須
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {
            'form':form
        })

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request , *args, **kwargs):
        # urlで指定されたidを指定して投稿データを取得
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data':post_data
        })
    
    # submitで削除ボタンがクリックされたあとの動作
    def post(self, request , *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')

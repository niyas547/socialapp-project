from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.serializers import PostSerializer,UserSerializer,CommentSerializer
from api.models import Posts,Comments
from rest_framework import authentication,permissions
from rest_framework.decorators import action


# Create your views here.

class PostsView(ViewSet):
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes =[authentication.TokenAuthentication]
    permission_classes =[permissions.IsAuthenticated]
    def list(self,request,*args,**kwargs):
        qs=Posts.objects.all()
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kwargs):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id=id)
        serializer=PostSerializer(qs)
        return Response(data=serializer.data)
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id=id)
        serializer=PostSerializer(instance=qs,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:

            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id=id)
        qs.delete()
        return Response({"message":"post deleted"})


class UsersView(ViewSet):
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class PostModelView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    authentication_classes =[authentication.TokenAuthentication]
    permission_classes =[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):    #2
        user=request.user
        serializer=PostSerializer(data=request.data,context={"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)



    #methods added by the user
    @action(methods=["GET"],detail=False)
    def my_posts(self,request,*args,**kwargs):
        user=request.user
        qs=user.post.all()                         #if related name is used the add related name with user.related name.all() that means remove set
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)
        #localhost:8000/api/v2/posts/my_posts/

    @action(methods=["GET"],detail=True)
    def get_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        comments=post.comments_set.all()
        serializer=CommentSerializer(comments,many=True)
        return Response(data=serializer.data)
        #localhost:8000/api/v2/posts/2/get_comments/

    @action(methods=["POST"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        serializer=CommentSerializer(data=request.data,context={"user":request.user,"post":post})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

        # comment=request.data.get("comment")
        # post.comments_set.create(comment=comment,user=request.user)
        # return Response(data="ok")

# localhost:8000/api/v2/posts/{post id}/add_like
    @action(methods=["POST"],detail=True)
    def add_like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        user=request.user
        post.liked_by.add(user)
        return Response(data="ok")

# localhost:8000/api/v2/posts/{post id}/get_likes/
    @action(methods=["GET"],detail=True)
    def get_likes(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        cnt=post.liked_by.all().count()
        return Response(data=cnt)
        # liked_by=post.liked_by.all()
        # serializer=UserSerializer(liked_by,many=True)
        # return Response(data=serializer.data)


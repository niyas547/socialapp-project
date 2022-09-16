from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.serializers import PostSerializer,UserSerializer,CommentSerializer
from api.models import Posts
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
        qs=user.posts_set.all()
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"],detail=True)
    def get_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id=id)
        cmt=qs.comments_set.all()
        serializer=CommentSerializer(cmt,many=True)
        return Response(data=serializer.data)


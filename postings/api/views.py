# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from rest_framework import generics,mixins
#from django.contrib.contenttypes import generic
from django.db.models import Q
from .serializers import BlogPostSerializer
from postings.models import *
from postings.models import BlogPost
class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field      = 'pk'
    serializer_class  = BlogPostSerializer

    def get_queryset(self):
        return BlogPost.objects.all()



class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field      = 'pk'
    serializer_class  = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()
        return qs

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

    def post(self,request, *args, **kwargs):
        return self.create(request,*args,**kwargs)


    def put(self,request, *args, **kwargs):
        return self.update(request,*args,**kwargs)

    def patch(self,request, *args, **kwargs):
        return self.update(request,*args,**kwargs)

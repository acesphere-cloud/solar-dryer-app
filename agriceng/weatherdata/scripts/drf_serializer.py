from datetime import datetime

from rest_framework import serializers

def run(*args):
    class Comment:
        def __init__(self, email, content, created=None):
            self.email = email
            self.content = content
            self.created = created or datetime.now()

    comment1 = Comment(email='leila@example.com', content='foo bar')

    comment2 = Comment(email='miguna@nrm.co.ke', content='Viva Patriots')


    class CommentSerializer(serializers.Serializer):
        email = serializers.EmailField()
        content = serializers.CharField(max_length=200)
        created = serializers.DateTimeField()

    serializer1 = CommentSerializer(comment1)
    serializer2 = CommentSerializer(comment2)


    comments = []
    comments.append(comment1)
    comments.append(comment2)

    serializerz = CommentSerializer(comments, many=True)



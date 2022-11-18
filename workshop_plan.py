from posts.models import Post, Group, User
from django.db import connection, reset_queries

user = User(username='Kate', password='test')
user.save()
group = Group(title='test', slug='test')
group.save()
post = Post(text='Post for demonstration', group=group, author=user)

user.posts.first()
# Что забыли сделать?

# show model fields
for p in Post._meta.get_fields():
    print(p)

y_2022 = Post.objects.filter(pub_date__year=2022)
type(y_2022)
type(y_2022[0])

posts = Post.objects.all()
reset_queries()

[p.group.title for p in Post.objects.all()]

len(connection.queries)
for c in connection.queries[:6]:
    print(c)

reset_queries()

w_all_with_select = Post.objects.select_related('group').all()
[w.group.title for w in w_all_with_select]

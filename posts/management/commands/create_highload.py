from __future__ import annotations

from argparse import ArgumentParser
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand

from posts.decorators import show_time
from posts.models import Group, User, Post, Comment, Follow


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('--use_bulk', action='store_true', help='Использовать пакетное создание')
        parser.add_argument(
            '--amount',
            type=int,
            default=10,
            help='Количество базовых записей в БД',
        )

    @show_time
    def handle(self, *args: Any, **options: Any) -> None:
        amount = options['amount']
        use_bulk = options['use_bulk']
        # Cleanup
        self.cleanup()
        # Create
        self.create_users(amount=amount, use_bulk=use_bulk)
        self.create_groups(amount=amount, use_bulk=use_bulk)
        self.create_posts_with_comments(amount=amount, use_bulk=use_bulk)
        self.create_follows()

    @show_time
    def cleanup(self) -> None:
        Follow.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Group.objects.all().delete()
        User.objects.filter(is_staff=False).delete()

    # @show_time
    def create_users(self, amount: int, use_bulk: bool) -> None:
        if use_bulk:
            users = []
            for i in range(amount):
                users.append(
                    User(
                        username=f'user_{i}',
                        password=make_password(None),
                        is_active=True,
                        is_staff=False,
                    )
                )
            User.objects.bulk_create(users, batch_size=1000)
        else:
            for i in range(amount):
                User.objects.create_user(username=f'user_{i}')
        self.stdout.write(f'{amount} users were created')

    # @show_time
    def create_groups(self, *, amount: int, use_bulk: bool) -> None:
        if use_bulk:
            groups = []
            for i in range(amount):
                groups.append(Group(title=f'Group {i}', slug=f'group_{i}'))
            Group.objects.bulk_create(groups, batch_size=1000)
        else:
            for i in range(amount):
                Group.objects.create(title=f'Group {i}', slug=f'group_{i}')
        self.stdout.write(f'{amount} groups were created')

    # @show_time
    def create_posts_with_comments(self, *, amount: int, use_bulk: bool, posts_per_group: int = 10) -> None:
        groups = Group.objects.all()
        users = User.objects.all()[:10]
        if use_bulk:
            posts = []
            for group in groups:
                for i in range(posts_per_group):
                    posts.append(
                        Post(
                            author=users[i],
                            group=group,
                            text=f'Post {group.pk}_{i}'
                        )
                    )
            Post.objects.bulk_create(posts, batch_size=1000)
        else:
            for group in groups:
                for i in range(posts_per_group):
                    Post.objects.create(
                        author=users[i],
                        group=group,
                        text=f'Post {group.pk}_{i}'
                    )
        self.stdout.write(f'{amount*posts_per_group} posts were created')

    # @show_time
    def create_follows(self) -> None:
        ...

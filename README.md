# TODoList_API

Its a DRF project that users can use for handling their tasks.

Installations:
Django              4.2
django-redis        5.3.0
django-rest-auth
djangorestframework 3.14.0
redis               4.5.5

Features that this app provides so far in general are:
1. create, edit, delete groups of desired users
2. assigne tasks to groups
3. create, edit, delete tasks 
(Each user can edit/delete a task only if is the creator of that or is a member of one of task's assigned groups)
4. comment system for tasks
5. comments CRUD
6. automatic notifications for added users to/removed users from groups
7. notifications CRUD

-> Used some signals to handle m2m field changes
-> Added a custom middleware for caching (redis)

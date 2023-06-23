# TODoList_API

Its a DRF project that users can use for handling their tasks.

<h1>Installations:</h1>
Django              4.2<br />
django-redis        5.3.0<br />
django-rest-auth    0.9.5<br />
djangorestframework 3.14.0<br />
redis               4.5.5<br />
<h1>Features:</h1>
Features that this app provides so far in general are:<br />
1. create, edit, delete groups of desired users<br />
2. assigne tasks to groups<br />
3. create, edit, delete tasks<br />
(Each user can edit/delete a task only if is the creator of that or is a member of one of task's assigned groups)<br />
4. comment system for tasks<br />
5. comments CRUD<br />
6. automatic notifications for added users to/removed users from groups<br />
7. notifications CRUD<br />

-> Used some signals to handle m2m field changes<br />
-> Added a custom middleware for caching (redis)

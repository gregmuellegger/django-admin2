API
===

**django-admin2** comes with a builtin REST-API for accessing all the
resources you can get from the frontend via JSON.

The API can be found at the URL you choose for the admin2 and then append
``api/v0/``.

If the API has changed in a backwards-incompatible way we will increase the
API version to the next number. So you can be sure that you're frontend code
should keep working even between updates to more recent django-admin2
versions.

However currently we are still in heavy development, so we are using ``v0``
for the API, which means it is subject to change and can be broken at any
time.

A quick walkthrough
-------------------

Let's start a quick walkthrough of the API that the admin provides. In the
following examples we are expecting the django-admin2 instance to be hooked up
at ``https://example.com/admin/`` as the base URL (you are using the admin
only via HTTPS, right?).

So lets make our first request to the API.

**Request**::

    GET /admin/api/v0/

**Response**::

    HTTP 200 OK
    Vary: Accept
    Content-Type: text/html
    Allow: GET, HEAD, OPTIONS

    {
        "admins": [
            {
                "url": "https://example.com/admin/auth/user/api/v1/", 
                "model": {
                    "object_name": "User", 
                    "verbose_name": "user", 
                    "verbose_name_plural": "users", 
                    "app_label": "auth"
                }, 
                "name": "auth_user", 
                "versions": [
                    {
                        "url": "https://example.com/admin/auth/user/api/v1/", 
                        "version": "1"
                    }
                ]
            }, 
            ...
        ],
        "version": "0"
    }

So what you see here, is like the JSON representation of the admin frontpage.
It is simply a listing of all the models that have been registered with this
admin site. You can find those in the ``admins`` array. Every of those admins
has then a ``url`` that you can follow to get to the resource that is
describing that model. Like you see it also contains a bit meta data about how
the model is called etc, that you could use to re-build your own admin
dashboard.

And finally there is the ``"version"``. This is just what you expect. It is
the API version number that was used to generate the response you got from the
server. However, it is only the version that is in use for the API entrypoint
that we just accessed.

API versioning
--------------

.. todo: continue tour, explain why model APIs have different API versions and
   why you should care.

Authentication
--------------

The django-admin2 API doesn't support any fancy authentication processes yet.
We totally rely on the session cookie to be available. That is sufficient so
far and will work nicely if you only access the API via javascript from the
browser.

If you want to develop an external client that is consuming the admin API, you
propably want to look into `django-rest-framework's authentication backends`_.
Use those and plug them into the admin's API views as you wish.

.. _django-rest-framework's authentication backends:
    http://django-rest-framework.org/api-guide/authentication.html

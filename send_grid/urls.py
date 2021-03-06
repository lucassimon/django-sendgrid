from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from django.conf import settings

from dashboard.views import Dashboard, NotAllowed

from django.contrib import admin
admin.autodiscover()

sitemaps = {
    # Place sitemaps here
}


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # SEO API's
    url(
        r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    url(
        r'^$',
        Dashboard.as_view(),
        name='dashboard'
    ),


    url(
        r'^emails/',
        include('ssendgrid.urls', namespace='emails')
    ),

    url(
        r'^invoice/',
        include('invoices.urls', namespace='invoices')
    )

]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

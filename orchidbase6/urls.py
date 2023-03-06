from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/',include('home.urls')),
    url(r'^', include('simple_page.urls')),
    url(r'^expression_profiling/', include('expression_profiling.urls')),
    url(r'^pfam/', include('pfam.urls')),
    url(r'^promoter/', include('promoter.urls')),
    url(r'^GeneAnnotation/', include('GeneAnnotation.urls')),
    url(r'^Transcriptome/', include('transcriptome.urls')),
]

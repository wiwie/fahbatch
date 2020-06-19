from django.shortcuts import render
import os
from django.http.response import JsonResponse
from django.http.response import HttpResponse
from django.conf import settings
from cairosvg import svg2png

import urllib.request
import urllib.parse
import json
import time
import datetime

from django.core.exceptions import PermissionDenied

from django.views.decorators.cache import cache_control


@cache_control(max_age=3600)
def index(request, uid):
        allowed_uids = settings.ALLOWED_UIDS
        if not allowed_uids == '*' and not uid in allowed_uids:
            raise PermissionDenied()
        svg_file = os.path.join(settings.STATIC_ROOT, 'fah-batch-2.svg')
        with open(svg_file, 'rb') as f:
                svg_content = str(f.read(), 'UTF-8')

        fah_stats_url = 'https://stats.foldingathome.org/api/donor/%d' % uid
        f = json.loads(urllib.request.urlopen(fah_stats_url).read())
        wus = f['wus']
        credit = f['credit']
        rank = f['rank']

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        svg_content = svg_content.replace("$X", "%d" % wus)
        svg_content = svg_content.replace("$Y", "%d" % credit)
        svg_content = svg_content.replace("$Z", "%d" % rank)
        svg_content = svg_content.replace("$T", st)

        return HttpResponse(svg2png(bytestring=bytes(svg_content, 'UTF-8')), content_type='image/png')

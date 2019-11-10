from django.shortcuts import render
from django.views import View

# 1.首页 广告页
from apps.contents.models import ContentCategory
from apps.contents.utils import get_categories


class IndexView(View):
    def get(self, request):
        # 1.获取商品分类的数据
        categories = get_categories()

        # 2.获取 广告内容
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents,
        }

        return render(request, 'index.html', context)



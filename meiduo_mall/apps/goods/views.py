from django import http
from django.shortcuts import render
from datetime import datetime
from django.views import View

from apps.goods import models
from apps.contents.utils import get_categories
from apps.goods.models import GoodsCategory, SKU, GoodsVisitCount
from apps.goods.utils import get_breadcrumb
from utils.response_code import RETCODE


class VisitCountView(View):
    def post(self, request, category_id):

        # 1.校验参数
        try:
            category = GoodsCategory.objects.get(id=category_id)

        except Exception as e:
            return http.HttpResponseForbidden('商品不存在!')

        # 2. 判断 (当天 这个商品分类) 有没有 记录数据
        today_date = datetime.now()
        # 将 日期格式 ----"Y-m-d" 字符串的日期
        today_str = today_date.strftime('%Y-%m-%d')
        # 将 字符串日期------日期格式
        today_date = datetime.strptime(today_str, '%Y-%m-%d')

        try:
            # visit_count = category.goodsvisitcount_set.get(date=today_date)

            visit_count = GoodsVisitCount.objects.get(category=category, date=today_date)

        except Exception as e:
            # 3. 如果没有 新建一条数据
            visit_count = GoodsVisitCount()

        # 4. 累加 count += 1
        visit_count.category = category
        visit_count.count += 1
        visit_count.save()

        # 5. save()

        # 6. 返回响应对象
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


# 详情页的显示
class DetailView(View):
    def get(self, request, sku_id):
        """提供商品详情页"""
        # 获取当前sku的信息
        try:
            sku = models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return render(request, '404.html')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(sku.category)

        # 构建当前商品的规格键
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格信息
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options

        # 渲染页面
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs,
        }
        return render(request, 'detail.html', context)


class HotView(View):
    def get(self, request, category_id):
        # 1.获取 上架的 -- 三级分类对应--sales 降序 取前两个
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        # 2. 装换前端需要的数据格式
        skus_list = []
        for sku in skus:
            skus_list.append({
                'id': sku.id,
                'price': sku.price,
                'name': sku.name,
                'default_image_url': sku.default_image.url
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'hot_skus': skus_list})


class ListView(View):
    def get(self, request, category_id, page_num):
        # category_id 三级分类id

        category = GoodsCategory.objects.get(id=category_id)

        # 1. 商品分类数据
        categories = get_categories()

        # 2.获取面包屑组件
        bread_crumb = get_breadcrumb(category)

        # 3. 排序判断 default==create_time price=price hot==-sales
        sort = request.GET.get('sort')
        order_field = "create_time"
        if sort == "price":
            order_field = "price"
        elif sort == "hot":
            order_field = "-sales"
        else:
            order_field = "create_time"

        # 获取 所有上架的商品(对应的类)---排序
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(order_field)

        # 每页有几个;   每页显示哪几个  ;  总页数;  当前页数 page_num
        from django.core.paginator import Paginator
        paginator = Paginator(skus, 5)
        page_skus = paginator.page(page_num)
        total_nums = paginator.num_pages

        context = {
            'categories': categories,
            'breadcrumb': bread_crumb,
            'category': category,
            'sort': sort,  # 排序字段
            'page_skus': page_skus,  # 分页后数据
            'total_page': total_nums,  # 总页数
            'page_num': page_num,  # 当前页码
        }
        return render(request, 'list.html', context)

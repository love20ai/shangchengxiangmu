import json

from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU
from utils.cookiesecret import CookieSecret


class CartsView(View):
    def post(self, request):
        # 1.接收 参数 json
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)

        # 2.校验
        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            return http.JsonResponse({'code': '0', 'errmsg': '商品不存在!'})

        try:
            count = int(count)
        except Exception as e:
            return http.HttpResponseForbidden('count 必须是 数字类型')

        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('selected 必须是 布尔类型')

        # 3.判断是否登录 手动判断
        user = request.user
        response = http.JsonResponse({'code': '0', 'errmsg': '添加购物车成功'})
        if user.is_authenticated:
            # 4.登录 redis存储
            # 4.1 链接redis
            client = get_redis_connection('carts')

            # 4.2 获取 当前用户 的 购物车数据
            redis_carts_data = client.hgetall(user.id)

            # 4.4 没有值 --直接新增 --sku_id  hset
            #     有值----sku_id: count += 1 hset
            # {b'1':b'{count:1,selected:true}'}
            if str(sku_id).encode() in redis_carts_data:

                # 1.根据 key  取出对应的 字典
                sku_dict = json.loads(redis_carts_data[str(sku_id).encode()].decode())

                # 2. dict['count'] += count
                sku_dict['count'] += count

                # 3. 覆盖以前的值
                client.hset(user.id, sku_id, json.dumps(sku_dict))

            else:
                client.hset(user.id, sku_id, json.dumps({'count': count, 'selected': selected}))


        else:
            # 5.未登录 cookie存储
            # 1.从cookie 取出数据
            cookie_str = request.COOKIES.get('carts')

            # 2.如果有数据-->解码
            if cookie_str:
                cookie_dict = CookieSecret.loads(cookie_str)
            else:
                cookie_dict = {}

            # 3. 判断 sku_id 是否存在; 在 +=count , 不在 新字典
            if sku_id in cookie_dict:
                # 将以前的个数 和 现在的个数累加
                orginal_count = cookie_dict[sku_id]['count']
                count = orginal_count + count

            cookie_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            print(cookie_dict)
            # 编码 加密
            dumps_str = CookieSecret.dumps(cookie_dict)
            response.set_cookie('carts', dumps_str, max_age=14 * 24 * 3600)

        # 返回响应对象
        return response

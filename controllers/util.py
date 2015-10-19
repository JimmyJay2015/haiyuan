#-*-coding:utf-8 -*-

import random
import string 
import Image
import ImageDraw, ImageFont, ImageFilter
 
from sqlalchemy.ext.declarative import DeclarativeMeta

#生成随机字符串，默认只有数字，
def get_random_code(length, has_lower=False, has_upper=False):
    chars = string.digits
    if has_lower:
        chars += string.lowercase
    if has_upper:
        chars += string.uppercase
    if length>len(chars):
        length = len(chars)
    return ''.join(random.sample(chars, length))

def create_validate_code(chars, 
                         size=(100, 30),
                         mode="RGB",  
                         bg_color=(255, 255, 255),  
                         fg_color=(255, 0, 0),  
                         font_size=18,  
                         font_type="/Data/webcode/asim_server/static/font/monaco.ttf",
                         draw_points=True,  
                         point_chance = 2):  
    ''''' 
    size: 图片的大小，格式（宽，高），默认为(120, 30) 
    chars: 允许的字符集合，格式字符串 
    mode: 图片模式，默认为RGB 
    bg_color: 背景颜色，默认为白色 
    fg_color: 前景色，验证码字符颜色 
    font_size: 验证码字体大小 
    font_type: 验证码字体，默认为 /Data/webcode/asim_server/static/font/monaco.ttf 
    length: 验证码字符个数 
    draw_points: 是否画干扰点 
    point_chance: 干扰点出现的概率，大小范围[0, 50] 
    ''' 
 
    width, height = size  
    img = Image.new(mode, size, bg_color) # 创建图形  
    draw = ImageDraw.Draw(img) # 创建画笔 
 
    def create_points():  
        '''''绘制干扰点''' 
        chance = min(50, max(0, int(point_chance))) # 大小限制在[0, 50]  
 
        for w in xrange(width):  
            for h in xrange(height):  
                tmp = random.randint(0, 50)  
                if tmp > 50 - chance:  
                    draw.point((w, h), fill=(0, 0, 0))
    
    if draw_points:  
        create_points()
    
    font = ImageFont.truetype(font_type, font_size)  
    font_width, font_height = font.getsize(chars)  
 
    draw.text(((width - font_width) / 3, (height - font_height) / 4),  
                    chars, font=font, fill=fg_color)  
 
    # 图形扭曲参数  
    params = [1 - float(random.randint(1, 2)) / 100,  
              0,  
              0,  
              0,  
              1 - float(random.randint(1, 10)) / 100,  
              float(random.randint(1, 2)) / 500,  
              0.001,  
              float(random.randint(1, 2)) / 500 
              ]  
    img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲  
 
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）  
 
    return img

def sa_to_dict(obj, filtrate=None, rename=None):
    """
    sqlalchemy 对象转为dict
    :param filtrate: 过滤的字段
    :type filtrate: list or tuple
    :param rename: 需要改名的,改名在过滤之后处理, key为原来对象的属性名称，value为需要更改名称
    :type rename: dict
    :rtype: dict
    """
 
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        #该类的相关类型，即直接与间接父类
        cla = obj.__class__.__mro__
        #过滤不需要的父类
        cla = filter(lambda c: hasattr(c, '__table__'), filter(lambda c: isinstance(c, DeclarativeMeta), cla))
        columns = []
        map(lambda c: columns.extend(c.__table__.columns), cla[::-1])
        # columns = obj.__table__.columns
        if filtrate and isinstance(filtrate, (list, tuple)):
            fields = dict(map(lambda c: (c.name, getattr(obj, c.name)), filter(lambda c: not c.name in filtrate, columns)))
        else:
            fields = dict(map(lambda c: (c.name, getattr(obj, c.name)), columns))
        # fields = dict([(c.name, getattr(obj, c.name)) for c in obj.__table__.columns])
        if rename and isinstance(rename, dict):
            #先移除key和value相同的项
            _rename = dict(filter(lambda (k, v): str(k) != str(v), rename.iteritems()))
            #如果原始key不存在，那么新的key对应的值默认为None
            #如果新的key已存在于原始key中，那么原始key的值将被新的key的值覆盖
            # map(lambda (k, v): fields.setdefault(v, fields.pop(k, None)), _rename.iteritems())
            map(lambda (k, v): fields.update({v: fields.pop(k, None)}), _rename.iteritems())
        #
        return fields
    else:
        return {}  
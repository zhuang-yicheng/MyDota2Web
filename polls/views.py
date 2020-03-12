from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello world.You're at the poll index.")

from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

CurrentConfig.GLOBAL_ENV = Environment(loader = FileSystemLoader("./polls/templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar

def pyecharts_test1(request):
    bar = (
        Bar()
        .add_xaxis(['衬衫','羊毛衫','雪纺衫','裤子','高跟鞋','袜子'])
        .add_yaxis("商家A", [5,20,36,10,75,90])
        .add_yaxis("商家B", [15,25,16,55,48,8])
        .set_global_opts(title_opts = opts.TitleOpts(title = "Bar-基本示例", subtitle = "我是副标题"))
    )
    return HttpResponse(bar.render_embed())
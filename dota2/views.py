from django.shortcuts import render
from django.http import HttpResponse
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./polls/templates"))

from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.charts import Bar, Grid, Line, Scatter

from account.config import get_my_key
from fundata_python_sdk.fundata.client import init_api_client
from fundata_python_sdk.fundata.client import get_api_client

import pandas as pd
from pandas.io.json import json_normalize

# Create your views here.

def team(request):
    public_key, secret_key = get_my_key()
    init_api_client(public_key, secret_key)

    client = get_api_client()
    uri = '/fundata-dota2-free/v2/league/team'  # 战队列表
    data = {"page": 0, "limit": 10000}  # limit默认是16
    res = client.api(uri, data)  # GET请求

    df = json_normalize(res['data'])
    df = df[(df['id'] > 0) & (df['region'] != '')][['region','name']]
    df.columns = ['地区', '队伍数量']
    df = df.groupby(['地区'])['队伍数量'].count().reset_index().sort_values(['队伍数量'], ascending=False)

    bar = (
        Bar()
            .add_xaxis(df['地区'].tolist())
            .add_yaxis("队伍数量", df['队伍数量'].tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title="各地区队伍数量"))#, subtitle="我是副标题")
    )

    line = (
        Line()
            .add_xaxis(df['地区'].tolist())
            .add_yaxis("队伍数量", df['队伍数量'].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="各地区队伍数量")
            )#, subtitle="我是副标题"))
    )

    grid = (
        Grid()
        .add(bar, grid_opts = opts.GridOpts(pos_bottom = "60%", pos_right = "-100%"))
        .add(line, grid_opts = opts.GridOpts(pos_top = "60%", pos_right = "55%"))
    )
    return HttpResponse(grid.render_embed())
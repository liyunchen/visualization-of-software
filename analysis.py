# -*- coding: utf-8 -*-


"""
李运辰 2021-3-4

公众号：python爬虫数据分析挖掘
"""

# 导包
import pandas as pd
# from pyecharts import options as opts
# from pyecharts.globals import ThemeType
# from pyecharts.charts import Bar
# from pyecharts.charts import Pie
from stylecloud import gen_stylecloud
import jieba

#读入数据
df_all = pd.read_csv("弹幕数据集-李运辰.csv",encoding="gbk")
df = df_all.copy()

# 重置索引
df = df.reset_index(drop=True)
#print(df.head())

#累计发送弹幕数的用户
def an1():
    danmu_counts = df.groupby('uid')['content'].count().sort_values(ascending=False).reset_index()
    danmu_counts.columns = ['用户id', '累计发送弹幕数']
    name = danmu_counts['用户id']
    name = (name[0:10]).tolist()
    dict_values = danmu_counts['累计发送弹幕数']
    dict_values = (dict_values[0:10]).tolist()

    # 链式调用
    c = (
        Bar(
            init_opts=opts.InitOpts(  # 初始配置项
                theme=ThemeType.MACARONS,
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="cubicOut"  # 初始动画延迟和缓动效果
                ))
        )
            .add_xaxis(xaxis_data=name)  # x轴
            .add_yaxis(series_name="累计发送弹幕数的用户", yaxis_data=dict_values)  # y轴
            .set_global_opts(
            title_opts=opts.TitleOpts(title='', subtitle='',  # 标题配置和调整位置
                                      title_textstyle_opts=opts.TextStyleOpts(
                                          font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                      ), pos_left="90%", pos_top="10",
                                      ),
            xaxis_opts=opts.AxisOpts(name='用户id', axislabel_opts=opts.LabelOpts(rotate=45)),
            # 设置x名称和Label rotate解决标签名字过长使用
            yaxis_opts=opts.AxisOpts(name='累计发送弹幕数'),

        )
            .render("累计发送弹幕数的用户.html")
    )

#查看某个用户评论情况
def an2():
    df_top1 = df[df['uid'] == 2127950839].sort_values(by="likeCount", ascending=False).reset_index()
    print(df_top1.head(20))

#查看用户(2127950839)每一集的评论数
def an3():
    df_top1 = df[df['uid'] == 2127950839].sort_values(by="likeCount", ascending=False).reset_index()
    data_top1 = df_top1.groupby('tvname')['content'].count()
    print(data_top1)
    name = data_top1.index.tolist()
    dict_values = data_top1.values.tolist()
    # 链式调用
    c = (
        Bar(
            init_opts=opts.InitOpts(  # 初始配置项
                theme=ThemeType.MACARONS,
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="cubicOut"  # 初始动画延迟和缓动效果
                ))
        )
            .add_xaxis(xaxis_data=name)  # x轴
            .add_yaxis(series_name="查看用户（2127950839）每一集的评论数", yaxis_data=dict_values)  # y轴
            .set_global_opts(
            title_opts=opts.TitleOpts(title='', subtitle='',  # 标题配置和调整位置
                                      title_textstyle_opts=opts.TextStyleOpts(
                                          font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                      ), pos_left="90%", pos_top="10",
                                      ),
            xaxis_opts=opts.AxisOpts(name='集数', axislabel_opts=opts.LabelOpts(rotate=45)),
            # 设置x名称和Label rotate解决标签名字过长使用
            yaxis_opts=opts.AxisOpts(name='评论数'),

        )
            .render("查看用户（2127950839）每一集的评论数.html")
    )

#剧集评论点赞数最多的评论内容
def an4():
    df_like = df[df.groupby(['tvname'])['likeCount'].rank(method="first", ascending=False) == 1].reset_index()[['tvname', 'content', 'likeCount']]
    df_like.columns = ['集', '弹幕内容', '点赞数']
    print(df_like)

#评论内容词云
def an5():
    contents = (df_all['content']).tolist()

    text = "".join(contents)
    with open("stopword.txt", "r", encoding='UTF-8') as f:
        stopword = f.readlines()
    for i in stopword:
        print(i)
        i = str(i).replace("\r\n", "").replace("\r", "").replace("\n", "")
        text = text.replace(i, "")
    word_list = jieba.cut(text)
    result = " ".join(word_list)  # 分词用 隔开
    # 制作中文云词
    icon_name = 'fas fa-play'
    gen_stylecloud(text=result, icon_name=icon_name, font_path='simsun.ttc',
                   output_name="评论内容词云.png")  # 必须加中文字体，否则格式错误


#累计发送弹幕数的用户
#an1()
#查看某个用户评论情况
#an2()
#查看用户每一集的评论数
#an3()
#剧集评论点赞数最多的评论内容
#an4()
#评论内容词云
an5()
import numpy as np
import calendar
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def engagement_summary(df,sma = "Twitter"):
    if sma == "Twitter":
        all_tweets = df[df['SMA'] == "Twitter"]  # [['SMA','Click-Through-Rate','Link Clicks']]
    elif sma == "Facebook":
        all_tweets = df[df['SMA'] == "Facebook"]  # [['SMA','Click-Through-Rate','Link Clicks']]
    else:
        all_tweets = df[df['SMA'] == "LinkedIn"]
        #     average CTR ===
    ate = round(np.mean(all_tweets['Click-Through-Rate']) * 100, 2)
    ade = round(all_tweets.groupby('Date_').sum().reset_index()['Click-Through-Rate'].mean(), 2) * 100
    #     link clicks
    link_clicks = f"{all_tweets['Link Clicks'].sum():,}"
    link_clicks_pt = f"{round(all_tweets['Link Clicks'].mean()):,}"
    link_clicks_pd = f"{round(all_tweets.groupby('Day_').sum().reset_index()['Link Clicks'].mean()):,}"
    #     likes
    total_likes = f"{all_tweets['Likes'].sum():,}"
    likes_pt = f"{round(all_tweets['Likes'].mean()):,}"
    likes_pd = f"{round(all_tweets.groupby('Day_').sum().reset_index()['Likes'].mean()):,}"
    #     all content
    tweet_count = f"{all_tweets.shape[0]:,}"
    #     total impressions
    total_impressions = f"{all_tweets.Impressions.sum():,}"
    #     total_folows
    total_folows = f"{all_tweets.Follows.sum():,}"
#     average engagements per tweet
    aveg = round(all_tweets.Engagements.mean(),2)
#     average impressions
    avi = f"{round(all_tweets.Impressions.mean(),2):,}"

    result = (ate, ade, link_clicks, link_clicks_pt, link_clicks_pd, total_likes, likes_pd,
              likes_pt, tweet_count, total_impressions, total_folows,aveg,avi)

    return result

    result = (ate, ade, link_clicks, link_clicks_pt, link_clicks_pd, total_likes, likes_pd,
              likes_pt, tweet_count, total_impressions, total_folows, aveg, avi)


    # result = (ate, ade, link_clicks, link_clicks_pt, link_clicks_pd, total_likes, likes_pd,
    #           likes_pt, tweet_count, total_impressions, total_folows)
    #
    # return result


# plot functions
def impression_day_month(df, plot, grouping, engagement, template='presentation', viz='Twitter'):
    if viz == 'Twitter':
        df = df[df['SMA'] == "Twitter"]
    elif viz == "Facebook":
        df = df[df['SMA'] == "Facebook"]
    elif viz == "LinkedIn":
        df = df[df['SMA'] == "LinkedIn"]
    df_imp = df.groupby(grouping).sum()  # .reset_index()
    if grouping == 'Month_':
        df_imp = df_imp.reindex(calendar.month_name).reset_index().dropna(axis=0, how='any')
        title = "{} {} per Month".format(viz, engagement)
        x_axis = list(calendar.month_name)
    else:
        df_imp = df_imp.reindex(calendar.day_name).reset_index().dropna(axis=0, how='any')
        title = "{} {} by Week Day".format(viz, engagement)
    if plot == "line":
        fig = px.area(data_frame=df_imp, x=grouping, y=engagement, title=title, template=template, height=350)
    else:
        fig = px.bar(data_frame=df_imp, x=grouping, y=engagement, title=title, template=template, height=350)
    return fig


# comentary
def comentary(df, mode, engagement, sub='Twitter'):
    if sub == 'Twitter':
        df = df[df['SMA'] == "Twitter"]
    elif sub == "Facebook":
        df = df[df['SMA'] == "Facebook"]
    elif sub == "LinkedIn":
        df = df[df['SMA'] == "LinkedIn"]
    inFile = df.groupby(mode).sum().reset_index()
    # monthly/weekly stats
    monthly_engagements = f"{round(round(inFile[engagement].mean())):,}"
    per_tweet_stat = f"{round(df[engagement].sum() / df.shape[0], ndigits=2):,}"
    max_stat = inFile[inFile[engagement] == max(inFile[engagement])][[mode, engagement]]
    min_stat = inFile[inFile[engagement] == min(inFile[engagement])][[mode, engagement]]

    if mode == "Month_":
        comentary = """On average ,you have had {} {} per month and {} per {}.
        {} had the highest {} for the whole year while {} had the least.""" \
            .format(monthly_engagements, engagement, per_tweet_stat, "tweet", max_stat[mode].values[0], engagement,
                    min_stat[mode].values[0])
    else:
        comentary = """You have had {} {} per week.
        {} have been the best day to share with a maximum {} of {}.""" \
            .format(monthly_engagements, engagement, max_stat[mode].values[0], engagement,
                    min_stat[engagement].values[0])

    return comentary


# top and bottom tweets
def top_bottom_plots(df, top=True):
    df = df[df['SMA'] == "Twitter"]
    top_5 = df.sort_values('Impressions', ascending=False).query('SMA == "Twitter"')
    top_5.Post = top_5.Post.str[:25] + "..."
    if top:
        fig = px.bar(top_5.head(), y='Post', x='Impressions', orientation='h', width=550, height=300)
    else:
        fig = px.bar(top_5.tail(), y='Post', x='Impressions', orientation='h', width=550, height=300)
    return fig


# best and worst perfoming tweets
def ctr(df):
    df = df[df['SMA'] == "Twitter"]
    ctr = df.groupby('Post Format').mean().reset_index()[['Post Format', 'Click-Through-Rate']]
    ctr['Click-Through-Rate'] = round(ctr['Click-Through-Rate'] * 100, 2)
    best = ctr[ctr['Click-Through-Rate'] == max(ctr['Click-Through-Rate'])]
    worst = ctr[ctr['Click-Through-Rate'] == min(ctr['Click-Through-Rate'])]
    return best['Post Format'].values[0], best['Click-Through-Rate'].values[0], worst['Post Format'].values[0], \
           worst['Click-Through-Rate'].values[0]


# engagements vs post types
# @interact(engagement=['Impressions','Click-Through-Rate', 'Retweets/Shares', 'Likes', 'Video Views','Link Clicks', 'Detail Expands', 'Hashtag Clicks','Media Engagements', 'Total Engagements','Engagements', 'Follows', 'Replies', 'Post/Tweet Length'])
def plot_en(df, engagement, sub='Twitter'):
    # df=company_A_data
    if sub == 'Twitter':
        df = df[df['SMA'] == "Twitter"]
    elif sub == "Facebook":
        df = df[df['SMA'] == "Facebook"]
    en_df = df[['Post Format', engagement]].groupby('Post Format').sum().reset_index()
    fig = px.bar(data_frame=en_df, x='Post Format', y=engagement, title="{} vs Post Format".format(engagement),
                 template='presentation', height=350)
    fig = fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total ascending'})
    # fig.show()
    return fig


# top Fb
def top_fb(df, sub="Facebook"):
    df = df[df['SMA'] == sub]
    top_posts = df.sort_values(by="Click-Through-Rate", ascending=False)[
        ['Date_', 'Post', 'Click-Through-Rate', 'Post Format']].head(5)
    top_posts.Post = top_posts.Post.str[:47] + "..."
    # top_5.Post.str[:25] + "..."
    return top_posts


# major fb engagements
def major_fb_engagements(df,sub="Facebook"):
    # data preprocessing
    if sub == "FaceBook":
        df = df[df['SMA'] == 'Facebook']
    elif sub == "LinkedIn":
        df = df[df['SMA'] == 'LinkedIn']
    post_types = df.groupby('Post Format').count().reset_index()[['Post Format', 'Impressions']].rename(
        columns={'Impressions': 'Count'})
    post_types.sort_values('Count', ascending=False).assign(
        Propotion=round(post_types.Count / post_types.Count.sum(), 3) * 100
    ).reset_index(drop=True)
    fig = px.pie(post_types, names='Post Format', values='Count', title='{} Post Format Propotions'.format(sub),height=400,template='presentation')
    # fig.show()
    return fig

homepage = dbc.Jumbotron(
    [
        html.H1("Social Media Performance Dashboard", className="display-3"),
        html.P(
            "Quick and fast insights",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "Welcome"
        ),
        html.P(dbc.Button("Learn more", color="primary"), className="lead"),
    ]
)
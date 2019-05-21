import os
from pprint import pformat
from aiohttp import ClientSession
from aiohttp import web
from bs4 import BeautifulSoup
from aiohttp.web_request import Request
import trafaret as t

URL = 'https://www.bbc.com/'
TEG = 'a'
CLASS = "gs-c-promo-heading"


async def fetch(session: ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


routes = web.RouteTableDef()


@routes.get('/')
async def get_chapters(request: Request):
    async with ClientSession() as session:
        tmp = t.Dict({'limit': t.String})
       # tmp = t.Dict({t.String: t.})
        params = {item[0]: item[1] for item in request.query.items()}
        converter = t.Dict({
            t.Key('chapter', default= 'news') >> 'chapter': t.String,
            t.Key('limit' , default= 1000) >> 'limit': t.Int,})
       # tmp.check(params)

        print(converter)
        print(params)



        try:
            params = converter.check(params)



        #except (KeyError, ValueError) as e:
        except (t.DataError) as e:
            return web.Response(text=str(t.extract_error(converter,params)))
        chapter = params['chapter']
        end = int(params['limit'])
        html = await fetch(session, URL + chapter)
        bs_obj = BeautifulSoup(html, features="html.parser")

        tmp1 = bs_obj.findAll(TEG, {CLASS})
        news = [{'title': item.get_text(), 'URL': item['href']} for (i, item) in enumerate(tmp1) if i < end]

        js = {'chapter': chapter,
              'news': news}

    return web.Response(text=pformat(js))


app = web.Application()
app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))

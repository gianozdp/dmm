# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import dblite
import unicodedata
import urllib2
import re
from dmm.items import DmmItem,ActorItem,CompanyItem,SeriesItem
from dmm.items import LevelItem,GenreItem
from scrapy.exceptions import DropItem

class DmmPipeline(object):

    def __init__(self):
        self.ds=None
        self.ds_actor=None
        self.actors=None
        self.videos=None
        self.ds_company=None
        self.ds_series=None
        self.ds_level=None
        self.ds_genres=None

    def open_spider(self,spider):
        try:
            self.ds=dblite.open(DmmItem,'sqlite://db/video.sqlite:data_videos',autocommit=True)
            self.ds_actor=dblite.open(ActorItem,'sqlite://db/video.sqlite:data_actors',autocommit=True)
            self.ds_company=dblite.open(CompanyItem,'sqlite://db/video.sqlite:data_company',autocommit=True)
            self.ds_series=dblite.open(SeriesItem,'sqlite://db/video.sqlite:data_series',autocommit=True)
            self.ds_level=dblite.open(LevelItem,'sqlite://db/video.sqlite:data_levels',autocommit=True)
            self.ds_genres=dblite.open(GenreItem,'sqlite://db/video.sqlite:data_genres',autocommit=True)

        except Exception as ex:
            print("--------------------------------")
            print(str(ex))
            print("--------------------------------")

    def close_spider(self,spider):
        self.ds_actor.commit()
        self.ds_company.commit()
        self.ds_level.commit()
        self.ds_genres.commit()
        self.ds.commit()

        self.ds.close()
        self.ds_genres.close()
        self.ds_level.close()
        self.ds_actor.close()
        self.ds_company.close()
    def process_item(self, item, spider):
        if isinstance(item,DmmItem):
            try:
                #print(item['video_actor'])
                #print(self.actors)
                item['video_code']=item['video_code'].encode('utf-8')
                item['video_company']=self.parse_company(company=item['video_company'])
                item['video_actor']=self.parse_actor(actor=item['video_actor'])
                item['video_series']=self.parse_series(series=item['video_series'])
                item['video_level']=self.parse_level(level=item['video_level'])
                item['video_genre']=self.parse_genre(item['video_genre'])
                existVideos=[p for p in self.ds.get({'video_code':item['video_code']})]
                if len(existVideos)==0:
                    self.ds.put(item)

            except dblite.DuplicateItem:
                raise DropItem("Duplicate item found")
            except Exception as ex:
                print(str(ex))
        else:
            raise DropItem("Unknown item type")
        return item

    def parse_actor(self,actor):
        #for items in self.actors:
        #   print(items)

        for (k,v) in actor.items():
            # print('----------------------------------------------')
            newActor=ActorItem(actor_code=k,actor_name=v)
            results=self.ds_actor.get({'actor_code':k})
            # print(results)
            # print('----------------------------------------------1')
            existActors=[p for p in results]

            if len(existActors)==0:
                self.ds_actor.put(newActor)
            # print('----------------------------------------------')
            return k
            #
            # if not self.actors.get(k):
            #     newActor=ActorItem(actor_code=k,actor_name=v)
            #     ds_actor.put(newActor)
            # return k
            #


    def parse_company(self,company):
        if len(company)!=0:
            txt=re.search(r'\>.*\<\/',company).group(0)
            if len(txt)!=0:
                size=len(txt)
                txt=txt[1:size-2]
            id=re.search(r'id=\d*',company).group(0)
            id=id[3:].encode('utf-8')

            existCompany=[p for p in self.ds_company.get({'company_code':id})]
            if not existCompany:
                newCompany=CompanyItem(company_code=id,company_name=txt)
                self.ds_company.put(newCompany)
            return id
        else:
            return None

    def parse_series(self,series):
        if len(series)!=0:
            m=re.search(r'\>.*\<\/',series)
            if m:
                txt=m.group(0)
                if len(txt)!=0:
                    size=len(txt)
                    txt=txt[1:size-2]
                id=re.search(r'id=\d*',series).group(0)
                id=id[3:].encode('utf-8')

                existSeries=[p for p in self.ds_series.get({'series_code':id})]
                #print('---------------------------')
                if not existSeries:
                    newSeries=SeriesItem(series_code=id,series_name=txt)
                    self.ds_series.put(newSeries)
                return id
            return None

    def parse_level(self,level):
        if len(level)!=0:
            m=re.search(r'\>.*\<\/',level)
            if m:
                txt=m.group(0)
                if len(txt)!=0:
                    size=len(txt)
                    txt=txt[1:size-2]
                id=re.search(r'id=\d*',level).group(0)
                id=id[3:].encode('utf-8')

                existLevel=[p for p in self.ds_level.get({'level_code':id})]
                #print(existLevel)
                if not existLevel:
                    newItem=LevelItem(level_code=id,level_name=txt)
                    self.ds_level.put(newItem)
                return id
            return None

    def parse_genre(self,genres):
        genre_codes=[]
        if not genres:
            return None
        else:
            for genre in genres.split('</a>'):
                if not genre:
                    continue
                else:
                    txt=re.search(r'\>.*$',genre)
                    id=re.search(r'id=\d*',genre)

                    if txt and id:
                        txt=txt.group(0)[1:]
                        code=id.group(0).encode('utf-8')[3:]

                        getGenres=self.ds_genres.get({'genre_code':code})
                        exists=[p for p in getGenres]
                        #print(exists)
                        if not exists:
                            newGenre=GenreItem(genre_code=code,genre_name=txt)
                            self.ds_genres.put(newGenre)

                        genre_codes.append(code)
            if genre_codes:
                return ",".join(genre_codes)

            else:
                return None


    def downloadPic(self,url):
        socket=urllib2.urlopen(url)
        data=socket.read()
        socket.close()
        return data

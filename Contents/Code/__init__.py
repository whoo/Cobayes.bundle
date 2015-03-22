PLUGIN_PREFIX           = "/video/Cobayes"
PLUGIN_ID               = "com.plexapp.plugins.Cobayes"
PLUGIN_REVISION         = 0.5
PLUGIN_UPDATES_ENABLED  = True
CACHE_INTERVAL = 3600 * 2
ICON="icon-default.png"
ART ='art-default.jpg'
NAME="On n'est pas que des cobayes"


base="https://www.googleapis.com/youtube/v3/playlistItems?"
search="https://www.googleapis.com/youtube/v3/search?"
playlist="https://www.googleapis.com/youtube/v3/playlists?"

video="https://www.youtube.com/watch?v=%s"
key="AIzaSyDq0YgvkD2-xo88kl073MK5ua_3935ROC4"


def Start():
	Plugin.AddPrefixHandler("/video/Cobayes", ListeCategories,"Cobaye", "logo.jpg", "logo-On-nest-pas-que-des-cobayes-600x340.jpg")
	ObjectContainer.title1    = L('Video Youtube')
	ObjectContainer.art       = R("logo-On-nest-pas-que-des-cobayes-600x340.jpg")
#        Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
#        Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
#        ObjectContainer.viewgroup = 'Details'


#Root categories

def addparam(url,param):
    return url+"&"+param




#@route("/video/Cobayes/Video/<info>")
@route(PLUGIN_PREFIX+"/Video")
def Video(info):
        Log(info)
        info=JSON.ObjectFromString(info)
        playlist=info['pl']
        title=info['ti']
        url=base
        url=addparam(url,'part=snippet')
        url=addparam(url,'playlistId=%s'%playlist)
        url=addparam(url,'key=%s'%key)
        url=addparam(url,'maxResults=50')

        data=JSON.ObjectFromURL(url)
        oc=ObjectContainer(title2=title)

        for a in data['items']:
                url=video%a['snippet']['resourceId']['videoId']
                title=a['snippet']['title']
                summary=a['snippet']['description']
                thumb=a['snippet']['thumbnails']['medium']['url']
                dd=MovieObject(url=url,title=L(title),summary=summary,thumb=thumb)
                oc.add(dd)
        return oc


def ListeCategories():
        oc = ObjectContainer()
        
#        PlayLists=[
#        {'Playlist':'PLEY1NNPhwXGWnd8uNPY3RVHPyNDlXnOwo','name':'Emission','thumb':'icon-videos.png' },
#        {'Playlist':'PLEY1NNPhwXGXqZCIg4bWqUH_dbYbecNPO','name':'Defis','thumb':'icon-channels.png'},
#        {'Playlist':'PLh-qVJTuss12drO62KwC5yr6zdXDJEAng','name':'C est pas sorcier','thumb':'icon-channels.png'}]
#        
#        for a in PlayLists:
#                oc.add( DirectoryObject(key=Callback(Video,playlist=a['Playlist']),title=a['name'],summary='',thumb=R(a['thumb'])))

        url=search
        url=addparam(url,'part=snippet')
        url=addparam(url,'channelId=UC9_IuigMSJd-q-buggknOuQ')
        url=addparam(url,'videoDuration=medium')
        url=addparam(url,'type=video')
        url=addparam(url,'key=%s'%key)
        url=addparam(url,'maxResults=50')
        oc.add( DirectoryObject(key=Callback(SearchAllV,url=url),title='All Cobayes',summary=L('Emission des cobayes'),thumb=R('icon-videos.png')))

        url=playlist
        url=addparam(url,'part=snippet')
        url=addparam(url,'channelId=UCENv8pH4LkzvuSV_qHIcslg')
        url=addparam(url,'key=%s'%key)
        url=addparam(url,'maxResults=50')
        
        oc.add(DirectoryObject(key=Callback(SearchAllP,url=url),title='Sorcier',summary=L('On n est pas que des sorciers'),thumb=R('icon-related.png')))
        
        
        return oc


#@route('/video/Cobayes/searchAllP/<url>')
def SearchAllP(url):
        oc=ObjectContainer(title2="C est pas Sorcier")
        error=None
        nextp=True
        urlb=url
        while (error is None and nextp is not None):
                xml=JSON.ObjectFromURL(url)
                error=TestError(xml)
                        
                if (error is None):
                        for a in xml['items']:
                                title=a['snippet']['title']
                                playlist=a['id']
                                thumb=a['snippet']['thumbnails']['medium']['url']
                                info={'pl': playlist,'ti':title}
                                info=JSON.StringFromObject(info)
                                oc.add(DirectoryObject(key=Callback(Video,info=info),title=title,summary='',thumb=thumb))
                                if ('nextPageToken' in xml.keys()):
                                        nextp=xml['nextPageToken']
                                        url=addparam(urlb,'pageToken=%s'%nextp)
                                        print("new url %s",url)
                                else:
                                        nextp=None
        return oc



#@route("/video/Cobayes/searchAllV/<url>")
def SearchAllV(url):
        oc=ObjectContainer(title2="Les cobayes")
        
        error=None
        nextp=True
        urlb=url
        
        while (error is None and nextp is not None):
                xml=JSON.ObjectFromURL(url)
                if ("error" in xml.keys()):
                        Log("ERROR [%10s]"%xml['error']['errors'][0]['reason']);
                        error=True
                
                if (error is None):
                        for a in xml['items']:
                                url=video%a['id']['videoId']
                                title=a['snippet']['title']
                                summary=a['snippet']['description']
                                thumb=a['snippet']['thumbnails']['medium']['url']
                                dd=MovieObject(url=url,title=L(title),summary=summary,thumb=thumb)
                                oc.add(dd)
                        if ('nextPageToken' in xml.keys()):
                                nextp=xml['nextPageToken']
                                url=addparam(urlb,'pageToken=%s'%nextp)
                                print("new  url %s"%url)
                        else:
                                nextp=None
        return oc 



def TestError(xml):
        if ("error" in xml.keys()):
                print("ERROR [%10s]"%xml['error']['errors'][0]['reason']);
                return True
        else:
                return None


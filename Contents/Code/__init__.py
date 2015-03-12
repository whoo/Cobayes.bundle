PLUGIN_PREFIX           = "/video/Cobayes"
PLUGIN_ID               = "com.plexapp.plugins.Cobayes"
PLUGIN_REVISION         = 0.5
PLUGIN_UPDATES_ENABLED  = True
CACHE_INTERVAL = 3600 * 2
ICON="icon-default.png"
ART ='art-default.jpg'
NAME="On n'est pas que des cobayes"


def Start():
	Plugin.AddPrefixHandler("/video/Cobayes", ListeCategories,"Cobaye", "logo.jpg", "logo-On-nest-pas-que-des-cobayes-600x340.jpg")
	ObjectContainer.title1    = 'On n\'est pas sur de Cobayes'
	ObjectContainer.art       = R("logo-On-nest-pas-que-des-cobayes-600x340.jpg")


#Root categories
def ListeCategories():
	oc = ObjectContainer(replace_parent=True)

        url="http://gdata.youtube.com/feeds/api/playlists/PLEY1NNPhwXGWnd8uNPY3RVHPyNDlXnOwo/?alt=json&max-results=50"
        oc.add( DirectoryObject(key=Callback(Video,url=url),title="Emissions",thumb=R('icon-videos.png')))

        url="http://gdata.youtube.com/feeds/api/playlists/PLEY1NNPhwXGXqZCIg4bWqUH_dbYbecNPO/?alt=json&max-results=50"
        oc.add( DirectoryObject(key=Callback(Video,url=url),title="Defis",thumb=R('icon-channels.png')))

        Log(oc) 

#        oc.add(dd)
	return oc

def Video(url):
    data=JSON.ObjectFromURL(url)
    oc=ObjectContainer()
    for a in data['feed']['entry']:
        url=a['link'][0]['href']
        title=a['title']['$t']
        summary=a['content']['$t']
        thumb=a['media$group']['media$thumbnail'][0]['url']
        dd=MovieObject(url=url,title=title,summary=summary,thumb=thumb)
        oc.add(dd)
    return oc


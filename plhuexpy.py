import cherrypy

cherrypy.config.update({'server.socket_port': 38148,
                       })

class PlexHandler(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def plexjson(self):
        payload = cherrypy.request.json
        print payload
        return "Fucking A Man!"


if __name__ == '__main__':
    cherrypy.quickstart(PlexHandler())
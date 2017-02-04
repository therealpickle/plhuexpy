import cherrypy

cherrypy.config.update({'server.socket_port': 38148,
                        #'tools.json_in.force': False,
                        #'tools.encode.encoding': "utf-8",
                        'tools.json_in.on': True,
                       })

class PlexHandler(object):
    @cherrypy.expose
    # @cherrypy.tools.json_in()
    # @cherrypy.tools.allow(methods=['POST'])
    def plexjson(self):
        print "###"
        # payload = cherrypy.request.json
        # print payload
        print "!!!"


    @cherrypy.expose
    def test(self):
        print "Test"
        return "Test"


if __name__ == '__main__':
    cherrypy.quickstart(PlexHandler())

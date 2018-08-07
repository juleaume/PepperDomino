

class MyClass(GeneratedClass):

    def onLoad(self):
        pass

    def onUnload(self):
        pass

    def _getTabletService(self):
        tabletService = None
        try:
            tabletService = self.session().service("ALTabletService")
        except Exception as e:
            self.logger.error(e)
        return tabletService

    def _getAbsoluteUrl(self, partial_url):
        import os
        subPath = os.path.join(self.packageUid(), os.path.normpath(partial_url).lstrip("\\/"))
        # We create TabletService here in order to avoid
        # problems with connections and disconnections of the tablet during the life of the application
        return "http://%s/apps/%s" %(self._getTabletService().robotIp(), subPath.replace(os.path.sep, "/"))

    def onInput_onStart(self, p):
        # We create TabletService here in order to avoid
        # problems with connections and disconnections of the tablet during the life of the application
        tabletService = self._getTabletService()
        if tabletService:
            try:
                url = p
                if url == '':
                    self.logger.error("URL of the image is empty")
                if not url.startswith('http'):
                    url = self._getAbsoluteUrl(url)
                tabletService.showImage(url)
            except Exception as err:
                self.logger.error("Error during ShowImage : %s " % err)
                self.onStopped()
        else:
            self.logger.warning("No ALTabletService, can't display the image.")
            self.onStopped()

    def onInput_onHideImage(self):
        # We create TabletService here in order to avoid
        # problems with connections and disconnections of the tablet during the life of the application
        tabletService = self._getTabletService()
        if tabletService:
            try:
                tabletService.hideImage()
            except Exception as err:
                self.logger.error("Error during HideImage : %s " % err)
                self.onStopped()
        else:
            self.logger.warning("No ALTabletService, can't hide the image.")
            self.onStopped()

    def onInput_onPreLoadImage(self):
        # We create TabletService here in order to avoid
        # problems with connections and disconnections of the tablet during the life of the application
        tabletService = self._getTabletService()
        if tabletService:
            try:
                partialUrl = self.getParameter("ImageUrl")
                fullUrl = self._getAbsoluteUrl(partialUrl)
                tabletService.preLoadImage(fullUrl)
            except Exception as err:
                self.logger.warning("Error during preLoadImage : %s " % err)
                self.onStopped()
        else:
            self.logger.warning("No ALTabletService, can't preload the image.")
            self.onStopped()

    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()

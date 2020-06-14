from core import plugin, model

class _api(plugin._plugin):
    version = 0.1

    def install(self):
        # Register models
        model.registerModel("api","_api","_action","plugins.api.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("api","_api","_action","plugins.api.models.action")
        return True

    
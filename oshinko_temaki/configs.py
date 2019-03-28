"""configuration objects"""
import uuid


class ClusterConfig():
    """a helper to contain the defaults"""
    def __init__(self, args):
        """convert a set of parsed arguments into a config."""
        self.set_parameter(
            "name", args, 'spark-{}'.format(uuid.uuid4().hex[-4:]))
        self.set_parameter("masters", args, 1)
        self.set_parameter("workers", args, 1)
        self.set_parameter("image", args, None)
        self.set_parameter("metrics", args, None)
        self.set_parameter("webui", args, None)
        self.set_parameter("configmap", args, None)
    
    def set_parameter(self, name, source, default):
        """set the named parameter or default if the value is None"""
        try:
            value = getattr(source, name)
        except AttributeError:
            value = None

        if value is None:
            value = default
        setattr(self, name, value)

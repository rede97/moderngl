import logging

from moderngl.mgl import InvalidObject  # type: ignore

__all__ = ['Scope']

LOG = logging.getLogger(__name__)


class Scope:
    '''
        This class represents a Scope object.

        Responsibilities on enter:

        - Set the enable flags.
        - Bind the framebuffer.
        - Assigning textures to texture locations.
        - Assigning buffers to uniform buffers.
        - Assigning buffers to shader storage buffers.

        Responsibilities on exit:

        - Restore the enable flags.
        - Restore the framebuffer.
    '''

    __slots__ = ['mglo', 'ctx', '_framebuffer', '_textures', '_uniform_buffers', '_storage_buffers', '_samplers', 'extra']

    def __init__(self):
        self.mglo = None  #: Internal representation for debug purposes only.
        self.ctx = None  #: The context this object belongs to
        # Keep references to keep this objects alive
        self._framebuffer = None
        self._textures = None
        self._uniform_buffers = None
        self._storage_buffers = None
        self._samplers = None
        self.extra = None  #: Any - Attribute for storing user defined objects
        raise TypeError()

    def __repr__(self):
        return '<Scope>'

    def __hash__(self) -> int:
        return id(self)

    def __enter__(self):
        self.mglo.begin()
        return self

    def __exit__(self, *args):
        self.mglo.end()

    def __del__(self):
        LOG.debug(f"{self.__class__.__name__}.__del__ {self}")
        if hasattr(self, "ctx") and self.ctx.gc_mode == "auto":
            self.release()

    def release(self):
        LOG.debug(f"{self.__class__.__name__}.release() {self}")
        if not isinstance(self.mglo, InvalidObject):
            self._framebuffer = None
            self._textures = None
            self._uniform_buffers = None
            self._storage_buffers = None
            self._samplers = None
            self.mglo.release()

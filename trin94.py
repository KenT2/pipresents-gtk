# with many thanks to trin94
# https://github.com/trin94/python-mpv-gtk4

# MIT
#
# Copyright (c) 2022
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import ctypes
import sys

import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
from OpenGL import GL
from mpv import MPV, MpvGlGetProcAddressFn, MpvRenderContext


class MyApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='org.example.App')
        self.renderer = MyRenderer()
        self.renderer.connect("realize", self.on_renderer_ready)

    def on_renderer_ready(self, *_):
        self.renderer.play('//home/pp/pp_home/media/suits-short.mkv')

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Gtk.ApplicationWindow(application=self)
            win.set_default_size(1280, 720)
            win.set_child(self.renderer)
        win.present()


class MyRenderer(Gtk.GLArea):

    def __init__(self, **properties):
        super().__init__(**properties)
        self.set_auto_render(False)
        self.connect("realize", self.on_realize)
        #krt
        self._mpv = MPV(vo="libmpv")
        self._ctx = None
        self._ctx_opengl_params = {'get_proc_address': MpvGlGetProcAddressFn(GetProcAddressGetter().wrap)}

    def on_realize(self, *_):
        self.make_current()
        self._ctx = MpvRenderContext(self._mpv, 'opengl', opengl_init_params=self._ctx_opengl_params)
        self._ctx.update_cb = self.on_mpv_callback

    def on_mpv_callback(self):
        GLib.idle_add(self.call_frame_ready, None, GLib.PRIORITY_HIGH)

    def call_frame_ready(self, *_):
        if self._ctx.update():
            self.queue_render()

    def do_render(self, *_):
        if not self._ctx:
            return False

        factor = self.get_scale_factor()
        width = self.get_allocated_width() * factor
        height = self.get_allocated_height() * factor
        #print(factor,width,height)
        fbo = GL.glGetIntegerv(GL.GL_DRAW_FRAMEBUFFER_BINDING)
        self._ctx.render(
            flip_y=True,
            opengl_fbo={'w': width, 'h': height, 'fbo': fbo}
        )
        
    def get_player(self):
        return self._mpv

    def play(self, file):
        self._mpv.play(file)
        return self._mpv

    def close(self):
        self._mpv.stop()
        self._mpv.terminate()

class GetProcAddressGetter:

    def __init__(self):
        self._func = self._find_platform_wrapper()

    def _find_platform_wrapper(self):
        return self._init_linux()

    def _init_linux(self):
        try:
            from OpenGL import GLX
            return self._glx_impl
        except AttributeError:
            pass
        try:
            from OpenGL import EGL
            return self._egl_impl
        except AttributeError:
            pass
        raise 'Cannot initialize OpenGL'

    def wrap(self, _, name: bytes):
        address = self._func(name)
        return ctypes.cast(address, ctypes.c_void_p).value

    @staticmethod
    def _glx_impl(name: bytes):
        from OpenGL import GLX
        return GLX.glXGetProcAddress(name.decode("utf-8"))

    @staticmethod
    def _egl_impl(name: bytes):
        from OpenGL import EGL
        return EGL.eglGetProcAddress(name.decode("utf-8"))


if __name__ == '__main__':
    sys.exit(MyApplication().run(sys.argv))

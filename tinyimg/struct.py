from ctypes import (Structure, c_int, c_char, c_char_p, c_size_t, c_ssize_t,
                    c_double, c_ushort, c_void_p, c_ubyte, CFUNCTYPE, POINTER)

def group(labels, type):
    return zip(labels, [type] * len(labels))

enum = c_int

MaxText = c_char * 4096

Compression = enum
Orientation = enum
MagickBoolean = enum
Interlace = enum
Endian = enum
Resolution = enum
Colorspace = enum
ImageType = enum
PreviewType = enum
Channel = enum
VirtualPixelMethod = enum
Class = enum
RenderingIntent = enum
Filter = enum
Gravity = enum
CompositeOperator = enum
DisposeType = enum
InterpolatePixelMethod = enum
PixelChannel = enum
PixelTrait = enum
TimerState = enum
StreamType = enum

Quantum = c_ushort

class PixelPacket(Structure):
    _fields_ = (group(('red', 'green', 'blue', 'alpha', 'black', 'index'), Quantum) +
                [('count', c_size_t)])

class PrimaryInfo(Structure):
    _fields_ = group(('x', 'y', 'z'), c_double)

class ChromacityInfo(Structure):
    _fields_ = group(('red_primary', 'green_primary', 'blue_primary', 'white_point'), PrimaryInfo)

class RectangleInfo(Structure):
    _fields_ = group(('width', 'height'), c_size_t) + group(('x', 'y'), c_ssize_t)

class PixelChannelMap(Structure):
    _fields_ = [('channel', PixelChannel), ('traits', PixelTrait)]

class ErrorInfo(Structure):
    _fields_ = group(('mean', 'normalized_mean', 'normalized_max'), c_double)

class Timer(Structure):
    _fields_ = group(('start', 'stop', 'total'), c_double)

class TimerInfo(Structure):
    _fields_ = (group(('user', 'elapsed'), Timer) +
                [('state', TimerState), ('signature', c_size_t)])
    
class Ascii85Info(Structure):
    _fields_ = group(('offset', 'line_break'), c_ssize_t) + [('buffer', c_ubyte * 10)]
    
class ProfileInfo(Structure):
    _fields_ = [('name', c_char_p), ('length', c_size_t),
                ('info', POINTER(c_ubyte)), ('signature', c_size_t)]
    
class BlobInfo(Structure):
    _fields_ = (group(('length', 'extent', 'quantum'), c_size_t) +
                group(('mapped', 'eof'), MagickBoolean) +
                [('offset', c_ssize_t), ('size', c_size_t)] +
                group(('exempt', 'synchronize', 'status', 'temporary'), MagickBoolean) +
                [('type', StreamType), ('file', c_void_p)])
                
MagickProgressMonitor = CFUNCTYPE(MagickBoolean, c_char_p, c_ssize_t, c_size_t, c_void_p)

class Image(Structure): pass

Image._fields_ = ([('storage_class', Class), ('colorspace', Colorspace),
                   ('compression', Compression), ('quality', c_size_t),
                   ('orientation', Orientation)] +
                  group(('taint', 'matte'), MagickBoolean) +
                  group(('columns', 'rows', 'depth', 'colors'), c_size_t) +
                  [('colormap', POINTER(PixelPacket))] +
                  group(('background_color', 'border_color', 'matte_color'), PixelPacket) +
                  [('gamma', c_double), ('chromacity', ChromacityInfo),
                   ('rendering_intent', RenderingIntent), ('profiles', c_void_p)
                   ('units', Resolution)] +
                  group(('montage', 'directory', 'geometry'), c_char_p) +
                  [('offset', c_ssize_t)] +
                  group(('x_resolution', 'y_resolution'), c_double) +
                  group(('page', 'extract_info'), RectangleInfo) +
                  group(('bias', 'blur', 'fuzz'), c_double) +
                  [('filter', Filter), ('interlace', Interlace), ('endian', Endian),
                   ('gravity', Gravity), ('compose', CompositeOperator), ('dispose', DisposeType),
                   ('clip_mask', POINTER(Image))] +
                  group(('scene', 'delay'), c_size_t) +
                  [('ticks_per_second', c_size_t)] +
                  group(('iterations', 'total_colors', c_size_t)) +
                  [('start_loop', c_ssize_t), ('interpolate', InterpolatePixelMethod),
                   ('black_point_compensation', MagickBoolean),
                   ('transparent_color', PixelPacket),
                   ('mask', POINTER(Image)), ('tile_offset', RectangleInfo)] +
                  group(('properties', 'artifacts'), c_void_p) +
                  [('type', ImageType), ('dither', MagickBoolean), ('extent', c_size_t),
                   ('ping', MagickBoolean)] +
                  group(('number_channels', 'number_meta_channels', 'metacontent_extent'), c_size_t) +
                  [('sync', MagickBoolean), ('channel_mask', Channel),
                   ('channel_map', PixelChannelMap), ('cache', c_void_p),
                   ('error', ErrorInfo), ('timer', TimerInfo),
                   ('progress_monitor', MagickProgressMonitor), ('client_data', c_void_p),
                   ('ascii85', Ascii85Info)] +
                  group(('color_profile', 'iptc_profile'), ProfileInfo) +
                  [('generic_profile', POINTER(ProfileInfo))] +
                  group(('filename', 'magick_filename', 'magick'), MaxText) +
                  group(('magick_columns', 'magick_rows'), c_size_t))
                  
    


# StreamHandler = CFUNCTYPE()

class ImageInfo(Structure):
    _fields_ = ([('compression', Compression), ('orientation', Orientation)] +
                group(('temporary', 'adjoin', 'affirm', 'antialias'), MagickBoolean) +
                group(('size', 'extract', 'page', 'scenes'), c_char_p) +
                group(('scene', 'number_scenes', 'depth'), c_size_t) +
                [('interlace', Interlace), ('endian', Endian),
                 ('units', Resolution), ('quality', c_size_t)] +
                group(('sampling_factor', 'server_name', 'font', 'texture', 'density'), c_char_p) +
                group(('pointsize', 'fuzz'), c_double) +
                group(('background_color', 'border_color', 'matte_color'), PixelPacket) +
                group(('dither', 'monochrome'), MagickBoolean) +
                [('colors', c_size_t), ('colorspace', Colorspace), ('type', ImageType),
                 ('preview_type', PreviewType), ('group', c_ssize_t)] +
                group(('ping', 'verbose'), MagickBoolean) +
                group(('view', 'authenticate'), c_char_p) +
                [('channel', Channel), ('options', c_void_p),
                 ('virtual_pixel_method', VirtualPixelMethod)
                 ('profile', c_void_p), ('synchronize', MagickBoolean),
                 ('progress_monitor', MagickProgressMonitor)] +
                group(('client_data', 'cache'), c_void_p) +
                [('stream', c_void_p)] + # should be StreamHandler func poineter
                [('file', c_void_p)] + # should be FILE*
                [('blob', c_void_p), ('length', c_size_t)] +
                group(('magick', 'unique', 'zero', 'filename'), MaxText) +
                [('debug', MagickBoolean)] +
                [('signature', c_size_t)])
                
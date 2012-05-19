# coding: utf-8
# pystacia/image/_impl/blur.py
# Copyright (C) 2011-2012 by Paweł Piotr Przeradowski
#
# This module is part of Pystacia and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php


def blur(image, radius, strength):
    if strength == None:
        strength = radius
    
    c_call(image, 'blur', radius, strength)


def gaussian_blur(image, radius, strength, bias):
    if strength == None:
        strength = radius
    
    if bias == None:
        bias = 0
    
    c_call(image, 'gaussian_blur', radius, strength, bias)


def motion_blur(image, radius, angle, strength, bias):
    if strength == None:
        strength = radius
    
    if bias == None:
        bias = 0
    
    c_call(image, 'motion_blur', radius, strength, angle, bias)


def adaptive_blur(image, radius, strength, bias):
    if strength == None:
        strength = radius
    if bias == None:
        bias = 0
        
    c_call(image, 'adaptive_blur', radius, strength, bias)


def sharpen(image, radius, strength, bias):
    if strength == None:
        strength = radius
    if bias == None:
        bias = 0
        
    c_call(image, 'sharpen', radius, strength, bias)


def adaptive_sharpen(image, radius, strength, bias):
    if strength == None:
        strength = radius
    if bias == None:
        bias = 0
        
    c_call(image, 'adaptive_sharpen', radius, strength, bias)


def detect_edges(image, radius, strength):
    if strength == None:
        strength = radius
    
    c_call(image, 'edge', radius, strength)


#TODO: moving center here
def radial_blur(image, angle):
    """Performs radial blur.
    
       :param angle: Blur angle in degrees
       :type angle: ``float``
       
       Radial blurs image within given angle.
       
       This method can be chained.
    """
    c_call(image, 'radial_blur', angle)


def denoise(image):
    """Attempt to remove noise preserving edges.
    
       Applies a digital filter that improves the quality of a
       noisy image.
       
       This method can be chained.
    """
    c_call(image, 'enhance')


def despeckle(image):
    """Attempt to remove speckle preserving edges.
       
       Resulting image almost solid color areas are smoothed preserving
       edges.
       
       This method can be chained.
    """
    c_call(image, 'despeckle')


def emboss(image, radius, strength):
    """Apply edge detecting algorithm.
       
       :param radius: filter radius
       :type radius: ``int``
       :param stregth: filter strength (sigma)
       :type strength: ``int``
       
       On a typical photo creates effect of raised edges.
       
       This method can be chained.
    """
    if strength == None:
        strength = radius
    
    c_call(image, 'emboss', radius, strength)


from pystacia.api.func import c_call

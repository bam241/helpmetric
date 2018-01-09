#!/usr/bin/env python


def FracAtom2Mass(atom):
    uma_235 = 235043928.190
    uma_238 = 238050786.996
    u235_atom = atom
    u238_atom = 1 - atom
    u235_mass = u235_atom * uma_235
    u238_mass = u238_atom * uma_238
    return u235_mass / (u235_mass + u238_mass)


def FracMass2Atom(mass):
    uma_235 = 235043928.190
    uma_238 = 238050786.996
    u235_mass = mass
    u238_mass = 1 - mass
    u235_atom = u235_mass / uma_235
    u238_atom = u238_mass / uma_238
    return u235_atom / (u235_atom + u238_atom)

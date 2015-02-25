#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Dos Santos Julien'
from models import User
def serialiseur_perso(obj):

    # Si c'est une musique.
    if isinstance(obj, User):
        return {"identifiant":obj.id,
                "name": obj.name,
                "firstname": obj.firstname,
                "mail":obj.mail,
                "promotion":obj.promotion_id,
                "updated":obj.updated }

    # Sinon le type de l'objet est inconnu, on lance une exception.
    raise TypeError(repr(obj) + " n'est pas sérialisable !")
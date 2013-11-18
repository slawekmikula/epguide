# -*- coding: utf-8 -*-
# 
# plik definiujacy obiekty dostarczające dane


from util import to_string

class Channel(object):
    """
    definicja kanalu
    """
    def __init__(self, id="", name="", icon_url=None):
        self.id = id
        self.name = name
        self.icon_url = icon_url

    def __hash__(self):
        return hash(self.id)

    def __cmp__(self, other):
        return cmp(self.id, other.id)
    
    def __str__(self):
        return "Channel(id:" + to_string(self.id) + ",name:" + to_string(self.name) +  ",icon_url:" + to_string(self.icon_url)+ ")"

class Event(object):
    """
    wydarzenie (program w telewizji), zawiera dane zakodowane w unicode
    """
    def __hash__(self):
        raise NotImplementedError( "Should have implemented this" )

    def __cmp__(self, other):
        return (self.channel_id() + self.time_start) - (other.channel_id() + other.time_start)

    def __str__(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def get_title(self):
        raise NotImplementedError( "Should have implemented this" )
        
    def get_description(self):
        raise NotImplementedError( "Should have implemented this" )

    def get_year(self):
        raise NotImplementedError( "Should have implemented this" )

    def get_icon_url(self):
        raise NotImplementedError( "Should have implemented this" )
        
    def get_country(self):
        raise NotImplementedError( "Should have implemented this" )

    def get_pg(self):
        raise NotImplementedError( "Should have implemented this" )

    def get_star_rating(self):
        raise NotImplementedError( "Should have implemented this" )

    def get_channel_id(self):
        raise NotImplementedError( "Should have implemented this" )

class Imdb(object):
    def __init__(self, url, rank):
        self.url = url
        self.rank = rank
        
    def __str__(self):
        return "Imdb(url:" + to_string(self.url) + ",rank:" + to_string(self.rank) + ")" 

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.url == other.url
            and self.rank == other.rank)
        
class ParentalRating(object):
    def __init__(self, desc, min_age):
        self.desc = desc
        self.min_age = min_age
        
    def __str__(self):
        return "ParentalRating(desc:" + to_string(self.desc)+ ",min_age:" + to_string(self.min_age) + ")" 

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.desc == other.desc
            and self.min_age == other.min_age)

class ParserOptions(object):
    def __init__(self, split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 99):
        self.split_title = split_title
        self.add_original_title_to_title = add_original_title_to_title
        self.add_year_to_title = add_year_to_title
        self.add_age_rating_to_title = add_age_rating_to_title

    def split_title(self):
        self.split_title
        
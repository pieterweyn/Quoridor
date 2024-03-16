#-----------------------------------#
#                                   #
#   filename: lib_quatornion        #
#   author: Ward Stoorvogel         #
#                                   #
#-----------------------------------#
#                                   #
#   description: file to generate   #
#       special quatornions for     #
#       reflections and projections #
#       Multiplying and divide      #
#       quatornions                 #
#                                   #
#-----------------------------------#

rules = (3,0,0)


def initialise(a: int, b: int, c: int):
    rules = (a, b, c)


def multiply(a: tuple, b: tuple):
    pass
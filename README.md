# Satellite-Aerial-Image-Retrieval

# Generate automatic aerial imagery given a Latitude, Longitude bounding box using Bing Maps Tile System
The algorithm uses Bing Tile System with the utility functions provided in bing_utilities.py to generate tiles.

An improved quality tile is overwritten on the previous image if found.

An initial image is created.

The starting point is chosen as the image with the highest resolution and the tile has at least one side.

The resolution is increased and iterated through the generated tiles  which are acquired from Bing Server.

The tile with the better resolution among those is attached to the initial image.

This process is carried out unless and until  Bing Server responds with null i.e. there is no better quality available.

Test Input Co-ordinates:

[![1.png](https://s23.postimg.org/twrhsu4l7/image.png)](https://postimg.org/image/6vawn34xj/)

Output:

[![2.jpg](https://s29.postimg.org/jeuvrqd5z/image.jpg)](https://postimg.org/image/u1oox5lb7/)

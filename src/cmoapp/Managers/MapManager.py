#!/usr/bin/python

#import other class

class MapManager:
	'Common base class for Map'
	mapID = 0
	data = []

	def __init__(self, mapID):
      self.mapID = mapID
	  
	def __del__(self):
      class_name = self.__class__.__name__
      print (class_name, "destroyed")
   
	def __str__(self):
      return 'mapID View (%d, %d)' % (self.mapID)
	 

	def loadMap(request,Location)
		latest_location_list = Location.objects.order_by('-crisis')[:5]
		context = {'latest_location_list': latest_location_list}
		
		try:
			forLocation = request.POST['Location']
		except(KeyError, Location.DoesNotExist):
			 # Redisplay
			return render(request, 'chief/base_site.html', {
				context,
				'error_message': "You didn't select a Location.",
			})
		else:
			return HttpResponseRedirect(reverse('cmoapp:base_site', args=(crisis.id,)))

			
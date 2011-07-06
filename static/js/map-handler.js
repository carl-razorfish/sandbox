RIA.MapHandler = {
	init: function() {
		document.getElements(".show-map").each(function(mapLink) {  

			mapLink.addEvents({
				"click": function(e) {
					e.preventDefault();
					var map = mapLink.getParent("dl").getElement(".map img"), size = map.getSize();
					map.getStyle("opacity") > 0 ? map.morph({"opacity":0, "height":"0px"}) : map.morph({"opacity":1, "height":"150px"});
				}
			})
		});  
	}
}
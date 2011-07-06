RIA.AjaxSubmit = new Class({
	Implements:[Options],
	options:{

	},
	initialize: function(options) {
		this.setOptions(options);
		this.content = document.id("content");
		this.ajaxForm = document.id("controls");
		this.destination = document.id("destination");
		this.addEventListeners();
	},
	addEventListeners: function() {
		this.ajaxForm.addEvents({
			"submit": function(e) {
				e.preventDefault();
				if(this.destination.get("value") != "") {
					this.requestData(this.destination.get("value"));
				}				
			}.bind(this)
		});
		this.destination.addEvents({
			"change": function(e) {
				e.preventDefault();
				if(this.destination.get("value") != "") {
					this.requestData(this.destination.get("value"));
				}				
			}.bind(this)
		});
	},
	requestData: function(destination) {  
		this.request = new Request.HTML({
			method:"POST",
			url:"/ajax",
			update:document.id("content"),
			onSuccess: this.requestSuccess.bind(this),
			onFailure: this.requestFailure.bind(this)
		}).send('destination='+destination);
	},
	requestSuccess: function(responseHTML, responseText) {
		Log.info("requestSuccess");
	},
	requestFailure: function(e) {
		Log.error({method:"requestFailure", error:e});
	}
});
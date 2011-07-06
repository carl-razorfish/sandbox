RIA.AjaxSubmit = new Class({
	Implements:[Options],
	options:{

	},
	initialize: function(options) {
		this.setOptions(options);
		this.content = document.id("content");
		this.tempContent = document.id("temp-content");
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
		this.tempContent = new Element("div", {"class":"temp-content"}).inject(document.body);
		this.request = new Request.HTML({
			method:"POST",
			url:"/ajax",
			update:this.tempContent,
			onRequest: this.requestStart.bind(this),
			onSuccess: this.requestSuccess.bind(this),
			onFailure: this.requestFailure.bind(this)
		}).send('destination='+destination);
	},
	requestStart: function() {
		this.content.setStyle("background", "#fff url(static/img/ajax-loader.gif) no-repeat 47% 45%");
		this.content.getFirst().morph({"opacity":0});
	},
	requestSuccess: function(responseHTML, responseText) {
		Log.info("requestSuccess");
        this.content.empty();
		this.tempContent.inject(this.content).set({
			"styles":{
				"position":"static"
			}
		}).morph({"opacity":1});
		this.content.setStyle("background", "#fff"); 
		
		RIA.MapHandler.init();
	},
	requestFailure: function(e) {
		Log.error({method:"requestFailure", error:e});
	}
});
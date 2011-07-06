var Log = {
	info: function(msg) {
		if(window.console && console.log && msg) console.log(msg);
	},
	error: function(errorObject) {
		/* 
		* 	errorObject : {
		* 		method[String]: "MyClass : myFunction()" (example) string to help you identify which js file and function caused the error
		* 		error:[Object]: the error object
		* 	}
		*/
		if (errorObject.error instanceof TypeError) {
			this.info("JS ERROR : "+(errorObject.method||'Unknown method')+" : TypeError; the type of a variable is not as expected : "+(errorObject.error.message||errorObject.error));
		} else if (errorObject.error instanceof RangeError) {
			this.info("JS ERROR : "+(errorObject.method||'Unknown method')+" : RangeError; numeric variable has exceeded its allowed range : "+(errorObject.error.message||errorObject.error));
		} else if (errorObject.error instanceof SyntaxError) {
			this.info("JS ERROR : "+(errorObject.method||'Unknown method')+" : SyntaxError; syntax error occurred while parsing : "+(errorObject.error.message||errorObject.error));
		} else if (errorObject.error instanceof ReferenceError) {
			this.info("JS ERROR : "+(errorObject.method||'Unknown method')+" : ReferenceError; invalid reference used : "+(errorObject.error.message||errorObject.error));
		} else {
			this.info("JS ERROR : "+(errorObject.method||'Unknown method')+" : Unidentified Error Type : "+(errorObject.error.message||errorObject.error));
		}
	}
};
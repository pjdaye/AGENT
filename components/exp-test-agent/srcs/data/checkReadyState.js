function isDOMLoaded() {
    return document.readyState == 'complete';
}

(function (callback) {
	if($.active > 0) {
    	$(document).ajaxStop(function() {
        	callback(isDOMLoaded());
    	});
	}
	else {
		callback(isDOMLoaded());
	}
})(arguments[arguments.length - 1]);
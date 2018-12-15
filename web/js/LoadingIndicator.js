function LoadingIndicator() {
	var loadingIndicatorTimer;

	if (top.document.getElementById("loading-indicator-modal-dialog") === null) {
		var jnlpFrameElem = document.createElement('div');
		jnlpFrameElem.innerHTML =
			'<div id="loading-indicator-modal-dialog" style="position: absolute; width: 100%; height: 100%; left: 0; top: 0; display: none; ">\n' +
			'\t<div style="position: absolute; z-index: 1001; width: 100%; height: 100%; left: 0; top: 0; background: gray; opacity: 0.5;"></div>\n' +
			'\t<img src="img/loading.gif" style="position: absolute; width: 32px; height: 32px; left: calc(50% - 16px); top: calc(50% - 16px);">\n' +
			'</div>';
		top.document.body.appendChild(jnlpFrameElem);
	}

	$(document).bind("ajaxSend", function () {
		loadingIndicatorTimer && clearTimeout(loadingIndicatorTimer);
		loadingIndicatorTimer = setTimeout(function () {
				$('#loading-indicator-modal-dialog').show();
				console.debug("ajax start");
			},
			1000);
	}).bind("ajaxComplete", function () {
		clearTimeout(loadingIndicatorTimer);
		$('#loading-indicator-modal-dialog').hide();
		console.debug("ajax stop");
	});
}




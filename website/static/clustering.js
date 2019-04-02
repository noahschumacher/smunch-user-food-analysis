
$(document).ready(function(){
	console.log('Document is ready')

	// Button config for Rendering Cluster DataFrame
	$("#renderClusters").click(async function(){
		console.log('button was clicked')

		const n_clusters = parseFloat($('#cluster_n').val());
		const data = {n_clusters}

		console.log(data)


		const response = await $.ajax('/renderClusters', {
			data: JSON.stringify(data),
			method: "post",
			contentType:'application/json'
		})

		console.log(response)
		$('#cluster_table').val(response.n)

	})

})









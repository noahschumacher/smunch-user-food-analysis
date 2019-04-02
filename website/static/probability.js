
$(document).ready(function(){
	console.log('Document is ready')

	// Button config for Rendering Cluster DataFrame
	$("#probOrder").click(async function(){
		console.log('button was clicked')

		const user_id = parseString($('#user_id').val());
		const account_id = parseString($('#account_id').val());

		const data = {user_id, account_id}

		console.log(data)


		const response = await $.ajax('/probOrder', {
			data: JSON.stringify(data),
			method: "post",
			contentType:'application/json'
		})

		console.log(response)
		$('#probabilty').val(response.n)

	})

})









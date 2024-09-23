function handleReply(id){
    //var title = `#titlex-${clicked_id}`
    const aas = `reply-form-container-${id}`;
    document.getElementById(aas).style.display = "block";
   console.log(aas);
}

function handleCancel(id){
    //var title = `#titlex-${clicked_id}`
    const aas = `reply-form-container-${id}`;
    document.getElementById(aas).style.display = "None";
   console.log(aas);
}




function buttonInput() {
    
    var userText = $('#textInput').val();
    var userHTML = "<p class='userText'> User: <span>"+userText+"</span></p>";
    $('#textInput').val("");

    $('#chatbot').append(userHTML);

    $.get('/getChat',{userMessage:userText}).done(function(data){
        var returnMessage = "<p class='botText'>Chatbot: <span>"+data+"</span></p>";
        $('#chatbot').append(returnMessage);
    })
  } 

  
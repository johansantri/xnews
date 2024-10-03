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



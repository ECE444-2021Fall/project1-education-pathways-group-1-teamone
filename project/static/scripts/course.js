var voteCount = {};

function toggleText(x){
    if(x.innerHTML == "Read More"){
        let tagDes = document.getElementsByClassName("many-text")[0];
        tagDes.classList.remove("many-text");
        tagDes.classList.add("all-text");
        x.innerHTML = "Collapse";
    } 
    else{
        let tagDes = document.getElementsByClassName("all-text")[0];
        tagDes.classList.remove("all-text");
        tagDes.classList.add("many-text");
        x.innerHTML = "Read More";
    }


}

async function upgradeVote(tagVote, code, postID){
    let action = tagVote.alt;
    if(voteCount[postID]){
        if(action == 'UpvoteComment' && voteCount[postID] >= 1){
            alert("You can't upvote this comment more than once!")
            return
        }
        else if(action == 'DownvoteComment' && voteCount[postID] <= -1){
            alert("You can't downvote this comment more than once!")
            return
        }
    }
    await fetch('/upgrade_vote', {
        method: 'POST',
        body: JSON.stringify({
            "action": action,
            "courseID": code,
            "PostID": postID
        }), 
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response =>{ 
        if(!response.ok){
            alert("Update Comment Failed");
            throw response.statusText;
        }
        return response.json(); 
    })
    
    if(action == 'UpvoteComment'){
        let tagCount = tagVote.nextElementSibling;
        voteCount[postID] = (voteCount[postID] || 0) + 1;
        tagCount.innerHTML = String(Number(tagCount.innerHTML)+1);
    }
    else{
        let tagCount = tagVote.previousElementSibling;
        voteCount[postID] = (voteCount[postID] || 0) - 1;
        tagCount.innerHTML = String(Number(tagCount.innerHTML)-1);
    }
}



function countLines(ele) {
  var styles = window.getComputedStyle(ele, null);
  var lh = parseInt(styles.lineHeight, 10);
  var h = parseInt(styles.height, 10);
  var lc = Math.round(h / lh);
  return lc;
}

var tagManyText = document.getElementsByClassName("many-text")[0];
var desLc =  countLines(tagManyText);
if(desLc <= 2){
    var btnToggleText = document.getElementsByClassName("toggle-text")[0];
    btnToggleText.remove();
}
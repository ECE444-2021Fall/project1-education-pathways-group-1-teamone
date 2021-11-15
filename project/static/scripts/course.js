var voteCount = 0;

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
    if(action == 'UpvoteComment' && voteCount >= 1){
        alert("You can't upvote a comment more than once!")
        return
    }
    if(action == 'DownvoteComment' && voteCount <= -1){
        alert("You can't downvote a comment more than once!")
        return
    }

    await fetch('http://onecourse.herokuapp.com/upgrade_vote', {
    method: 'POST',
    body: JSON.stringify({
        "action": action,
        "courseID": code,
        "PostID": postID
    }), 
    headers: {
        'Content-Type': 'application/json',
    },
    }).then(response => response.json())
    .catch(error => console.log(error));
    if(action == 'UpvoteComment'){
        let tagCount = tagVote.nextElementSibling;
        voteCount += 1;
        tagCount.innerHTML = String(Number(tagCount.innerHTML)+1);
    }
    else{
        let tagCount = tagVote.previousElementSibling;
        voteCount -= 1;
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
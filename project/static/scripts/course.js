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

function toggleHeartColor(tag_heart, code, postID){
    var action = "UpvoteComment"
    var tag_count = tag_heart.nextElementSibling;
    if(tag_heart.style.color == 'red'){
        tag_heart.style.color = 'black';
        action = "DownvoteComment";
        tag_count.innerHTML = String(Number(tag_count.innerHTML)-1);
    }
    else{
        tag_heart.style.color = 'red';
        action = "UpvoteComment";
         tag_count.innerHTML = String(Number(tag_count.innerHTML)+1);
    }
    fetch('http://localhost:5000/upgrade_vote', {
        method: 'POST',
        body: JSON.stringify({
            "action": action,
            "courseID": code,
            "PostID": postID
        }), 
        headers: {
            'Content-Type': 'application/json',
            // "Access-Control-Allow-Methods": "GET",
            // "Access-Control-Allow-Headers": "Content-Type"
        },
    }).then(response => response.json())
    .catch(error => console.log(error));

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
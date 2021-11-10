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
    .then(data => {
        console.log(data)
    });

}


function countLines(ele) {
  var styles = window.getComputedStyle(ele, null);
  var lh = parseInt(styles.lineHeight, 10);
  var h = parseInt(styles.height, 10);
  var lc = Math.round(h / lh);
  console.log('line count:', lc, 'line-height:', lh, 'height:', h);
  return lc;
}
var tagManyText = document.getElementsByClassName("many-text")[0];
var desLc =  countLines(tagManyText);
if(desLc <= 2){
    var btnToggleText = document.getElementsByClassName("toggle-text")[0];
    btnToggleText.remove();
}

// function buildTable(course){
//     var table = document.getElementById("courseInfo");
//     i = 0;
//     for(var key in course){
//         if(i >= 6){
//             return;
//         }
//         var content = course[key]
//         if(content != null && content.length > 0){
//             var row = `<tr> 
//                 <td class="col-2"><h5>${key}</h5></td>`
//             if(key == "Course Description"){   
//                 row += `<td class="col-8 description"> <p class="many-text">${course[key]}</p> 
//                         <span type="button" class="toggle-text" onclick="toggleText(this)">Read More</span></td></tr>`
//             }
//             else{
//                 row += `<td class="col-8 description">${course[key]}</td></tr>`
//             }
//             table.innerHTML += row;
//             i += 1;
//         }

//     }
// }
function popup(id){
    document.getElementById(id).style.display = "flex";
}

function off(e){
    e.parentNode.parentNode.style.display = "none";
}

function render_path(){

    var tag_paths =  document.getElementById("path_selection")
    var path = tag_paths.options[tag_paths.selectedIndex].text;
    var tbody = document.getElementById("path_courses");
    tbody.innerHTML = "";
    for(let course of paths_json[path]){
        let courseRef = `/course/${course["Code"]}`
        let row = `<tr id="">
                        <td class="align-middle col-2"><a href=${courseRef}>${course["Code"]}</a></td>
                        <td class="align-middle col-5">${course["Name"]}</td>
                        <td class="align-middle col-3">${course["Semester"]}</td>
                        <td class="align-middle text-center col-2"><button class="btn btn-secondary" onclick="drop_course(this)">drop</button></td>
                    </tr>`;
        tbody.innerHTML += row;
    }
}

async function drop_course(e){
    var courseCode = e.parentNode.parentNode.childNodes[1].innerText;
    var ePathChoice = document.getElementById("path_selection");
    var pathName = ePathChoice.options[ePathChoice.selectedIndex].text;   
    await fetch('/enroll/remove_course', {
        method: 'POST',
        body: JSON.stringify({
            "action": "RemoveCourse",
            "Username": username,
            "pathName": pathName,
            "courseCode": courseCode
        }), 
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if(!response.ok){
            alert("Drop Course Failed!");
            throw response.statusText;
        }
        return response.json();
    })
    e.parentNode.parentNode.remove();
}



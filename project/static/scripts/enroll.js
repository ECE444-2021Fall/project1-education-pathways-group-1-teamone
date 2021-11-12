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
        let row = `<tr id="">
                        <td class="align-middle col-2">${course["Code"]}</td>
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
    await fetch('http://localhost:5000/enroll/remove_course', {
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
    }
    ).then(response => response.json())
    .catch(error => console.log(error));
    e.parentNode.parentNode.remove();
}



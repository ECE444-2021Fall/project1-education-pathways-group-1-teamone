function popup(){
    document.querySelector('.bg-model').style.display = "flex";
}

function off(){
    document.querySelector('.bg-model').style.display = "none";
}

function render_table(){
    var tag_paths =  document.getElementById("paths")
    var path = tag_paths.options[tag_paths.selectedIndex].text;
    var tbody = document.getElementById("path_courses");
    tbody.innerHTML = "";
    for(let course of paths_json[path]){
        let row = `<tr>
                        <td class="align-middle col-2">${course["Code"]}</td>
                        <td class="align-middle col-5">${course["Name"]}</td>
                        <td class="align-middle col-3">${course["Semester"]}</td>
                        <td class="align-middle text-center col-2"><button class="btn btn-secondary">drop</button></td>
                    </tr>`;
        tbody.innerHTML += row;
    }
}

render_table()

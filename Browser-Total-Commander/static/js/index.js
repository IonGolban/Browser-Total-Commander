// <div id="jsonData" data-json="{{ jsonData | tojson }}"></div>


document.addEventListener('DOMContentLoaded', () => {
    const dataJsonString = document.getElementById('jsonData').getAttribute('data-json');
    const dataJson = JSON.parse(dataJsonString);
    console.log(dataJson);
    init_panels(dataJson);


});

function init_panels(data_json) {
    const main_dir = data_json.main_dir_name;
    const files_folders_paths = data_json.data;
    console.log(files_folders_paths);
    console.log(main_dir);
    for (var i = 0; i < files_folders_paths.length; i++) {
        const el_name = files_folders_paths[i];
        let li1 = document.createElement('li');
        let li2 = document.createElement('li');
        li1.setAttribute('class', 'list-group-item');
        li1.setAttribute('id', el_name + "1");
        li1.innerHTML = el_name;
        li2.setAttribute('class', 'list-group-item');
        li2.setAttribute('id', el_name + "2");
        li2.innerHTML = el_name;

        li1.addEventListener('click', click_element_handler);
        li2.addEventListener('click', click_element_handler);

        document.getElementById('files-folders-list-1').appendChild(li1);
        document.getElementById('files-folders-list-2').appendChild(li2);
    }

    document.getElementById('main-dir-name1').innerHTML = main_dir;
    document.getElementById('main-dir-name2').innerHTML = main_dir;
}

function click_element_handler(event) {
    const element = event.target;
    const element_id = element.getAttribute('id');
    const element_type = element.getAttribute('type');
    if (element_type === 'folder') {
        // get folder content
        get_folder_content(element_id);
    } else {
        // get file content
        get_file_content(element_id);
    }
}

// let copy_button = document.getElementById("copy-button")
// copy_button.addEventListener("click",() =>{
//     const folder_list = document.getElementById('files-folders-list-1')
//     folder_list.innerHTML = "";
// })

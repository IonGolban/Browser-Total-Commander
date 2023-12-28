// Realizati o pagina web care sa aiba backend-ul scris complet în Python, și care sa mimeze
// comportamentul unui tool similar cu Total Commander. Backend-ul va fi rulat pe masina
// curentă iar site-ul va fi accesat pe 127.0.0.1. Interfața web trebuie sa suporte următoarele
// funcții:
// ● Copiere fișiere / foldere (inclusiv selecție de fișiere/ foldere)
// ● Stergere fișiere / foldere (inclusiv selecție de fișiere/ foldere)
// ● Mutare/Redenumire fișiere / foldere (inclusiv selecție de fișiere/ foldere)
// ● Creare fisier
// ● Creare folder
// ● Editare fisiere text
// Interfața web va avea doua panel-uri în care se vizualizeaza fișiere și sub-folderele dintr-un
// folder (inclusiv cu informații despre dimensiunea fișierelor , respectiv date-time la care au fost
// create). Fiecare panel permite navigarea prin folderul curent, iar operatiile intre fisiere /
// foldere / etc se aplica intre cele doua panel-uri.

const url = 'http://localhost:5000/';

const rename_button = document.getElementById('rename-button');

document.addEventListener('DOMContentLoaded', () => {
    // const dataJsonString = document.getElementById('jsonData').getAttribute('data-json');
    // const dataJson = JSON.parse(dataJsonString);
    // // console.log(dataJson);
    // // init_panel(dataJson, 1);
    // // init_panel(dataJson, 2);

    console.log(jsonData)

    addClickListeners();

});

function init_panel(data_json, panel_id) {
    const main_dir = data_json.main_dir_name;
    const files_folders_data = data_json.data;

    let list = document.getElementById('files-folders-list-' + panel_id);
    list.innerHTML = "";
    list.setAttribute('path', main_dir)
    list.setAttribute('panel-id', panel_id)
    createListElements(list, files_folders_data);


    document.getElementById('main-dir-name' + panel_id).innerHTML = main_dir;

    addClickListeners();
}

function createListElements(list, elements) {
    for (var i = 0; i < elements.length; i++) {

        let li = create_li_element(elements[i], list)
        list.appendChild(li);
    }
}

function addClickListeners() {
    const listItems = document.querySelectorAll('.list-group-item');
    console.log("listItems = ", listItems);
    listItems.forEach((item) => {
        console.log(item.id)
        item.addEventListener('click', click_element_handler);
        item.addEventListener('dblclick', dbl_click_element_handler)
    });
}

function dbl_click_element_handler(event) {
    let clickedElement = event.target;
    if (clickedElement.tagName.toLowerCase() !== 'li') {
        clickedElement = clickedElement.closest('li.list-group-item');
    }
    // if(event.target.parentElement.className === '') {

    const el_id = clickedElement.id;
    console.log(el_id)
    console.log(el_id.substring(0, el_id.length - 2))
    const goto_dir_encoded = encodeURIComponent(el_id.substring(0, el_id.length - 2));
    console.log("encoded", goto_dir_encoded)
    const dir_name_1_encoded = encodeURIComponent(document.getElementById("main-dir-name1").innerHTML);
    const dir_name_2_encoded = encodeURIComponent(document.getElementById("main-dir-name2").innerHTML);
    const panel_changed_id = clickedElement.parentElement.parentElement.getAttribute('id')

// /goto/<panel_change>/<main_dir_1>/<main_dir_2>/<goto_dir>

    let go_to_url = url + 'goto/' + panel_changed_id + '/' + dir_name_1_encoded + '/' + dir_name_2_encoded + '/' + goto_dir_encoded;
    window.location.href = go_to_url;


}

function click_element_handler(event) {
    let clickedElement = event.target;

    const isCtrlPressed = event.ctrlKey || event.metaKey;

    if (clickedElement.tagName.toLowerCase() !== 'li') {
        clickedElement = clickedElement.closest('li.list-group-item');
    }


    if (!isCtrlPressed) {
        const selectedItems = document.querySelectorAll('.selected');
        console.log(selectedItems)
        selectedItems.forEach(item => {
            if (item !== clickedElement) {
                item.classList.remove('selected');
            }
        });
    }

    clickedElement.classList.toggle('selected');

    const clickedElementID = clickedElement.id;
    const isSelected = clickedElement.classList.contains('selected');

    console.log(`Element clicked: ${clickedElementID}, Selected: ${isSelected}`);
}

rename_button.addEventListener('click', () => {
    const selectedItems = document.querySelectorAll('.selected');
    if (selectedItems.length !== 1) {
        alert("Please select one item to rename")
        return;
    }

    let modal = document.getElementById('rename-modal');
    let old_name = selectedItems[0].id.substring(0, selectedItems[0].id.length - 2);
    let modal_old_name = document.getElementById('old-name-rename-modal');
    modal_old_name.innerHTML = "Old-name: " + old_name;

    modal.style.display = 'block';
});

document.getElementById('close-rename-modal').addEventListener('click', () => {
    let modal = document.getElementById('rename-modal');
    modal.style.display = 'none';
    console.log("close-rename-modal")
});

document.getElementById("confirm-rename-modal-button").addEventListener('click', () => {
    let new_name = document.getElementById('new-rename-modal').value;
    if (new_name === "") {
        alert("Please enter a new name")
        return;
    }

    const selectedItem = document.querySelectorAll('.selected')[0];
    let old_name = selectedItem.id.substring(0, selectedItem.id.length - 2);

    if (new_name === old_name) {
        alert("Please enter a new name")
        return;
    }
    // list-group-item
    let all_elements = document.querySelectorAll('.list-group-item');
    for (let element of all_elements) {
        if (element.parentElement.getAttribute('id') === selectedItem.parentElement.getAttribute('id')
        && element.id.substring(0, element.id.length - 2) === new_name) {
            alert("Name already exists")
            return;
        }
    }

    let main_dir_name = selectedItem.parentElement.getAttribute('path');

    let element_id = selectedItem.id;

    // @app.route('/rename/<main_dir_1>/<main_dir_2>/<old_name_path>/<new_name_path>', methods=["GET"])
    const dir_name_1_encoded = encodeURIComponent(document.getElementById("main-dir-name1").innerHTML);
    const dir_name_2_encoded = encodeURIComponent(document.getElementById("main-dir-name2").innerHTML);
    const old_name_encoded = encodeURIComponent(main_dir_name + "\\" + old_name);
    const new_name_encoded = encodeURIComponent(main_dir_name + "\\" + new_name);

    let rename_url = url + 'rename/' + dir_name_1_encoded + '/' + dir_name_2_encoded + '/' + old_name_encoded + '/' + new_name_encoded;

    window.location.href = rename_url;

});



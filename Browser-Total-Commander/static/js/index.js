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

document.addEventListener('DOMContentLoaded', () => {
    // const dataJsonString = document.getElementById('jsonData').getAttribute('data-json');
    // const dataJson = JSON.parse(dataJsonString);
    // // console.log(dataJson);
    // // init_panel(dataJson, 1);
    // // init_panel(dataJson, 2);

    addClickListeners();

});

function init_panel(data_json, panel_id) {
    const main_dir = data_json.main_dir_name;
    const files_folders_data = data_json.data;

    let list = document.getElementById('files-folders-list-'+panel_id);
    list.innerHTML = "";
    list.setAttribute('path', main_dir)
    list.setAttribute('panel-id', panel_id)
    createListElements(list, files_folders_data);



    document.getElementById('main-dir-name'+ panel_id).innerHTML = main_dir;

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
    listItems.forEach((item)  => {
        console.log(item.id)
        item.addEventListener('click', click_element_handler);
        item.addEventListener('dblclick', dbl_click_element_handler)
    });
}



function create_li_element(element, list) {
        let li = document.createElement('li');
        li.setAttribute('class', 'list-group-item');
        li.setAttribute('id', element.name + list.id.substring(18));
        li.setAttribute('data-type', element.type)



        let name = document.createElement('span');
        name.innerHTML = element.name;

        let img = document.createElement('img');
        img.setAttribute('src', "/static/img/" + element.type + ".png");

        let details = document.createElement('div')
        details.setAttribute('class', 'details')

        let size = document.createElement('span')
        size.setAttribute('class', 'size')
        size.innerHTML = element.size

        let date = document.createElement('span')
        date.setAttribute('class', 'date')
        date.innerHTML = element.date


        details.appendChild(size)
        details.appendChild(date)

        li.appendChild(img);
        li.appendChild(name);
        li.appendChild(details);

        return li
}

function dbl_click_element_handler(event) {
    let clickedElement = event.target;
    if (clickedElement.tagName.toLowerCase() !== 'li') {
        clickedElement = clickedElement.closest('li.list-group-item');
    }
    // if(event.target.parentElement.className === '') {

    const list = clickedElement.parentElement;
    console.log(list.getAttribute('path'))
    const path = clickedElement.id.substring(0, clickedElement.id.length - list.length)
    console.log(path)
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

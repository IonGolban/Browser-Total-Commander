const url = 'http://localhost:5000/';

function $(selector, context = document) {
    const elements = context.querySelectorAll(selector);

    if (selector[0] == '#') {
        return elements[0];
    } else if (selector[0] == '.') {
        return elements;
    }
}

const panel1 = $('#panel1');
const panel2 = $('#panel2');
const main_dir_name1 = $('#main-dir-name1');
const main_dir_name2 = $('#main-dir-name2');

const rename_button = $('#rename-button');
const copy_button = $('#copy-button');
const move_button = $('#move-button');
const delete_button = $('#delete-button');
const create_file_button = $('#create-file-button')
const create_dir_button = $('#create-dir-button')
const edit_file_button = $('#edit-file-button')
const go_to_button_1 = $('#go-to-button-1')
const go_to_button_2 = $('#go-to-button-2')
document.addEventListener('DOMContentLoaded', () => {
    console.log(jsonData)
    addClickListeners();
});

function addClickListeners() {
    const listItems = $('.list-group-item');
    console.log("listItems = ", listItems);
    listItems.forEach((item) => {
        console.log(item.id)
        item.addEventListener('click', click_element_handler);
        item.addEventListener('dblclick', dbl_click_element_handler)
    });
}


async function dbl_click_element_handler(event) {
    let clickedElement = event.target;
    if (clickedElement.tagName.toLowerCase() !== 'li') {
        clickedElement = clickedElement.closest('li.list-group-item');
    }
    if (clickedElement.getAttribute('data-type') === 'file') {
        await view_file_content(clickedElement)
        return;
    }

    const el_id = clickedElement.id;
    console.log(el_id)
    console.log(el_id.substring(0, el_id.length - 2))
    const goto_dir_encoded = encodeURIComponent(el_id.substring(0, el_id.length - 2));
    console.log("encoded", goto_dir_encoded)
    const dir_name_1_encoded = encodeURIComponent($("#main-dir-name1").innerHTML);
    const dir_name_2_encoded = encodeURIComponent($("#main-dir-name2").innerHTML);
    const panel_changed_id = clickedElement.parentElement.parentElement.getAttribute('id')

    const goto_url = url + 'goto/' + panel_changed_id + '/' + dir_name_1_encoded + '/' + dir_name_2_encoded + '/' + goto_dir_encoded;
    window.location.href = goto_url;


}

function click_element_handler(event) {
    let clickedElement = event.target;

    const isCtrlPressed = event.ctrlKey || event.metaKey;

    if (clickedElement.tagName.toLowerCase() !== 'li') {
        clickedElement = clickedElement.closest('li.list-group-item');
    }


    if (!isCtrlPressed) {
        const selectedItems = $('.selected');
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
    const selectedItems = $('.selected');
    if (selectedItems.length !== 1) {
        alert("Please select one item to rename")
        return;
    }

    let modal = $('#rename-modal');
    let old_name = selectedItems[0].id.substring(0, selectedItems[0].id.length - 2);
    let modal_old_name = $('#old-name-rename-modal');
    modal_old_name.innerHTML = "Old-name: " + old_name;

    modal.style.display = 'block';
});

document.querySelectorAll('.close').forEach((item) => {
    item.addEventListener('click', () => window.location.reload());
});

$("#confirm-rename-modal-button").addEventListener('click', async () => {
    let new_name = $('#new-rename-modal').value;
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
    let all_elements = $('.list-group-item');
    for (let element of all_elements) {
        if (element.parentElement.getAttribute('id') === selectedItem.parentElement.getAttribute('id')
            && element.id.substring(0, element.id.length - 2) === new_name) {
            alert("Name already exists")
            return;
        }
    }

    let main_dir_name = selectedItem.parentElement.getAttribute('path');

    console.log("main_dir_name", main_dir_name)

    let element_id = selectedItem.id;

    // @app.route('/rename/<main_dir_1>/<main_dir_2>/<old_name_path>/<new_name_path>', methods=["GET"])
    const dir_name_1_encoded = encodeURIComponent($("#main-dir-name1").innerHTML);
    const dir_name_2_encoded = encodeURIComponent($("#main-dir-name2").innerHTML);
    const old_name_encoded = encodeURIComponent(main_dir_name + "\\" + old_name);
    const new_name_encoded = encodeURIComponent(main_dir_name + "\\" + new_name);

    const rename_url = url + 'rename/' + dir_name_1_encoded + '/' + dir_name_2_encoded + '/' + old_name_encoded + '/' + new_name_encoded;

    const response = await api_call('PUT', rename_url, {})
    if (response.ok === false) {
        alert("Error renaming")
        console.log('Server response:', response.message);

        return;
    }
    console.log('Server response:', response.message);
    window.location.reload();

});

copy_button.addEventListener('click', async () => {
    await generic_move_copy_delete_request_button('copy')
});

move_button.addEventListener('click', async () => {
    await generic_move_copy_delete_request_button('move')
});

delete_button.addEventListener('click', async () => {
    await generic_move_copy_delete_request_button('delete')
});

go_to_button_1.addEventListener('click', async () => {

    const dir_name_1_encoded = encodeURIComponent($("#main-dir-name1").innerHTML);
    const dir_name_2_encoded = encodeURIComponent($("#main-dir-name2").innerHTML);
    window.location.href = url + 'goto/' + dir_name_1_encoded + '/' + dir_name_2_encoded;

});

go_to_button_2.addEventListener('click', async () => {

    const dir_name_1_encoded = encodeURIComponent($("#main-dir-name1").innerHTML);
    const dir_name_2_encoded = encodeURIComponent($("#main-dir-name2").innerHTML);

    window.location.href = url + 'goto/' + dir_name_1_encoded + '/' + dir_name_2_encoded;

});

async function generic_move_copy_delete_request_button(type) {
    const selectedItems = $('.selected');

    const req_type = type === 'delete' ? 'DELETE' : 'POST';

    if (selectedItems.length === 0) {
        alert("Please select at least one item to copy")
        return;
    }

    const panel_id_from_copy = selectedItems[0].parentElement.parentElement.getAttribute('id');

    for (selectedItem of selectedItems) {
        if (selectedItem.parentElement.parentElement.getAttribute('id') !== panel_id_from_copy) {
            alert("Ignore deleting: Please select items from the same panel")
            return;
        }
    }

    let elements_to_copy = [];
    for (selectedItem of selectedItems) {
        elements_to_copy.push(selectedItem.id.substring(0, selectedItem.id.length - 2));
    }

    console.log(elements_to_copy);
    let main_dir_name_from_copy = "";
    let main_dir_name_to_copy = "";
    if (panel_id_from_copy === 'panel1') {
        main_dir_name_from_copy = $("#main-dir-name1").innerHTML;
        main_dir_name_to_copy = $("#main-dir-name2").innerHTML;
    } else {
        main_dir_name_from_copy = $("#main-dir-name2").innerHTML;
        main_dir_name_to_copy = $("#main-dir-name1").innerHTML;
    }

    if (type === "move" || type === "copy") {
        for (selectedItem of selectedItems) {

            if (main_dir_name_to_copy === main_dir_name_from_copy + "\\" + selectedItem.id.substring(0, selectedItem.id.length - 2)) {
                alert("Cannot move or copy to a subfolder")
                return;
            }
        }

    }

    const main_dir_name_from_copy_encoded = encodeURIComponent(main_dir_name_from_copy);

    const main_dir_name_to_copy_encoded = encodeURIComponent(main_dir_name_to_copy);
    const request_url = url + type + '/' + main_dir_name_from_copy_encoded + (type !== "delete" ? '/' + main_dir_name_to_copy_encoded : "");
    console.log(request_url)
    const response = await api_call(req_type, request_url, {elements: elements_to_copy})
    if (response.ok === false) {
        alert("Error : " + response.message)
        console.log('Server response:', response.message);
        return;
    }
    console.log('Server response:', response.message);
    window.location.reload();
}

create_file_button.addEventListener("click", () => {
    let modal = $('#create-file-modal');
    modal.style.display = 'block';
});
create_dir_button.addEventListener("click", () => {
    let modal = $('#create-dir-modal');
    modal.style.display = 'block';
});

$("#confirm-create-file-button").addEventListener('click', async () => {
    const name = $('#create-file-input').value;
    console.log("name= " + name)

    if (name === "") {
        alert("Please enter a name")
        return;
    }
    const choice = $('#panel-choice-file').value;
    console.log("choice= " + choice)
    const panel = $('#' + choice);
    console.log("panel= " + panel)

    let elements_from_panel = panel.querySelectorAll('.list-group-item');
    for (let element of elements_from_panel) {
        if (element.id.substring(0, element.id.length - 2) === name) {
            alert("Name already exists")
            return;
        }
    }

    const dir_name = $('#' + choice).getAttribute('path');

    const response = await create_file('file', dir_name, name)
    if (response.ok === false) {
        alert("Error creating file " + response.message)
        console.log(response.message)
        return;
    }

    $('#create-file-input').value = "";
    $('#create-file-modal').style.display = 'none';
});

$("#confirm-create-dir-button").addEventListener('click', async () => {

    const name = $('#create-dir-input').value;
    if (name === "") {
        alert("Please enter a name")
        return;
    }
    const choice = $('#panel-choice-dir').value;

    const panel = $('#' + choice);
    let elements_from_panel = panel.querySelectorAll('.list-group-item');
    for (let element of elements_from_panel) {
        if (element.id.substring(0, element.id.length - 2) === name) {
            alert("Name already exists")
            return;
        }
    }

    const main_dir_name = panel.getAttribute('path');

    await create_file('dir', main_dir_name, name)

    $('#create-dir-input').value = "";
    $('#create-dir-modal').style.display = 'none';

});

async function create_file(type, dir_name, name) {
    const dir_name_encoded = encodeURIComponent(dir_name);
    const name_encoded = encodeURIComponent(name);
    const request_url = url + "create" + "/" + type + '/' + dir_name_encoded + '/' + name_encoded;
    console.log(request_url)
    const response = await api_call('POST', request_url, {})
    if (response.ok === false) {
        alert("Error creating file")
        console.log(response.message)
        return;
    }
    console.log('Server response:', response.message);
    window.location.reload();
}


edit_file_button.addEventListener("click", async () => {
    const selected_items = $('.selected');
    if (selected_items.length !== 1) {
        alert("Please select one item to edit")
        return;
    }
    if (selected_items[0].getAttribute('data-type') !== 'file') {
        alert("Please select a file to edit")
        return;
    }
    await view_file_content(selected_items[0])
});

async function view_file_content(selected_item) {

    let modal = $('#edit-file-modal');
    let file_name = selected_item.id.substring(0, selected_item.id.length - 2);
    let modal_edit_file_name = $('#edit-file-name');
    modal_edit_file_name.setAttribute('value', file_name);
    modal_edit_file_name.innerHTML = "Edit file: " + file_name;
    let dir_name = selected_item.parentElement.getAttribute('path');
    modal.setAttribute('path', dir_name);
    const reponse_status = await init_file_content(dir_name, file_name)
    if (reponse_status === false) {
        alert("Error getting file content")
        return;
    }
    modal.style.display = 'block';

}

$("#confirm-edit-file-modal-button").addEventListener('click', async () => {
    const modal = $('#edit-file-modal');
    const dir_name = modal.getAttribute('path');
    const file_name = $('#edit-file-name').getAttribute('value');
    const content = $('#edit-file-content').innerText;

    const response_status = await edit_file_content(dir_name, file_name, content)

});

async function init_file_content(dir_name, file_name) {
    const path_encoded = encodeURIComponent(dir_name);
    const file_name_encoded = encodeURIComponent(file_name);
    const request_url = url + "content" + '/' + path_encoded + '/' + file_name_encoded;
    console.log(request_url)

    const response = await api_call('GET', request_url, {})
    if (response.ok === false) {
        alert("Error getting file content")
        return false;
    }

    console.log('Server response content:', response.content);
    $('#edit-file-content').innerText = response.content;
}

async function edit_file_content(dir_name, file_name, content) {
    const path_encoded = encodeURIComponent(dir_name);
    const file_name_encoded = encodeURIComponent(file_name);
    const request_url = url + "edit/content" + '/' + path_encoded + '/' + file_name_encoded;
    console.log(request_url)
    const response = await api_call('PUT', request_url, {content: content})

    if (response.ok == false) {
        alert("Error editing file content")
        console.log(response.message)
    }

    console.log('Server response:', response.message);
    alert("File content edited successfully")
}


async function api_call(method, url, data) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        }
        if (method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        const response = await fetch(url, options);
        return await response.json();

    } catch (e) {
        console.log(e)
    }

}
function onNfcKeySubmit() {
    const files = document.getElementById('nfc_file').files;
    if (files.length === 0) {
        return;
    }
    const file = files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const nfcKey = e.target.result;
        document.getElementById('card_data').value = btoa(nfcKey);
    }
    reader.readAsText(file);
}
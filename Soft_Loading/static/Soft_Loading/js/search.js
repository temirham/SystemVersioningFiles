//document.querySelector('#header_navbar img.lupe').addEventListener('click', () => {
//    event.target.parentNode.submit();
//});

//let deldocument.querySelector('delete').addEventListener('click', () => {
//event.target.parentNode.submit();
//});

// we can use hidden form and make .submit; under - is usless

// thats because easier to make lupe button then form button be invisible:
document.querySelector('#header_navbar img.lupe').addEventListener('click', () => {
    let href = window.location.href;
    let add = '';
    if (href.includes('?')) {
        let last_smbh = href.substring(href.length - 1);
        if (last_smbh != '?' && last_smbh != '&') add = '&';

//        let spl = href.split('search=');
//        if (spl.length > 1) href = spl[0] + spl[1].slice(spl[1].indexOf('&'));
    }
    else add = '?'

    let search_query = event.target.parentNode.querySelector('input.navbar_search').value;
    if (search_query.replace(' ', '') != '') {
        window.location.href = href + add + 'search=' + url_encode(event.target.parentNode.querySelector('input.navbar_search').value);
    }
});

// there isn't need to encode language simbols il left nav, but special characters which can appear in search,
// should be encoded:
function url_encode(str) {
    return escape(encodeURIComponent(str));
}
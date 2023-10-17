// This is not to drop get filters while following link or to change some params in it to yours by link get part or
// by given_param_dict value
//      Using: [elements lists here], {'par_name': ('value' - if its needed to changed here, or '' - if its changes in
//      get part of html link'), true - if you want insert that parameters even if they arnt in link}




function save_get_param_while_link_follow(links_list) {
    let params_string = location.search;

    for (let i = 0; i < links_list.length; i++) {
        for (let j = 0; j < links_list[i].length; j++) {

            // adding event for every element:
            links_list[i][j].addEventListener('click', (event) => {
                event.preventDefault();

                let new_params = '';
                let params_list = params_string.replace('?', '').split('&').filter((f) => { return f !== '' });

                // for every get parameter in browser link:
		        for(let i = 0; i < params_list.length; i++) {
			        let key = params_list[i].split('=')[0];

			        // if that parameter is not set in link:
                    if (!event.target.href.includes(key)) new_params = new_params + '&' + params_list[i];
			    }

                // needed to process '?' which could be in link or couldnt, and last &
                let add = ''; let i2 = 0;
                if (event.target.href.indexOf('?') == -1 && new_params !== '') { add='?'; i2++; }

		        // going on link:
                window.location.href = links_list[i][j].href + add + new_params.slice(i2);
            });
        }
    }
}

save_get_param_while_link_follow([document.getElementsByClassName("side_nav_sub_a"),
                                 document.getElementsByClassName("side_nav_main_a"),
                                 document.getElementsByClassName("navbar_cases")[0].querySelectorAll('a:not(.home)')]);

// wrote like that to use in future (it works as with full href as with params):
function get_string_to_dict(href, is_full_href=false) {
    let params_dict = {};
    let params_list;

    let parts = href.split('?').length;
    if (parts > 2) throw 'error-link in get_params_to_dict (double ? symbol)' // there is error link
    else {
        let query_part;
        if (parts == 1) { // not full href or full href without parameters
            if (is_full_href) return params_dict;
            query_part = href.split('?')[0];
        }
        else query_part = href.split('?')[1];
        params_list = query_part.split('&').filter((f) => { return f !== '' });

	    for(let i = 0; i < params_list.length; i++) {
	        pair_list = params_list[i].split('=');
            params_dict[pair_list[0]] = pair_list[1]; //if there isn't param value - undefined
        }
        return params_dict;
    }
}

//function catch_post_to_dict(form) {
//    form.addEventListener('submit', () => {
//        form.
//    });
//}
//
//function search_params_to_dict() {
//    let query_string = location.search; //window.
//    return get_params_to_dict(query_string);
//}
//
//// base href can incude query string or not, params could contain query string, query dict or be non used
//function redirect_to(href, params='none') {
//
//}
//
//function dict_to_get_params(dict, add_query_symbol = false) {
//    let query = '';
//    for (let key in dict) query += key + '=' + dict[key] + '&';
//
//    query = query.slice(0, query.length - 1);
//    if (add_query_symbol) query = '?' + query;
//    return query;
//}

//
//let r = {}
//r['l'] = 'rt'
//r['r'] = 'rt2'
//console.log(dict_to_get_params(get_params_to_dict(window.location.href)));
//document.getElementsByClassName('href')[0].addEventListener('click', ()=>{
//    let dict = get_params_to_dict(window.location.href);
//    let params_from_dict = dict_to_get_params(dict);
////    for(let key in dict.keys){
////        document.getElementsByClassName('t')[0].value += (key + '=' + dict[key] + '&');
////    }
//    document.getElementsByClassName('t')[0].value += params_from_dict;
//})














//// This is not to drop get filters while following link:
//function save_get_params_while_link_follow(links_list) {
//    let params = location.search; //it changes dinamicly
//
//    for (let i = 0; i < links_list.length; i++){
//        links_list[i];
//        let number = links_list[i].length;
//
//        for (let j = 0; j < number; j++) {
//            links_list[i][j].addEventListener('click', (event) => {
//                event.preventDefault();
//                window.location.href = links_list[i][j].href + params;
//            });
//        }
//    }
//}
//
//
//save_get_params_while_link_follow([document.getElementsByClassName("side_nav_sub_a"),
//                                   document.getElementsByClassName("side_nav_main_a")]);
//
//сhange_get_param_while_link_follow([document.getElementsByClassName("navbar_cases")[0].querySelectorAll('a')]);
//
//
//


//
//// left nav sub links:
//let left_nav_sub_links = document.getElementsByClassName("side_nav_sub_a");
//let number = left_nav_sub_links.length;
//
//for (let i = 0; i < number; i++) {
//    left_nav_sub_links[i].addEventListener('click', (event) => {
//        event.preventDefault();
//        window.location.href = left_nav_sub_links[i].href + params;
//    });
//}
//
//// left nav main links:
//let left_nav_main_links = document.getElementsByClassName("side_nav_main_a");
//number = left_nav_main_links.length;
//
//for (let i = 0; i < number; i++) {
//    left_nav_main_links[i].addEventListener('click', (event) => {
//        event.preventDefault();
//        window.location.href = left_nav_main_links[i].href + params;
//    });
//}
//
//// top nav links:
//let top_nav_links = document.getElementsByClassName("navbar_cases")[0].querySelectorAll('a');
//number = top_nav_links.length;
//
//for (let i = 0; i < number; i++) {
//    top_nav_links[i].addEventListener('click', (event) => {
//        event.preventDefault();
//
//        // deleting old parameter:
//        let new_params = '';
//        let par = params.replace('?', '').split('&');
//		for(let i = 0; i < par.length; i++) {
//			let key = par[i].split('=');
//			if(key[0] !== 'plantf') {
//				new_params =  new_params + '&' + par[i];
//			}
//		}
//
//        window.location.href = top_nav_links[i].href  +  new_params;
//    });
//}

//// number ogranichenie:
//
//
//
//// This is not to drop get filters while following link or to change some params in it to yours by link get part or
//// by given_param_dict value
////      Using: [elements lists here], {'par_name': ('value' - if its needed to changed here, or '' - if its changes in
////      get part of html link'), true - if you want insert that parameters even if they arnt in link}
//function set_get_param_while_link_follow(links_list, given_param_dict, change_or_insert) {
//    let params_string = location.search;
//    items_list = items(given_param_dict); // like in python
//
//    for (let i = 0; i < links_list.length; i++) {
//        for (let j = 0; j < links_list[i].length; j++) {
//
//            // adding event for every element:
//            links_list[i][j].addEventListener('click', (event) => {
//                event.preventDefault();
//
//                let new_params = '';
//                let params_list = params_string.replace('?', '').split('&').filter((f) => { return f !== '' });
//
//                // for every get parameter in browser link:
//		        for(let i = 0; i < params_list.length; i++) {
//			        let key = params_list[i].split('=')[0];
//
//                    // searching on given parameters to find match
//                    let found_given_param = '';
//			        for (let p = 0; p < items_list.length; p++) {
//			            if(key == items_list[p]['key']) { found_given_param = items_list[p]['value']; break; }
//			        }
//
//                    // changing if it needed manually:
//			        if (found_given_param !== '') new_params =  new_params + '&' +  key + '=' + found_given_param;
//                    else if (!event.target.href.includes(key)) new_params = new_params + '&' + params_list[i];
//                    // inserting if it needed manually:
//
//
//			        // main part
//
//			    }
//
//                // needed to process '?' which could be in link or couldnt, and last &
//                let add = '';
//                let i2 = 0;
//                if (event.target.href.indexOf('?') == -1 && new_params !== '') { add='?'; i2++; }
//
//		        // going on link:
//                window.location.href = links_list[i][j].href + add + new_params.slice(i2);
//            });
//        }
//    }
//}

//function items(dict) {
//    var key, items_list = [];
//    for(key in dict)  items_list.push({'key': key, 'value': dict[key]});
//    return items_list;
//}


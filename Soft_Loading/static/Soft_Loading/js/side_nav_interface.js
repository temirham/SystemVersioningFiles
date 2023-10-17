let svg_buttons = document.getElementsByClassName("visible");
let num_buttons = svg_buttons.length;

for (let i = 0; i < num_buttons; i++) {
    svg_buttons[i].addEventListener('click', (event) => {

    const main_cat_brick = event.target.parentNode;
    const cat_group = event.target.parentNode.parentNode;
    const sub_cat_group = cat_group.querySelector('.sub_cat_group');

    const minusSvg  = event.target.parentNode.querySelector('.minus');
    const plusSvg  = event.target.parentNode.querySelector('.plus');
    if (window.getComputedStyle(sub_cat_group).display === 'none') {
        sub_cat_group.style.display = 'block';

        main_cat_brick.style.backgroundColor = '#fd6f29';
        main_cat_brick.querySelector('a').style.color = 'white';

        minusSvg.style.display = 'block'
        plusSvg.style.display = 'none'
    } else {
        sub_cat_group.style.display = 'none';

        main_cat_brick.style.backgroundColor = 'white';
        main_cat_brick.querySelector('a').style.color = 'black';

        minusSvg.style.display = 'none'
        plusSvg.style.display = 'block'
    }
  }, false);
}

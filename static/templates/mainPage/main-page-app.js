import {category as ct} from "../../components/category/category.js";
import {New} from "../../components/new/new.js"
window.customElements.define('new-section' , New)
window.customElements.define('new-category' , ct)
let nav = document.getElementsByTagName('nav')[0]
let panelLogo = document.getElementById('panel')
let blurDiv = document.getElementById('blur')
let panelSelect = document.getElementsByClassName('panel-select-box')[0] ;
let dateSpans = document.getElementsByClassName('date-text')
let searchBox = document.getElementById('searchBox')
let searchResult = document.getElementById('search-result')
dateSpans = [...dateSpans]
async function getToken(){
     let response = await fetch('/blog/getCsrfToken')
     let data = await response.json()
     return data['csrftoken']
}
window.addEventListener('scroll' , (e)=>{
    if(window.scrollY > 10){
            nav.classList.add('scrolled') ;
    }
    else {
           nav.classList.remove('scrolled') ;
    }
})
panelLogo.addEventListener('click' , (e)=>{
      panelSelect.style.visibility = "visible"
      panelSelect.style.opacity = "1"
      blurDiv.style.visibility = "visible"
      blurDiv.style.opacity = "1"
})
window.addEventListener('click' , (e)=>{
      searchResult.style.visibility = "hidden"
      searchResult.style.opacity = "0"
})

blurDiv.addEventListener('click' , (e)=>{
      panelSelect.style.visibility = "hidden"
      panelSelect.style.opacity = "0"
      blurDiv.style.visibility = "hidden"
      blurDiv.style.opacity = "0"
})

searchBox.addEventListener('keyup' , async (e)=>{
    if(event.keyCode >= 65 && event.keyCode <= 90 || // A-Z
      event.keyCode >= 97 && event.keyCode <= 122 || // a-z
      event.keyCode >= 48 && event.keyCode <= 57 || event.keyCode==32 || event.keyCode==8) {
        let response = await fetch('/blog/getSearchResult', {
            body: JSON.stringify({
                'searchText': e.target.value
            },) ,
            method: "POST" ,
            headers : {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': await getToken() //This is crucial for Django's CSRF middleware
            }
        })
        let data = await response.json()
        searchResult.style.visibility = 'visible'
        searchResult.style.opacity = '1'
        searchResult.innerHTML = data['template']
        if(!data['template'] || e.target.value===''){
                 searchResult.style.visibility = "hidden"
                 searchResult.style.opacity = "0"
        }
    }
})



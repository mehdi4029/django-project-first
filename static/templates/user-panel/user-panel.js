import {New} from '../../components/new/new.js'
window.customElements.define('new-section' , New)

let container = document.getElementById('container')
let accessBox = document.getElementById('user-access')
let username = document.getElementById('username')
let email = document.getElementById('email')

let deleteComment = async(data)=>{
    let response = await fetch(`/blog/deleteComment/${data}`)
    let rdata = await response.json()
    let path = rdata['url']
    location.href = path
}


let commentManagement = async ()=>{
    let response = await fetch('/blog/commentsList')
    let data = await response.json()
    container.innerHTML = data['template']
    let commentDeleteTool = document.getElementsByClassName('commentDeleteTool')
    commentDeleteTool = [...commentDeleteTool]
    commentDeleteTool.forEach((tool)=>{
        tool.addEventListener('click' ,(e)=>{
            if(e.target.tagName === 'svg'){
                 deleteComment(e.target.dataset.id)
            }
        })
    })
}



async function fetchManipulateForm(data){
    console.log(data)
    let response = await fetch(`/blog/fetchManipulateForm/${data}`)
    let json = await response.json()
    let postStatusDict = {
        'draft' : 'پیش نویس' ,
        'published' : 'پخش در همین لحطه(در صورت خالی بودن تاریخ انتشار)'
    }
    console.log(json['myPostImportant'])
    container.innerHTML = json['template']
    // here we fill the fetched form values with our previous values we had
    let inputTitle = document.getElementById('post-title') ;let inputBody = document.getElementById('post-body')
    let inputCat = document.getElementById('post-cat') ; let inputStatus = document.getElementById('post-status')
    let inputImportance = document.getElementById('post-important')
    inputTitle.value = json['myPostTitle']
    inputBody.value = json['myPostBody']
    inputStatus.value = postStatusDict[json['myPostStatus']]
    inputCat.value = json['myPostCat']
    if(json['myPostImportant']===true){
         inputImportance.checked = true ;
         let flag = true ;
         inputImportance.addEventListener('click' , (e)=>{
             flag = !flag
            inputImportance.checked = flag
         })
    }
}


let updatePost = async (e)=>{
    console.log('hello')
    let response = await fetch('/blog/updatePostRequest')
    let data = await response.json()
    container.innerHTML = data['template']
    let tool = document.getElementsByClassName('post-delete-tool')
    tool =  [...tool]
    tool.forEach((btn)=>{
         btn.addEventListener('click' , (event)=>{
             if(event.target.tagName === 'svg') {
                 fetchManipulateForm(event.target.parentElement.dataset.id)
             }
         })
    })

}

let deletePost = async (e)=>{
    console.log('hello')
    let response = await fetch('/blog/deletePostRequest')
    let data = await response.json()
    container.innerHTML = data['template']
}


let deleteCategory = async (e)=>{
    let response = await fetch('/blog/deleteCategory')
    let data = await response.json()
    container.innerHTML = data['template']
}


let updateCategory = async (e)=>{
    let response = await fetch('/blog/updateCategory')
    let data = await response.json()
    container.innerHTML = data['template']
}


let loadCreateForm = async ()=>{
     let response = await fetch('/blog/loadCreateForm')
     let data = await response.json()
     let formFrag = data['form'] ;
     container.innerHTML = formFrag
     $(document).ready(function() {
          $(".datepick").persianDatepicker({
              initialValue : false ,
          });
        });
}

let createCategory = async ()=> {
    let res = await fetch('/blog/createCategoryRequest')
    let data = await res.json()
    container.innerHTML = data['cat-form']
}



let btnListener = ()=>{
     let Btns = document.getElementsByClassName('btn')
     Btns = [...Btns]
//  templates appending to container based on access that requested
    for (let btn of Btns){
    btn.addEventListener('click' , (e)=>{
        for (let i of [...accessBox.children]){
             i.classList.remove('active') ;
        }
        e.target.parentElement.classList.add('active') ;
        if(btn.id === "create-post-btn"){
             loadCreateForm()
        }
        if(btn.id === "create-category-btn"){
             createCategory()
        }
        if(btn.id === "delete-category-btn"){
            deleteCategory()
        }
        if(btn.id==="update-category-btn"){
             updateCategory()
        }
        if(btn.id === "delete-post-btn"){
             deletePost()
        }
        if(btn.id === "manipulate-btn"){
             updatePost()
        }
        if(btn.id === "comment-management-btn"){
            commentManagement()
        }
    })
    }
}



// fetch access
window.addEventListener('load' , async (e)=>{
     let respond = await fetch('/blog/show-panel')
     let data = await respond.json()
     let titles = data['link_titles']
     let ids = data['link_ids']
     let svgs = data['link_images']
     for (let i=0 ; i<=titles.length-1 ; i++){
         accessBox.innerHTML += `
               <div id="access" class="access">
                    ${svgs[i]} 
                    <a class="${ids[i]} btn" id="${ids[i]}">
                        ${titles[i]}
                    </a>
               </div>
         `
     }
     username.innerHTML += data['username']
     email.innerHTML += data['email']
     btnListener()
})